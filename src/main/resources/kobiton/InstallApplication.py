import json


def getUrl():
    param = {
        'url': 'https://api.kobiton.com/v1/apps/uploadUrl'
    }
    request = HttpRequest(param, 'undefined', 'a79fa165-6347-43a7-9cbb-10447a59f982')
    content = {
        'filename': 'appdemo.apk'
    }

    response = request.post('', json.dumps(content), contentType='application/json')

    return json.loads(response.getResponse())['url']


def uploadS3(application_url):
    param = {
        'url': application_url
    }

    request = HttpRequest(param)

    file_input = open("/appdemo.apk", "rb")

    response = request.put("", file_input, contentType='application/octet-stream')
    print response.getResponse()
    print response.getStatus()
    print response.errorDump()


app_url = getUrl()
uploadS3(app_url)

