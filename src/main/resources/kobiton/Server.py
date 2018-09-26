import sys

params = { 'url': configuration.url }

request = HttpRequest(params, configuration.username, configuration.apiKey)
response = request.get('/devices')

# check response status code, if is different than 200 exit with error code
if response.getStatus() != 200:
    sys.exit(1)
