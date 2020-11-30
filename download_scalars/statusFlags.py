import requests
import pprint
import json
import server_paths as url

def get_device_statusFlags(host, session_token, deviceHostId, deviceId):
    r = requests.get(url.backend(host)+"/statusFlag/statusflags_by_device", data={'session_token': session_token,'deviceHostId':deviceHostId, 'deviceId':deviceId})
    if r.status_code != requests.codes.ok:
        print(get_device_statusFlags.__name__ + " Failed", r.status_code, r.reason)
        return
    scalars = r.json()
    return scalars

def get_statusFlag_timeserie(host, session_token, deviceHostId, deviceId, statusFlagId, start, end):

    r = requests.get(url.backend(host)+"/statusFlag/get_statusflag_timeserie", data={
        'session_token': session_token, 
        'deviceHostId':deviceHostId,
        'deviceId':deviceId,
        'statusFlagId':statusFlagId,
        'from':start,
        'to':end,
    })
    
    if r.status_code != requests.codes.ok:
        print(get_statusFlag_timeserie.__name__ + " Failed", r.status_code, r.reason)
        return
    
    data = r.json()
    return data
