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
# Terterman message lib.
#
# Provides a high-level class to encode/decode testerman messages
# over most internal and external interfaces. 
#
##

import re
import base64
import pickle
import JSON
#import urllib

# Message separator.
# On reference perf tests, 8% faster when using \n instead of \r\n.
SEPARATOR = '\n'

URI_REGEXP = re.compile(r'(?P<scheme>[a-z]+):((?P<user>[a-zA-Z0-9_\.-]+)@)?(?P<domain>[a-zA-Z0-9_\.-]+)')
HEADERLINE_REGEXP = re.compile(r'(?P<header>[a-zA-Z0-9_-]+)\s*:\s*(?P<value>.*)')
REQUESTLINE_REGEXP = re.compile(r'(?P<method>[a-zA-Z0-9_-]+)\s*(?P<uri>[^\s]*)\s*(?P<protocol>[a-zA-Z0-9_-]+)/(?P<version>[0-9\.]+)')
STATUSLINE_REGEXP = re.compile(r'(?P<status>[0-9]+)\s*(?P<reason>.*)')

class Uri(object):
	"""
	Testerman URI object.
	
	Encode/decode uri of the form:
	<scheme>:[<user>@]<domain>
	"""
	def __init__(self, uri):
		self.scheme = None
		self.user = None
		self.domain = None
		self.parse(uri)
	
	def parse(self, uri):
		m = URI_REGEXP.match(uri)
		if not m:
			raise Exception("Invalid URI format (%s)" % uri)
		self.setScheme(m.group('scheme'))
		self.setDomain(m.group('domain'))
		self.setUser(m.group('user')) # allows setting it to None
	
	def setScheme(self, scheme):
		self.scheme = scheme
	
	def setUser(self, user):
		self.user = user
	
	def setDomain(self, domain):
		self.domain = domain
	
	def getScheme(self):
		return self.scheme
	
	def getUser(self):
		return self.user
	
	def getDomain(self):
		return self.domain
	
	def __str__(self):
		if self.user:
			return "%s:%s@%s" % (self.scheme, self.user, self.domain)
		else:
			return "%s:%s" % (self.scheme, self.domain)


class Message(object):
	"""
	Base message implemented by Testerman messages
	(requests, notifications, responses)
	"""
	
	TYPE_REQUEST = "request"
	TYPE_NOTIFICATION = "notification"
	
	ENCODING_UTF8 = "utf-8"
	ENCODING_BASE64 = "base64"
	
	CONTENT_TYPE_PYTHON_PICKLE = "application/x-python-pickle" # specific type
	CONTENT_TYPE_JSON = "application/json" # Official one
	
	def __init__(self):
		self.headers = {} # dict of str of unicode
		self.body = None # unicode or datastring

	def setHeader(self, header, value):
		if not isinstance(value, basestring):
			value = str(value)
		self.headers[header] = value.encode('utf-8')
	
	def getHeader(self, header):
		return self.headers.get(header, None)
	
	def setBody(self, body):
		"""
		Sets the body directly.
		"""
		self.body = body
	
	def setApplicationBody(self, body, profile = CONTENT_TYPE_JSON):
		"""
		Convenience function: encode the body, sets
		both Content-Encoding ad Content-Type as JSON encoding.
		"""
		if profile == self.CONTENT_TYPE_JSON:
			self.body = JSON.dumps(body)
			self.setContentEncoding(self.ENCODING_UTF8)
			self.setContentType(self.CONTENT_TYPE_JSON)
		elif profile == self.CONTENT_TYPE_PYTHON_PICKLE:
			self.body = pickle.dumps(body)
			self.setContentEncoding(self.ENCODING_UTF8)
			self.setContentType(self.CONTENT_TYPE_PYTHON_PICKLE)
		else:
			raise Exception("Invalid application body encoding profile (%s)" % str(encodeAs))
	
	def getBody(self):
		return self.body
	
	def isResponse(self):
		return False

	def isNotification(self):
		return False

	def isRequest(self):
		return False
	
	def getContentEncoding(self):
		return self.headers.get("Content-Encoding", self.ENCODING_UTF8)
	
	def getContentType(self):
		return self.headers.get("Content-Type", None)

	def setContentEncoding(self, encoding):
		self.headers["Content-Encoding"] = encoding
	
	def setContentType(self, contentType):
		self.headers["Content-Type"] = contentType

	def getApplicationBody(self):
		"""
		According to Content-Encoding and Content-Type, tries to decode the body.
		If the encoding is not supported by this method, returns None.
		"""	
		contentType = self.getContentType()
		if contentType == self.CONTENT_TYPE_JSON:
			ret = JSON.loads(self.getBody())
			return ret
		elif contentType == self.CONTENT_TYPE_PYTHON_PICKLE:
			ret = pickle.loads(self.getBody())
			return ret
		else:
			return self.body

	def getTransactionId(self):
		try:
			return int(self.headers["Transaction-Id"])
		except:
			return None


class Request(Message):
	def __init__(self, method, uri, protocol, version):
		"""
		@type  uri: Uri
		"""
		Message.__init__(self)
		self.method = method
		if isinstance(uri, basestring):
			self.uri = Uri(uri)
		else:
			self.uri = uri
		self.protocol = protocol
		self.version = version
		self.setHeader('Type', Message.TYPE_REQUEST)

	def __str__(self):
		"""
		Encodes a message to a utf-8 string.
		The final \00 is not part of the message, but just a transport separator.
		"""
		ret = [ "%s %s %s/%s" % (self.method, str(self.uri), self.protocol, self.version) ]
		for (h, v) in self.headers.items():
			ret.append("%s: %s" % (h, v.encode('utf-8')))
		ret.append('')
		if self.body:
			if self.getContentEncoding() == self.ENCODING_UTF8:
				ret.append(self.body) #.encode('utf-8')
			else:
				ret.append(self.body)
		return SEPARATOR.join(ret)

	def getUri(self):
		return self.uri
	
	def getMethod(self):
		return self.method
	
	def getProtocol(self):
		return self.protocol
	
	def getVersion(self):
		return self.version

	def makeRequest(self):
		self.setHeader('Type', Message.TYPE_REQUEST)

	def makeNotification(self):
		self.setHeader('Type', Message.TYPE_NOTIFICATION)

	def isRequest(self):
		return self.headers.has_key("Type") and self.headers["Type"] == Message.TYPE_REQUEST
		
	def isNotification(self):
		return self.headers.has_key("Type") and self.headers["Type"] == Message.TYPE_NOTIFICATION


class Notification(Request):
	def __init__(self, method, uri, protocol, version):
		Request.__init__(self, method, uri, protocol, version)
		self.makeNotification()

class Response(Message):
	def __init__(self, statusCode, reasonPhrase):
		Message.__init__(self)
		self.statusCode = int(statusCode)
		self.reasonPhrase = reasonPhrase

	def __str__(self):
		"""
		Encodes a message to a utf-8 string.
		The final \00 is not part of the message, but just a transport separator.
		"""
		ret = [ "%s %s" % (str(self.statusCode), str(self.reasonPhrase)) ]
		for (h, v) in self.headers.items():
			ret.append("%s: %s" % (h, v.encode('utf-8')))
		ret.append("")
		if self.body:
			if self.getContentEncoding() == self.ENCODING_UTF8:
				ret.append(self.body) #.encode('utf-8')
			else:
				ret.append(self.body)
		return SEPARATOR.join(ret)

	def getStatusCode(self):
		return self.statusCode
	
	def getReasonPhrase(self):
		return self.reasonPhrase
				
	def isResponse(self):
		return True

##
# Main message creator from data
##

def parse(data):
	"""
	Parses data into a Message (either a Notification, Request, Response, actually).
	Raises an exception in case of an invalid message.
	"""
	lines = data.split(SEPARATOR)

	# request line, for request and notifications
	m = REQUESTLINE_REGEXP.match(lines[0])
	if m:
		# This is a request
		message = Request(method = m.group('method').upper(), uri = Uri(m.group('uri')), protocol = m.group('protocol'), version = m.group('version'))

	else:
		m = STATUSLINE_REGEXP.match(lines[0])
		if not m:
			raise Exception("Invalid message first line (%s) - not a response, not a request" % str(lines[0]))
		# This is a response
		message = Response(statusCode = m.group('status'), reasonPhrase = m.group('reason'))

	# Common part: headers parsing, body parsing.
	i = 1
	for header in lines[1:]:
		i += 1
		l = header.strip()
		if not header:
			break # reached body
		m = HEADERLINE_REGEXP.match(l)
		if m:
			message.setHeader(m.group('header'), m.group('value').decode('utf-8'))
		else:
			raise Exception("Invalid header in message (%s)" % str(l))
	
	# Body
	if message.getContentEncoding() == message.ENCODING_UTF8:
		message.setBody(SEPARATOR.join(map(lambda x: x.decode('utf-8'), lines[i:])))
	else:
		message.setBody(SEPARATOR.join(lines[i:]))

	# OK, we're done.
	return message
