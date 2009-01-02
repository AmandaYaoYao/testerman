﻿##
# -*- coding: utf-8 -*-
# A plugin to display logs through an XSLT transformation.
#
# $Id: XlstReportView.py,v 1.7 2008/10/02 07:33:57 dduquen Exp $
##

import PyQt4.Qt as qt
import PyQt4.QtXml as QtXml

import os.path

from CommonWidgets import *
from Base import *

import Plugin
import PluginManager

# Plugin ID, as generated by uuidgen
PLUGIN_ID = "4bd1dbc8-7bbc-4bf7-821d-286af583b369"
AUTHOR = "sebastien.lefevre@comverse.com"
VERSION = "1.0.0"
DESCRIPTION = """
This reporter is applies an XSLT transformation to the raw XML Helium execution logs <br />
to extract interesting things according to your needs. <br />
The XSLT files should be named with the ".xlst" extension and located in <br />
the configured directory to make them appear from the report view."""


class WXsltLogView(Plugin.WReportView):
	def __init__(self, parent = None):
		Plugin.WReportView.__init__(self, parent)

		settings = qt.QSettings()
		self.xsltPath = settings.value('plugins/%s/xsltpath' % PLUGIN_ID, qt.QVariant(".")).toString()

		# The log		
		self.xml = qt.QString()

		self.__createWidgets()
	
	def __createWidgets(self):
		layout = qt.QVBoxLayout()
		
		# A button bar with selectable XSLT and save option ?
		buttonLayout = qt.QHBoxLayout()
		buttonLayout.addWidget(qt.QLabel("XSLT transformation:"))
		self.transformationComboBox = qt.QComboBox()
		buttonLayout.addWidget(self.transformationComboBox)
		self.applyTransformationButton = qt.QPushButton("Apply")
		buttonLayout.addWidget(self.applyTransformationButton)
		self.refreshTransformationButton = qt.QPushButton("Refresh available transformations")
		buttonLayout.addWidget(self.refreshTransformationButton)
		buttonLayout.addStretch()
		self.connect(self.applyTransformationButton, qt.SIGNAL('clicked()'), self.applyTransformation)
		self.connect(self.refreshTransformationButton, qt.SIGNAL('clicked()'), self.refreshTransformationsList)

		# We display XSLT transformation options only if we have the required librairies
		try:
			import libxslt
			import libxml2
			layout.addLayout(buttonLayout)
		except ImportError:
			log("Unable to import libxslt and libxml2 modules : XSLT report plugin can not be used")
			layout.addWidget(qt.QLabel("Unable to import libxslt and libxml2 modules : XSLT report plugin can not be used"))
			layout.addWidget(qt.QLabel("Please install libxml2-python package for your python/OS versions."))
			pass

		# The text view
		self.textView = qt.QTextEdit()
		self.textView.setReadOnly(1)
		font = qt.QFont("courier", 8)
		font.setFixedPitch(True)
		self.textView.setFont(font)
		self.textView.setLineWrapMode(qt.QTextEdit.NoWrap)
		
		layout.addWidget(self.textView)
		
		self.setLayout(layout)
		
		self.refreshTransformationsList()

	def refreshTransformationsList(self):
		"""
		Reload available transformations and repopulate the combo box.
		"""
		self.transformationComboBox.clear()

		settings = qt.QSettings()
		self.xsltPath = settings.value('plugins/%s/xsltpath' % PLUGIN_ID, qt.QVariant(".")).toString()
		
		d = qt.QDir(self.xsltPath)
		d.setNameFilters([ "*.xsl", "*.xslt" ])
		d.setSorting(qt.QDir.Name)
		for transfo in d.entryList():
			self.transformationComboBox.addItem(transfo)

	def applyTransformation(self):
		if self.transformationComboBox.currentText().isEmpty():
			return

		try:
			f = open(self.xsltPath.toAscii() + '/' + self.transformationComboBox.currentText().toAscii())
			xslt = f.read()
			f.close()
		except Exception, e:
			log("Unable to read XSLT file: " + str(e))
			return

		transient = WTransientWindow("Log Viewer", self)
		transient.showTextLabel("Applying XSLT...")
		xml = '<?xml version="1.0" encoding="utf-8"?><root>' + str(self.xml.toUtf8()) + '</root>'
		try:
			import libxslt
			import libxml2
			xmlDoc = libxml2.parseDoc(xml)
			xsltDoc = libxml2.parseDoc(xslt)
			style = libxslt.parseStylesheetDoc(xsltDoc)
			transformedDoc = style.applyStylesheet(xmlDoc, None)
			transformedXml = style.saveResultToString(transformedDoc)
			style.freeStylesheet()
			#xsltDoc.freeDoc() -- freeStylesheet does it ???
			transformedDoc.freeDoc()
			xmlDoc.freeDoc()
		except Exception, e:
			log("Unable to apply XSLT to log: " + str(e))
			transient.hide()
			transient.setParent(None) # enable garbage collecting of the transient window
			return
			
		transient.hide()
		transient.setParent(None) # enable garbage collecting of the transient window
		if transformedXml.find("<html", 0, 50) == -1: #should be enhanced...
			self.textView.setPlainText(transformedXml)
		else:
			self.textView.setHtml(transformedXml)

	def onEvent(self, domElement):
		# Accumulate the events into pure txt form.
		domElement.save(qt.QTextStream(self.xml), 0)
	
	def displayLog(self):
		pass
	
	def clearLog(self):
		self.xml = qt.QString()
		self.textView.clear()


class WXsltLogViewConfiguration(Plugin.WPluginConfiguration):
	def __init__(self, parent = None):
		Plugin.WPluginConfiguration.__init__(self, parent)
		self.__createWidgets()

	def __createWidgets(self):
		"""
		The model is in the saved settings.
		"""
		self.xlstPathLineEdit = qt.QLineEdit()
		self.xlstPathLineEdit.setMinimumWidth(150)
		self.browseDirectoryButton = qt.QPushButton("...")
		self.connect(self.browseDirectoryButton, qt.SIGNAL('clicked()'), self.browseDirectory)
		layout = qt.QVBoxLayout()
		layout.addWidget(qt.QLabel("Search XSLT files (.xslt) in directory:"))
		optionLayout = qt.QHBoxLayout()
		optionLayout.addWidget(self.xlstPathLineEdit)
		optionLayout.addWidget(self.browseDirectoryButton)
		layout.addLayout(optionLayout)

		self.setLayout(layout)

	def browseDirectory(self):
		xsltPath = qt.QFileDialog.getExistingDirectory(self, "XSLT files directory", self.xlstPathLineEdit.text())
		if not xsltPath.isEmpty():
			self.xlstPathLineEdit.setText(os.path.normpath(unicode(xsltPath)))

	def displayConfiguration(self):
		path = "plugins/%s" % PLUGIN_ID
		# Read the settings
		settings = qt.QSettings()
		xsltPath = settings.value(path + '/xsltpath', qt.QVariant(qt.QString(os.path.normpath(qt.QApplication.instance().get('qtheliumpath'))))).toString()
		self.xlstPathLineEdit.setText(xsltPath)

	def saveConfiguration(self):
		"""
		Update the data model.
		"""
		settings = qt.QSettings()
		path = "plugins/%s" % PLUGIN_ID
		settings.setValue(path + '/xsltpath', qt.QVariant(self.xlstPathLineEdit.text()))
		return True

	def checkConfiguration(self):
		"""
		Check the data model, return 1 if OK, 0 if not.
		"""
		return True


PluginManager.registerPluginClass("XSLT", PLUGIN_ID, WXsltLogView, WXsltLogViewConfiguration, version = VERSION, description = DESCRIPTION, author = AUTHOR)

