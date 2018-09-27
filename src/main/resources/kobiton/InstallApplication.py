param = {
    'url': 'https://kobiton-us-east.s3.amazonaws.com/users/32809/apps'
}

request = HttpRequest(param)

with open('/appdemo.apk', 'rb') as finput:
    response = request.put('appdemo-b5a62a90-c223-11e8-bc74-b71de2b2cb30.apk?AWSAccessKeyId=AKIAJ7BONOZUJZ'+
                           'MWR4WQ&Content-Type=application%2Foctet-stream&Expires=1538075126&Signature=CXfh'+
                           'bVS9YHDQO%2Bqk5PX4jH1yd5E%3D&x-amz-acl=private&x-amz-meta-appid=0&x-amz-meta-crea'+
                           'tedby=32809&x-amz-meta-organizationid=294&x-amz-meta-privateaccess=false&x-amz-ta'+
                           'gging=unsaved%3Dtrue',
                           finput,
                           contentType='application/octet-stream')

    print response.getResponse()
    print response.getStatus()
    print response.getHeaders()
    print response.errorDump()


def getUrl():
    param = {
        'url': 'https://api.kobiton.com/v1/apps/uploadUrl'
    }
    request = HttpRequest(param, 'undefined', 'a79fa165-6347-43a7-9cbb-10447a59f982')
    content = {
        'filename': 'appdemo.apk'
    }

