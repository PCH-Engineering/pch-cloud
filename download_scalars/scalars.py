import requests
import pprint
import json
import server_paths as url

def get_device_scalars(host, session_token, deviceHostId, deviceId):
    r = requests.get(url.backend(host)+"/scalars/scalars_by_device", data={'session_token': session_token,'deviceHostId':deviceHostId, 'deviceId':deviceId})
    if r.status_code != requests.codes.ok:
        print(get_device_scalars.__name__ + " Failed", r.status_code, r.reason)
        return
    scalars = r.json()
    return scalars

def get_scalar_timeserie(host, session_token, deviceHostId, deviceId, scalarId, start, end):

    r = requests.get(url.backend(host)+"/scalars/get_scalar_timeserie", data={
        'session_token': session_token, 
        'deviceHostId':deviceHostId,
        'deviceId':deviceId,
        'scalarId':scalarId,
        'from':start,
        'to':end,
    })
    
    if r.status_code != requests.codes.ok:
        print(get_scalar_timeserie.__name__ + " Failed", r.status_code, r.reason)
        return
    
    data = r.json()
    return data

def get_alarmlimits_timeseries(host, session_token, deviceHostId, deviceId, scalarId, start, end ):
    r = requests.get(url.backend(host)+"/scalars/get_alarmlimits_timeseries", data={
        'session_token': session_token, 
        'deviceHostId':deviceHostId,
        'deviceId':deviceId,
        'scalarId':scalarId,
        'from':start,
        'to':end
    })
    
    if r.status_code != requests.codes.ok:
        print(get_scalar_alarmlimits.__name__ + " Failed", r.status_code, r.reason)
        return
    
    data = r.json()
    return data

