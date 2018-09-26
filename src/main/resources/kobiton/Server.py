import sys
import urllib2
import base64

errorLog = []
def ping(params={}, headers={}):
    try:
        request = urllib2.Request(params['url'], None, headers)
        urllib2.urlopen(request)
    except Exception as ex:
        errorLog.append("Error while connecting to {}: {}".format(params['server'], ex))

ping({
    "url": configuration.url + '/v1/devices',
    "server": "Kobiton"
}, {
    "Authorization": 'Basic %s' % base64.b64encode('%s:%s' % (configuration.username, configuration.apiKey))
})

ping({
    "url": configuration.remoteServer + '/ping',
    "server": "Remote Server"
})

if errorLog != []:
    sys.exit(errorLog)