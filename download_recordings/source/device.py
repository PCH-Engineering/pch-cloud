import requests
import pprint
import server_paths as url

def get_device_list(host, session_token):

    # login and get token 
    r = requests.get(url.backend(host)+"/device/devices", data={'session_token': session_token}, verify=False)
    print("get_device_list", r.status_code, r.reason)

    if r.status_code != requests.codes.ok:
        print('get_device_list failed')
        return
    devices = r.json()
    return devices
