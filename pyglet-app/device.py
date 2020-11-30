import requests
import pprint
import server_paths as url

def get_device_list(host, session_token):

    r = requests.get(url.backend(host)+"/device/devices", data={'session_token': session_token})
    # print("get_device_list", r.status_code, r.reason)

    if r.status_code != requests.codes.ok:
        print('get_device_list failed')
        return
    devices = r.json()
    return devices

def get_device_data(host, session_token, deviceHostId, deviceId):
    r = requests.get(url.backend(host)+"/device/get_device_data", data={'session_token': session_token, 'deviceHostId':deviceHostId, 'deviceId':deviceId})
    # print("get_device_data", r.status_code, r.reason)

    if r.status_code != requests.codes.ok:
        print('get_device_data failed')
        return
    device_data = r.json()
    return device_data