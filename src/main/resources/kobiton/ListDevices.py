import json
import re
import urllib2
import copy

kobiton_api_server = kobitonServer['url']
username = kobitonServer['username']
api_key = kobitonServer['apiKey']

group_options = {
  'cloudDevices': isCloud,
  'privateDevices': isPrivate,
  'favoriteDevices': isFavorite
}

platform_options = {
  'Android': isAndroid,
  'iOS': isiOs
}

# Return list in XebiaLabs
devices = {}


def get_devices_list():
  filtered_list = None
  try:
    devices_list = get_all_devices()
    filtered_list = devices_filter(group_options, devices_list)
  except Exception as e:
    print e
    print 'Failed to get devices list'
  finally:
    return filtered_list


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

  
def devices_filter(group_options, devices_list=[]):
  classified_list = {}

  for option in group_options:
    for device in devices_list[option]:
      if device_matches_filter(device):
        if classified_list.get(device['udid']) is None:
          classified_list.update(serialize_device(device))

  return classified_list


def device_matches_filter(device):
  return device_is_available(device) and device_has_matching_platform(device) and device_contains_name(device)


def device_is_available(device):
  return device['isOnline'] and not device['isBooked']


def device_has_matching_platform(device):
  return platform_options[device['platformName']]


def device_contains_name(device):
  devices_name = model.split(',')

  for name in devices_name:
    if re.search(name, device['deviceName'], re.IGNORECASE):
      return True

  return False


def serialize_device(device):
  device_data = str().join([device['deviceName'], ' | ', device['platformName'], ' | ', device['platformVersion'], ' | ', categorize_device(device)])
  serialized_device = {
    device['udid']: str(device_data)
  }

  return serialized_device


def categorize_device(device):
  if device['isMyOrg']:
    return "privateDevices"
  return "cloudDevices"


devices = get_devices_list()