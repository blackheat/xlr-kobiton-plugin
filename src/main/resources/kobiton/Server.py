import sys

request = HttpRequest({ 'url': configuration.url }, configuration.username, configuration.apiKey)
response = request.get('/v1/devices')
kobiStatus = response.getStatus()

request = HttpRequest({'url': configuration.remoteServer})
response = request.get('/ping')
remoteStatus = response.getStatus()

errorLog = []
# Check response status code, if is different than 200 exit with error code
if kobiStatus != 200:
    errorLog.append('Invalid Kobiton credentials')

if remoteStatus != 200:
    errorLog.append('Cannot connect to remote server')

if errorLog != []:
    sys.exit(errorLog)