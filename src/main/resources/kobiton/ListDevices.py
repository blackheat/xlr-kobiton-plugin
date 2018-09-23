import json
import re
import urllib2

kobiton_api_server = kobitonServer['url']
username = kobitonServer['username']
api_key = kobitonServer['password']

# Return list in XebiaLabs
devices = {}


def create_basic_authentication_token():
    s = username + ":" + api_key
    return "Basic " + s.encode("base64").rstrip()


def get_devices_list():
    devices_list = get_all_devices_list()

    devices_list = merge_devices(devices_list, isCloud, isPrivate, isFavorite)
    devices_list = device_available_filter(devices_list)
    devices_list = device_platform_filter(isAndroid, isiOs, devices_list)
    devices_list = device_name_filter(model, devices_list)
    serialized_devices_list = serialize_devices(devices_list)

    return serialized_devices_list


def get_all_devices_list():
    auth_token = create_basic_authentication_token()
    url = kobiton_api_server + '/devices'
    header = {
        "Content-Type": "application/json",
        "Authorization": auth_token
    }
    request = urllib2.Request(url, headers=header)
    response = urllib2.urlopen(request)
    body = response.read()
    return json.loads(body)


def device_available_filter(devices_list=None):
    if devices_list is None:
        return []

    filtered_list = []

    for item in devices_list:
        if item['isOnline'] and not item['isBooked']:
            filtered_list.append(item)

    return filtered_list


def device_platform_filter(android, ios, devices_list=None):
    if devices_list is None:
        return []

    filtered_list = []

    for item in devices_list:
        if android:
            if item['platformName'] == 'Android':
                filtered_list.append(item)
        if ios:
            if item['platformName'] == 'iOS':
                filtered_list.append(item)

    return filtered_list


def device_name_filter(filter_string=None, devices_list=None):
    if devices_list is None:
        return []

    filtered_list = []

    if filter_string is None:
        filter_string = ""

    devices_name = filter_string.split(',')
    for item in devices_list:
        for name in devices_name:
            if re.search(name, item['deviceName'], re.IGNORECASE):
                filtered_list.append(item)
                break

    return filtered_list


def merge_devices(devices_list, cloud, private, favorite):
    classified_list = []

    if cloud:
        for item in devices_list['cloudDevices']:
            if item not in classified_list:
                classified_list.append(item)
    if private:
        for item in devices_list['privateDevices']:
            if item not in classified_list:
                classified_list.append(item)
    if favorite:
        for item in devices_list['favoriteDevices']:
            if item not in classified_list:
                classified_list.append(item)

    return classified_list


def serialize_devices(devices_list=None):
    if devices_list is None:
        return {}

    serialized_list = {}

    for item in devices_list:
        device_id = item['id']
        device_data = {
            'deviceName': str(item['deviceName']),
            'platformName': str(item['platformName']),
            'udid': str(item['udid'])
        }

        serialized_device = {
            str(device_id): str(device_data)
        }

        serialized_list.update(serialized_device)

    return serialized_list


devices = get_devices_list()

