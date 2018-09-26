import json
import re
import urllib2
import copy

kobiton_api_server = kobitonServer['url']
username = kobitonServer['username']
api_key = kobitonServer['apiKey']

group_options = {
  'cloudDevices': cloudDevices,
  'privateDevices': privateDevices,
  'favoriteDevices': favoriteDevices
}

platform_options = {
  'Android': isAndroid,
  'iOS': isiOs
}

# Return list in XebiaLabs
devices = {}


def create_basic_authentication_token():
  s = username + ":" + api_key
  return "Basic " + s.encode("base64").rstrip()


def get_all_devices():
  auth_token = create_basic_authentication_token()
  url = kobiton_api_server + '/v1/devices'
  header = {
    "Content-Type": "application/json",
    "Authorization": auth_token
  }
  request = urllib2.Request(url, headers=header)
  response = urllib2.urlopen(request)
  body = response.read()
  return json.loads(body)


def get_devices_list():
  devices_list = None
  try:
    devices_list = get_all_devices()
    devices_list = merge_list(group_options, devices_list)
  except Exception:
    print 'Failed to get devices list'
  finally:
    return devices_list

  
def merge_list(group_options, devices_list=[]):
  classified_list = {}

  for option in group_options:
    if group_options[option]:
      devices_list[option] = get_available_devices(devices_list[option])
      devices_list[option] = device_platform_filter(devices_list[option])
      devices_list[option] = device_name_filter(model, devices_list[option])

    for device in devices_list[option]:
      if classified_list.get(device['udid']) is None:
        device = serialize_device(device)
        classified_list.update(device)

  return classified_list


def get_available_devices(devices_list=[]):
  filtered_list = []

  for item in devices_list:
    if item['isOnline'] and not item['isBooked']:
      filtered_list.append(item)

  return filtered_list


def device_platform_filter(platform_options, devices_list=[]):
  filtered_list = []

  for item in devices_list:
    for option in platform_options:
      if platform_options[option]:
        if item['platformName'] == option:
          filtered_list.append(item)

  return filtered_list


def device_name_filter(filter_string="", devices_list=[]):
  filtered_list = []
  devices_name = filter_string.split(',')

  for item in devices_list:
    for name in devices_name:
      if re.search(name, item['deviceName'], re.IGNORECASE):
        filtered_list.append(item)
        break

  return filtered_list


def categorize_device(device):
  if device['isMyOrg']:
    return "privateDevices"
  return "cloudDevices"


def serialize_device(device):
  device_data = str().join([device['deviceName'], ' | ', device['platformName'], ' | ', device['platformVersion'], ' | ', categorize_device(device)])
  serialized_device = {
    device['udid']: device_data
  }

  return serialized_device


devices = get_devices_list()

