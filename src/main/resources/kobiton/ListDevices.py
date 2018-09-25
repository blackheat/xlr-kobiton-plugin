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


def get_devices_list():
    serialized_devices_list = {}
    try:
      devices_list = get_all_devices()

      devices_list = merge_list(group_options, devices_list)
      devices_list = get_available_devices(devices_list)
      devices_list = device_platform_filter(platform_options, devices_list)
      devices_list = device_name_filter(model, devices_list)

      serialized_devices_list = serialize_devices(devices_list)
    except Exception:
      print 'Failed to get devices list'
    finally:
      return serialized_devices_list

  
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


def merge_list(group_options, devices_list=[]):
  classified_list = []

  for option in group_options:
    if option != 'favoriteDevices':
      for item in devices_list[option]:
        if group_options['favoriteDevices']:
          if item['isFavorite']:
            item.update({'group': option})
            classified_list.append(item)
        elif group_options[option]:
          item.update({'group': option})

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


def serialize_devices(devices_list=[]):
  serialized_list = {}

  for item in devices_list:
    device_data = str().join([item['deviceName'], ' | ', item['platformName'], ' | ', item['platformVersion'], ' | ', item['group']])

    serialized_device = {
      item['udid']: device_data
    }

    serialized_list.update(serialized_device)

  return serialized_list


devices = get_devices_list()

