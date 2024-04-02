import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from timeit import default_timer as timer
import pandas as pd
import time

def log_error(message:str, log=None):
    if log is not None:
        log.error(message)
    else:
        print(message)
        


# Login API
def version(base_url, log=None, session=None):
    if session is None:
        session = requests.Session()
    r = session.get(base_url+"/info/version", verify=False, timeout=60)
    
    if r.status_code != requests.codes.ok:
        log_error('ping failed', log)
        return False
    
    return True

def login(base_url, username='demo', password='password', log=None, session=None):

    
    if session is None:
        session = requests.Session()
    # login and get token 

    r = session.post(base_url+"/login", data={'username': username, 'password': password}, verify=False, timeout=60)
    
    if r.status_code != requests.codes.created:
        log_error("Login failed", log)
        return
    
    return r.json()

def logout(base_url, session_token, log=None, session=None):

    if session is None:
        session = requests.Session()
    # logout  
    r = session.delete(base_url+"/login", data={'session_token': session_token}, verify=False, timeout=60)
    if r.status_code != requests.codes.no_content:
        log_error("Logout failed", log)
        return
    
# Device API

def get_gateways(base_url, session_token, log=None, session=None):
    if session is None:
        session = requests.Session()
    """ Return list of devices """
    r = session.get(base_url+"/devicemanager", data={'session_token': session_token}, verify=False, timeout=60)
    
    if r.status_code != requests.codes.ok:
        log_error('get_gateways failed', log)
        return []
    devices = r.json()
    return devices

# Time recording API

def get_recordings_by_device(base_url, session_token, deviceHostId, deviceId, start, end, log=None, session=None):
    
    if session is None:
        session = requests.Session()

    r = session.get(base_url+"/timerecording/recordings", data={'session_token': session_token, 'deviceHostId':deviceHostId, 'deviceId':deviceId, 'start':start, 'end':end}, verify=False, timeout=60)
    if r.status_code != requests.codes.ok:
        log_error(f"get_reccording_by_device Failed, status code: {r.status_code}, reason:{r.reason}", log)
        return []
    recordings = r.json()
    return recordings

def raw_data_by_channel_v2(base_url, session_token,  deviceHostId, deviceId, recording_id, channel=1, log=None, session=None):
    
    if session is None:
        session = requests.Session()
    
    r = session.get(base_url+"/timerecording/recording/channel/raw/v2", data={'session_token': session_token, 'recordingId':recording_id, 'deviceHostId':deviceHostId, 'deviceId':deviceId, 'channel':channel}, verify=False, timeout=60)
    if r.status_code != requests.codes.ok:
        log_error(f"raw_data_by_channel_v2 Failed, status code: {r.status_code}, reason: {r.reason}", log)
        return None
    raw = r.json()
    return raw


def raw_data_by_channel(base_url, session_token,  deviceHostId, deviceId, recording_id, channel=1, log=None, session=None):
    
    if session is None:
        session = requests.Session()
    
    r = session.get(base_url+"/timerecording/recording/channel/raw", data={'session_token': session_token, 'recordingId':recording_id, 'deviceHostId':deviceHostId, 'deviceId':deviceId, 'channel':channel}, verify=False, timeout=60)
    if r.status_code != requests.codes.ok:
        log_error(f"raw_data_by_channel Failed, status code: {r.status_code}, reason:{r.reason}", log)
        return None
    raw = r.json()
    return raw

def parameter_dataset(base_url, session_token,  deviceHostId, deviceId, recording_id, log=None, session=None):
    
    if session is None:
        session = requests.Session()
    
    r = session.get(base_url+"/timerecording/recording/parameters", data={'session_token': session_token, 'recordingId':recording_id, 'deviceHostId':deviceHostId, 'deviceId':deviceId}, verify=False, timeout=60)
    if r.status_code != requests.codes.ok:
        log_error(f"parameter_dataset Failed, status code: {r.status_code}, reason:{r.reason}", log, session=None)
        return None
    raw = r.json()
    return raw
def statusflags_dataset(base_url, session_token,  deviceHostId, deviceId, recording_id, log=None, session=None):
    
    if session is None:
        session = requests.Session()
    
    r = session.get(base_url+"/timerecording/recording/statusflags", data={'session_token': session_token, 'recordingId':recording_id, 'deviceHostId':deviceHostId, 'deviceId':deviceId}, verify=False, timeout=60)
    if r.status_code != requests.codes.ok:
        log_error(f"parameter_dataset Failed, status code: {r.status_code}, reason:{r.reason}", log)
        return None
    raw = r.json()
    return raw

def delete_recording(base_url, session_token,  deviceHostId, deviceId, recording_id, log=None, session=None):
    
    if session is None:
        session = requests.Session()
    
    r = session.post(base_url+"/timerecording/recording/delete", data={'session_token': session_token, 'recordingId':recording_id, 'deviceHostId':deviceHostId, 'deviceId':deviceId}, verify=False, timeout=60)
    if r.status_code != requests.codes.ok:
        log_error(f"delete_recording Failed, status code: {r.status_code}, reason:{r.reason}", log)
        return False
    return True
def start_stream(base_url, session_token,  deviceHostId, log=None, session=None):
    
    if session is None:
        session = requests.Session()
    
    r = session.post(base_url+"/devicemanager/remote_start_recording", data={'session_token': session_token, 'deviceHostId':deviceHostId}, verify=False, timeout=60)
    if r.status_code != requests.codes.ok:
        log_error(f"start_stream Failed, status code: {r.status_code}, reason:{r.reason}", log)
        return False
    return True
def gateway_system_time(base_url, session_token,  deviceHostId, log=None, session=None):
    
    if session is None:
        session = requests.Session()
    
    r = session.get(base_url+"/devicemanager/get_remote_configuration_page", data={'session_token': session_token, 'deviceHostId':deviceHostId, 'page':'system'}, verify=False, timeout=60)
    if r.status_code != requests.codes.ok:
        log_error(f"get_remote_configuration_page, status code: {r.status_code}, reason:{r.reason}", log)
        return None
    raw = r.json()
    return raw['system_time']

def gateway_reset(base_url, session_token,  deviceHostId, level, timeout=20, log=None, session=None):
    
    if session is None:
        session = requests.Session()
    
    r = session.post(base_url+"/devicemanager/remote_reset", data={'session_token': session_token, 'deviceHostId':deviceHostId, 'timeout':timeout, 'level':level}, verify=False, timeout=60)
    if r.status_code != requests.codes.ok:
        log_error(f"remote_reset, status code: {r.status_code}, reason:{r.reason}", log)
        return False
    return True
    
def meausure_time_diff2(base_url, session_token,  deviceHostId, log=None, session=None):
    
    now = pd.Timestamp.utcnow()
    # wait for second shift
    time.sleep(1.0- now.microsecond/1e6)
    now = pd.Timestamp.utcnow()
    
    start = timer()
    res = gateway_system_time(base_url, session_token, deviceHostId, log, session)
    end = timer()
    if res is None:
        return None
    gateway_time = pd.to_datetime(res, utc=True)
    roundtrip = end-start
    time_diff = (gateway_time-now).total_seconds()

    if time_diff > 0:
        time_diff_withtout_roundtrip = time_diff - roundtrip
    else:
        time_diff_withtout_roundtrip = time_diff + roundtrip
        
    log.info(f'{deviceHostId}, system time: {now:%H:%M:%S.%f}, gateway time: {gateway_time:%H:%M:%S.%f}, round trip: {roundtrip}, diff: {time_diff}, without roundtrip: {time_diff_withtout_roundtrip}')
    return time_diff_withtout_roundtrip

def meausure_time_diff(base_url, session_token,  deviceHostId, log=None, session=None):
     
    offsets = []
    for n in range(3):

        now = pd.Timestamp.utcnow()
        # wait for second shift
        time.sleep(1.0- now.microsecond/1e6)
        t0 = pd.Timestamp.utcnow()
    
        res = gateway_system_time(base_url, session_token, deviceHostId, log, session)
        t3 = pd.Timestamp.utcnow()
        if res is None:
            continue
        t1 = pd.to_datetime(res, utc=True)
        t2 = t1
        offset = ((t1-t0).total_seconds() + (t2-t3).total_seconds())/2
        roundtrip = (t3-t0).total_seconds()-(t2-t1).total_seconds()
        offsets.append(offset)
        log.info(f'n: {n}, {deviceHostId}, system time: {t0:%H:%M:%S.%f}, gateway time: {t1:%H:%M:%S.%f}, round trip: {roundtrip}, offset: {offset}')

    return sum(offsets)/len(offsets)

def humanize_devicehost(deviceHostId:str)->str:
    return deviceHostId.split('.')[0]