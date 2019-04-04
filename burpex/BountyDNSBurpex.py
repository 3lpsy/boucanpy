#!/usr/bin/env python2

from burp import IBurpExtender, ITab
from javax.swing.table import AbstractTableModel
from java.util import ArrayList
from javax import swing
from java.awt import Dimension
import threading
import sys

try:
    from exceptions_fix import FixBurpExceptions
except ImportError:
    pass


class BurpExtender(IBurpExtender, ITab):
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        sys.stdout = callbacks.getStdout()
        self._callbacks.setExtensionName("BountyDNS")
        self._panel = self.buildPanel()
        print "Adding self to Suite Tab"
        self._callbacks.addSuiteTab(self)
        return

    def buildPanel(self):
        print 'Building Panel...'
        panel = swing.JPanel()
        boxVertical = swing.Box.createVerticalBox()

        print 'Creating API URL Label...'
        boxHorizontal = swing.Box.createHorizontalBox()
        boxHorizontal.add(swing.JLabel("Enter API URL"))
        boxVertical.add(boxHorizontal)

        print 'Creating API URL Text Field...'
        boxHorizontal = swing.Box.createHorizontalBox()
        self._apiUrl = swing.JTextField(self.loadApiUrl(), 30)
        boxHorizontal.add(self._apiUrl)
        boxVertical.add(boxHorizontal)

        print 'Creating API Token Label...'
        boxHorizontal = swing.Box.createHorizontalBox()
        boxHorizontal.add(swing.JLabel("Enter API Token"))
        boxVertical.add(boxHorizontal)

        print 'Creating API Token Text Field...'
        boxHorizontal = swing.Box.createHorizontalBox()
        self._apiToken = swing.JTextArea()
        apiTokenOuput = swing.JScrollPane(self._apiToken)
        apiTokenOuput.setPreferredSize(Dimension(250,125))
        self._apiToken.setText(self.loadApiToken())
        self._apiTokenOuput = apiTokenOuput
        boxHorizontal.add(self._apiTokenOuput)
        boxVertical.add(boxHorizontal)

        print 'Adding Save Button'
        boxHorizontal = swing.Box.createHorizontalBox()
        saveConfButton = swing.JButton('Save Configuration', actionPerformed=self.saveConf)
        boxHorizontal.add(saveConfButton)
        boxVertical.add(boxHorizontal)

        print 'Adding Vertical Box to Panel...'
        panel.add(boxVertical)
        return panel

    def saveConf(self, button):
        api_url = self._apiUrl.text
        self.saveApiUrl(api_url)
        api_token = self._apiToken.text
        self.saveApiToken(api_token)

    def getTabCaption(self):
        return "BountyDNS"

    def getUiComponent(self):
        return self._panel

    def loadApiUrl(self):
        return self._callbacks.loadExtensionSetting('api_url')

    def saveApiUrl(self, val):
        return self._callbacks.saveExtensionSetting('api_url', val)

    def loadApiToken(self):
        return self._callbacks.loadExtensionSetting('api_token')

    def saveApiToken(self, val):
        return self._callbacks.saveExtensionSetting('api_token', val)

# Always at the end
try:
    FixBurpExceptions()
except:
    pass
