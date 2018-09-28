from org.apache.http.client.methods import HttpPut
from org.apache.http.entity import ByteArrayEntity
from org.apache.http.impl.client import HttpClients
import json
import urllib2
import ntpath

api_server = kobitonServer['url']
username = kobitonServer['username']
api_key = kobitonServer['apiKey']

options = {
    'filename': ntpath.basename(appPath),
    'app_id': appId,
    'package_name': appPackageName
}


def loader():
    if options['app_id'] is None or options['app_id'] == '':
        if options['package_name'] is not None:
            options['app_id'] = get_id_from_package_name(options['package_name'])

    url_data = get_url()
    option = {
        'file_path': str(appPath),
        'url': url_data['url']
    }
    upload_s3(option)
    upload_kobiton(url_data['appPath'])


def create_basic_authentication_token():
    s = username + ":" + api_key
    return "Basic " + s.encode("base64").rstrip()


def get_id_from_package_name(package_name):
    header = {
        'content-type': 'application/json',
        'authorization': create_basic_authentication_token()
    }

    request = urllib2.Request(url=api_server + '/v1/apps/', headers=header)

    try:
        response = urllib2.urlopen(request)
        data = response.read()
        applications = json.loads(data)

        for application in applications['apps']:
            for version in application['versions']:
                native_properties = version['nativeProperties']
                if native_properties['package'] == package_name:
                    return str(application['id'])

        raise Exception
    except Exception:
        return ''


def get_url():
    content = {
        'filename': options['filename']
    }

    header = {
        'content-type': 'application/json',
        'authorization': create_basic_authentication_token()
    }

    if options['app_id'] is not None and options['app_id'] != '':
        content.update({'appId': options['app_id']})

    request = urllib2.Request(url=api_server + '/v1/apps/uploadUrl', data=json.dumps(content), headers=header)

    response = urllib2.urlopen(request)
    data = response.read()

    return json.loads(data)


def upload_s3(upload_options={}):
    binary = open(upload_options['file_path'], "rb")
    http_put = HttpPut(upload_options['url'])
    http_put.setHeader('content-type', 'application/octet-stream')
    http_put.setHeader('x-amz-tagging', 'unsaved=true')
    http_put.setEntity(ByteArrayEntity(binary.read()))
    http_client = HttpClients.createDefault()
    response = http_client.execute(http_put)
    print response.getStatusLine()
    print response.getStatusLine().getStatusCode()


def upload_kobiton(app_path):
    content = {
        'appPath': app_path,
        'filename': options['filename']
    }

    header = {
        'content-type': 'application/json',
        'authorization': create_basic_authentication_token()
    }

    request = urllib2.Request(url=api_server + '/v1/apps', data=json.dumps(content), headers=header)

    response = urllib2.urlopen(request)
    data = response.read()

    return json.loads(data)


loader()
