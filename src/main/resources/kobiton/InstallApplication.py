import json
import base64


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

    response = request.put("", base64.b64encode(file_input.read()), contentType='application/octet-stream')
    print response.getResponse()
    print response.getStatus()
    print response.errorDump()
# from org.apache.http.client.methods import HttpPut
# from org.apache.http.entity import StringEntity, ByteArrayEntity
# from org.apache.http.impl.client import HttpClients
#
#
# def upload():
#     binary = open("appdemo.apk", "rb")
#     http_put = HttpPut("https://kobiton-us-east.s3.amazonaws.com/users/32809/apps/appdemo-b5a62a90-c223-11e8-bc74-b71de2b2cb30.apk?AWSAccessKeyId=AKIAJ7BONOZUJZMWR4WQ&Content-Type=application%2Foctet-stream&Expires=1538075126&Signature=CXfhbVS9YHDQO%2Bqk5PX4jH1yd5E%3D&x-amz-acl=private&x-amz-meta-appid=0&x-amz-meta-createdby=32809&x-amz-meta-organizationid=294&x-amz-meta-privateaccess=false&x-amz-tagging=unsaved%3Dtrue")
#     http_put.setEntity(ByteArrayEntity(binary.read()))
#     print "Executing request" + str(http_put.getRequestLine())
#
#     http_client = HttpClients.createDefault()
#     response = http_client.execute(http_put)
#     print response
#
# upload()

app_url = getUrl()
uploadS3(app_url)

