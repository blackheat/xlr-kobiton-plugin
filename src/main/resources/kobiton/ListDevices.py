import json
import re
import urllib2
import copy

kobiton_api_server = kobitonServer['url']
username = kobitonServer['username']
api_key = kobitonServer['password']

# kobiton_api_server = "https://api.kobiton.com/v1"
# username = "undefined"
# api_key = "a79fa165-6347-43a7-9cbb-10447a59f982"
# isCloud = False
# isPrivate = True
# isFavorite = True
# isAndroid = True
# isiOs = True
# model = ""

# Return list in XebiaLabs
devices = {}


def create_basic_authentication_token():
    s = username + ":" + api_key
    return "Basic " + s.encode("base64").rstrip()


def get_devices_list():
    serialized_devices_list = {}
    try:
        devices_list = get_all_devices_list()

        devices_list = merge_devices(devices_list, isCloud, isPrivate, isFavorite)
        devices_list = device_available_filter(devices_list)
        devices_list = device_platform_filter(isAndroid, isiOs, devices_list)
        devices_list = device_name_filter(model, devices_list)

        serialized_devices_list = serialize_devices(devices_list)
    except Exception as e:
        print 'Failed to get devices list'
        print 'Log : ' + e
        sys.exit(1)
    finally:
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
        return None

    filtered_list = []

    for item in devices_list:
        if item['isOnline'] and not item['isBooked']:
            filtered_list.append(item)

    return filtered_list


def device_platform_filter(android, ios, devices_list=None):
    if devices_list is None:
        return None

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
        return None

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
    
    if favorite:
        device_classification(devices_list['favoriteDevices'], classified_list, devices_list)

    if cloud:
        device_classification(devices_list['cloudDevices'], classified_list, devices_list)

    if private:
        device_classification(devices_list['privateDevices'], classified_list, devices_list)

    return classified_list

def device_classification(list_to_be_classified, classified_list=None, devices_list=None):
    if classified_list is None:
        classified_list=[]

    if devices_list is None:
        return []

    # Defined attributes
    cloud_attribute = {
        "group": "Cloud"
    }
    private_attribute = {
        "group": "In-House"
    }
    other_attribute = {
        "group": "Other"
    }

    for item in list_to_be_classified:
        if find_device_by_id(item['id'], classified_list) is None:
            if find_device_by_id(item['id'], devices_list['cloudDevices']) is not None:
                item.update(cloud_attribute)
            elif find_device_by_id(item['id'], devices_list['privateDevices']) is not None:
                item.update(private_attribute)
            else:
                item.update(other_attribute)
            classified_list.append(item)
    return classified_list


def find_device_by_id(device_id, devices_list=[]):
    if devices_list is None:
        return None
   
    for a in devices_list:
        if a['id'] == device_id:
            return a
    
    return None


def serialize_devices(devices_list=None):
    if devices_list is None:
        return {}

    serialized_list = {}

    for item in devices_list:
        device_data = str().join([item['deviceName'], ' | ', item['platformName'], ' | ', item['platformVersion'], ' | ', item['group']])

        serialized_device = {
            item['udid']: device_data
        }

        serialized_list.update(serialized_device)

    return serialized_list


devices = get_devices_list()

