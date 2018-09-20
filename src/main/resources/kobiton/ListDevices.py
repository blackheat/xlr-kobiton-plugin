import json
import re
import urllib2

# kobiton_api_server = kobitonServer['url']
# username = kobitonServer['username']
# api_key = kobitonServer['password']

kobiton_api_server = 'https://api.kobiton.com'
username = 'undefined'
api_key = 'a79fa165-6347-43a7-9cbb-10447a59f982'
model = 'iphone galaxy'
isFavorite = True
isPrivate = False
isCloud = True
isAndroid = True
isiOs = False
devices = []


def create_basic_authentication_token():
    s = username + ":" + api_key
    return "Basic " + s.encode("base64").rstrip()


def get_all_devices_list():
    auth_token = create_basic_authentication_token(username, api_key)
    url = kobiton_api_server
    headers = {
        "Content-Type": "application/json",
        "Authorization": auth_token
    }
    request = urllib2.Request(url, headers=headers)
    response = urllib2.urlopen(request)
    body = response.read()
    return json.loads(body)


def get_devices_list():
    all_list = get_all_devices_list()
    filtered_list = []

    if isFavorite:
        for item in all_list['favoriteDevices']:
            if item['isOnline']:
                for name in devices:
                    if re.search(name, item['deviceName'], re.IGNORECASE):
                        filtered_list.append(serialize_device_format(item, 'favoriteDevices'))

    if isCloud:
        for item in all_list['cloudDevices']:
            if item['isOnline']:
                for name in devices:
                    if re.search(name, item['deviceName'], re.IGNORECASE):
                        filtered_list.append(serialize_device_format(item, 'cloudDevices'))

    if isPrivate:
        for item in all_list['privateDevices']:
            if item['isOnline']:
                for name in devices:
                    if re.search(name, item['deviceName'], re.IGNORECASE):
                        filtered_list.append(serialize_device_format(item, 'privateDevices'))

    return filtered_list


def serialize_device_format(device, device_group):
    data = {
        'deviceName': str(device['deviceName']),
        'platformName': str(device['platformName']),
        'udid': str(device['udid']),
        'deviceGroup': device_group
    }
    return data

