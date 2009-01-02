##
# This file is part of Testerman, a test automation system.
# Copyright (c) 2008-2009 Sebastien Lefevre and other contributors
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
##

##
# -*- coding: utf-8 -*-
# Implements RTSP encoding/decoding (request and response) over tcp (for now)
# RFC 2326
# 
# Manages CSeq (generates them, matches them when waiting for a response)
# if not provided by the user.
##


import TestermanSA
import TestermanTCI
import TestermanCD

import threading
import socket
import select


class RtspClientProbe(TestermanSA.LocalProbe):
	"""
	type record RtspRequest
	{
		charstring method,
		charstring uri,
		charstring version optional, // default: 'RTSP/1.0', or as configured
		record { charstring <header name>* } headers,
		charstring body optional, // default: ''
	}

	type record RtspResponse
	{
		integer status,
		charstring reason,
		charstring protocol,
		record { charstring <header name>* } headers,
		charstring body,
	}

	type portRtspClientPortType
	{
		in RtspRequest;
		out RtspResponse;
	}
	"""
	def __init__(self):
		TestermanSA.LocalProbe.__init__(self)
		self._mutex = threading.RLock()
		self._responseThread = None
		self._connection = None
		self._cseq = 0
		# Default test adapter parameters
		self.setParameter('version', 'RTSP/1.0')
		self.setParameter('auto_connect', False)
		self.setParameter('maintain_connection', False)
		self.setParameter('host', 'localhost')
		self.setParameter('port', 554)
		self.setParameter('transport', 'tcp')
		self.setParameter('local_ip', '')
		self.setParameter('local_port', 0)

	# LocalProbe reimplementation)
	def onTriMap(self):
		if self['auto_connect']:
			self.connect()
	
	def onTriUnmap(self):
		self.reset()
	
	def onTriExecuteTestCase(self):
		# No static connections
		pass

	def onTriSAReset(self):
		# No static connections
		pass
	
	def send(self, message, sutAddress):
		try:
			# FIXME:
			# Should go to a configured codec instance instead.
			# (since we modify the message here... should be a copy instead)
			if not message.has_key('version'):
				message['version'] = self['version']
			if not message.has_key('headers'):
				message['headers'] = {}
			if not message['headers'].has_key('cseq'):
				message['headers']['cseq'] = self.generateCSeq()
			try:
				encodedMessage = TestermanCD.encode('rtsp.request', message)
			except Exception, e:
				raise TestermanSA.ProbeException('Invalid request message format: cannot encode RTSP request')
			
			# Connect if needed
			if not self.isConnected():
				self.connect()

			# Send our payload
			self._connection.send(encodedMessage)
			TestermanTCI.logSystemSent(self._tsiPortId, encodedMessage.split('\r\n')[0], encodedMessage)
			# Now wait for a response asynchronously
			self.waitResponse(cseq = str(message['headers']['cseq']))
		except Exception, e:
			raise TestermanSA.ProbeException('Unable to send RTSP request: %s' % str(e))
			
	# Specific methods
	def _lock(self):
		self._mutex.acquire()
	
	def _unlock(self):
		self._mutex.release()
	
	def generateCSeq(self):
		self._lock()
		self._cseq += 1
		cseq = self._cseq
		self._unlock()
		return self._cseq
	
	def connect(self):
		"""
		Tcp-connect to the host. Returns when we are ready to send something.
		"""
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
		sock.bind((self['local_ip'], self['local_port']))
		sock.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1)
		# Blocking or not ?
		sock.connect((self['host'], self['port']))
		self._connection = sock
	
	def isConnected(self):
		if self._connection:
			return True
		else:
			return False
	
	def disconnect(self):
		if self._connection:
			try:
				self._connection.close()
			except:
				pass
		self._connection = None
	
	def reset(self):
		if self._responseThread:
			self._responseThread.stop()
		self.disconnect()
		self._responseThread = None
	
	def waitResponse(self, cseq):
		"""
		Creates a thread, wait for the response.
		@type  cseq: string
		@param cseq: the expected cseq in response
		"""
		self._responseThread = ResponseThread(self, self._connection, cseq)
		self._responseThread.start()

class ResponseThread(threading.Thread):
	def __init__(self, probe, socket, cseq):
		threading.Thread.__init__(self)
		self._probe = probe
		self._socket = socket
		self._stopEvent = threading.Event()
		self._cseq = cseq
	
	def run(self):
		buf = ''
		while not self._stopEvent.isSet():
			try:
				r, w, e = select.select([self._socket], [], [], 0.1)
				if self._socket in r:
					read = self._socket.recv(1024*1024)
					buf += read

					# In RTSP/1.0, content-length is mandatory if there is a body.
					decodedMessage = None
					try:
						TestermanTCI.logInternal('data received (bytes %d), decoding attempt...' % len(buf))
						decodedMessage = TestermanCD.decode('rtsp.response', buf)
					except Exception, e:
						# Incomplete message. Wait for more data.
						TestermanTCI.logInternal('unable to decode: %s' % str(e))
						pass
						
					if decodedMessage:
						# System log, always
						TestermanTCI.logSystemReceived(self._probe._tsiPortId, buf.split('\r\n')[0], buf)
						# Conditional enqueing
						if decodedMessage['headers'].get('cseq', None) == self._cseq:
							TestermanTCI.logInternal('message decoded, enqueuing...')
							self._probe.enqueueMessage(decodedMessage)
							self._stopEvent.set()
						else:
							TestermanTCI.logInternal('Invalid cseq received. Not enqueuing, ignoring message')
							buf = ''
							decodedMessage = None
							# Wait for a possible next message...

					elif not read:
						# Message not decoded, nothing to read anymore.
						raise Exception('Incomplete message received, stream interrupted')
						# .. and we should disconnect, too...
						
			except Exception, e:
				TestermanTCI.logInternal('Error while waiting for rtsp response: %s' % str(e))
				self._stopEvent.set()
		if not self._probe['maintain_connection']:
			# Well, maintain connection in RTSP ? 
			self._probe.disconnect()
	
	def stop(self):
		self._stopEvent.set()
		self.join()
					
					
TestermanSA.registerProbeClass('local.rtsp.client', RtspClientProbe)
		
