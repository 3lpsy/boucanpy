#!/usr/bin/env python2

from burp import IBurpExtender, ITab
from javax.swing.table import AbstractTableModel
from java.util import ArrayList
from java.lang import Runnable
from java.awt import Dimension
from javax import swing
import threading
import sys
import json
from urlparse import urlparse
from StringIO import StringIO
from httplib import HTTPResponse

try:
    from exceptions_fix import FixBurpExceptions
except ImportError:
    pass

callbacks = None
helpers = None

class FakeSocket():
    def __init__(self, response_str):
        self._file = StringIO(response_str)
    def makefile(self, *args, **kwargs):
        return self._file

class PyRunnable(Runnable):
    def __init__(self, target, *args, **kwargs):
        self.target = target
        self.args = args
        self.kwargs = kwargs

    def run(self):
        self.target(*self.args, **self.kwargs)

class ApiClient(object):
    def __init__(self, api_url, api_token):
        self._api_url = api_url
        self._api_token = api_token

    def get_zones(self):
        url = urlparse(self.url('/zone'))
        # print "Building request"
        request = self.build_request("get", url, self._api_token)
        # print "Hostname: " + str(self.hostname())
        # print "Port: " + str(self.port())
        # print "HTTPS?: " + str(self.is_https())
        # print "Invoking request"
        try:
            response = callbacks.makeHttpRequest(self.service(), request)
            status = int(response.getStatusCode())
            return self.get_json(response)['zones']

        except:
            print "HTTP Error. Could not get Zones"
        return []

    def build_request(self, meth, url, token):
        requestString = StringIO()
        requestString.write(meth.upper())
        requestString.write(" ")
        requestString.write(url.path)
        requestString.write(" HTTP/1.1\r\n")
        requestString.write("HOST: ")
        requestString.write(str(url.hostname))
        requestString.write("\r\n")
        requestString.write("User-Agent: Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.28) Gecko/00000000 Firefox/30.0.00\r\n")
        requestString.write('Accept: application/json\r\n')
        if token:
            requestString.write('Authorization: Bearer ')
            requestString.write(str(token))
            requestString.write("\r\n")

        requestString.write('\r\n\r\n')
        # print "Request: " + str(requestString.getvalue())
        Request = map(lambda x: ord(x), requestString.getvalue())
        requestString.close()
        return Request

    def get_json(self, response):
        res_str = str(helpers.bytesToString(response.getResponse()))
        source = FakeSocket(res_str)
        res_obj = HTTPResponse(source)
        res_obj.begin()
        print "Reading response object"
        return json.loads(res_obj.read())

    def url(self, path):
        return self._api_url + path

    def port(self):
        port = self.parsed_url().port
        if port:
            return int(port)
        elif self.parsed_url().scheme == 'https':
            return 443
        else:
            return 80
    def is_https(self):
        return self.parsed_url().scheme == 'https'

    def hostname(self):
        hostname = self.parsed_url().hostname
        if hostname:
            return hostname
        print "No hostname on parsed url. using netloc"
        return self.parsed_url().netloc

    def parsed_url(self):
        return urlparse(self._api_url)

    def service(self):
        return helpers.buildHttpService(str(self.hostname()), self.port(), self.is_https())

class BurpExtender(IBurpExtender, ITab):
    def registerExtenderCallbacks(self, _callbacks):
        global callbacks
        global helpers
        callbacks = _callbacks
        self._callbacks = _callbacks
        helpers = callbacks.getHelpers()
        self._helpers = helpers
        sys.stdout = callbacks.getStdout()
        self._callbacks.setExtensionName("BountyDNS")
        self._panel = self.buildPanel()
        self.loadZones()

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

        print 'Adding Update Button'
        boxHorizontal = swing.Box.createHorizontalBox()
        updateConfButton = swing.JButton('Update Configuration', actionPerformed=self.updateConfEvent)
        boxHorizontal.add(updateConfButton)
        boxVertical.add(boxHorizontal)

        self._zones = []
        print 'Creating Zones Output Box'
        boxHorizontal = swing.Box.createHorizontalBox()
        boxHorizontal.add(swing.JLabel("Loaded Zones (Output)"))
        boxVertical.add(boxHorizontal)
        boxHorizontal = swing.Box.createHorizontalBox()
        self._zonesLoaded = swing.JTextArea()
        zonesLoaded = swing.JScrollPane(self._zonesLoaded)
        zonesLoaded.setPreferredSize(Dimension(250,125))
        boxHorizontal.add(zonesLoaded)
        boxVertical.add(boxHorizontal)

        self._payloads = []
        print 'Creating Payloads Output Box'
        boxHorizontal = swing.Box.createHorizontalBox()
        boxHorizontal.add(swing.JLabel("Submitted Payloads (Output)"))
        boxVertical.add(boxHorizontal)
        boxHorizontal = swing.Box.createHorizontalBox()
        self._payloadsSubmitted = swing.JTextArea()
        payloadsSubmitted = swing.JScrollPane(self._payloadsSubmitted)
        payloadsSubmitted.setPreferredSize(Dimension(250,125))
        boxHorizontal.add(payloadsSubmitted)
        boxVertical.add(boxHorizontal)

        print 'Adding Vertical Box to Panel...'
        panel.add(boxVertical)
        return panel

    def updateConfEvent(self, button):
        self.updateConf()

    def updateConf(self):
        api_url = self._apiUrl.text
        self.saveApiUrl(api_url)
        api_token = self._apiToken.text
        self.saveApiToken(api_token)
        self.loadZonesLater()

    def loadZonesLater(self):
        print "Starting loadZones in thread"
        thread = threading.Thread(target=self.loadZones, args=())
        thread.start()

    def loadZones(self):
        api_url = self._apiUrl.text
        api_token = self._apiToken.text
        if api_url and api_token:
            print "Requesting zones from api"
            zones = self.api().get_zones()
            self._zones = zones
            print "Clearing loaded zones"
            self._zonesLoaded.setText("")
            for i in range(len(zones)):
                zone = zones[i]
                domain = str(zone['domain'])
                print "Appending zone " + domain
                self._zonesLoaded.append(domain)
                if len(zones) > 1 and i != (len(zones) - 1):
                    self._zonesLoaded.append("\r\n")
            print "Zones loaded"
        else:
            print 'Zones not loaded. No API Token or URL'
        return ''

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

    def api(self):
        api_url = self._apiUrl.text
        api_token = self._apiToken.text
        print "Building API Client"
        return ApiClient(api_url, api_token)

# Always at the end
try:
    FixBurpExceptions()
except:
    pass
