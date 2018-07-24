import sys

params = { 'url': configuration.url, 'proxyHost': configuration.proxyHost, 'proxyPort': configuration.proxyPort }

request = HttpRequest(params, configuration.username, configuration.password)
response = request.get('/v1/devices')

# check response status code, if is different than 200 exit with error code
if response.getStatus() != 200:
    sys.exit(1)

