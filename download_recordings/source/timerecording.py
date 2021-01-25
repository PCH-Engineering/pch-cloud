import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import pprint
import json
import server_paths as url
import os

def get_recording_tree(host, session_token):
    r = requests.get(url.backend(host)+"/timerecording/tree", data={'session_token': session_token}, verify=False)
    if r.status_code != requests.codes.ok:
        print(get_recording_tree.__name__ + " Failed", r.status_code, r.reason)
        return
    tree = r.json()
    return tree

def query_recordings(host, session_token, device, year, month, count):

    query = {
        "selection": [
            {
                "device":device,
                "month":month,
                "year":year,

            },
        ],
        "page":1,
        "numberOfItems":count
    }

    r = requests.get(url.backend(host)+"/timerecording/recording/query", data={'session_token': session_token, "queryString":json.dumps(query)}, verify=False)
    
    if r.status_code != requests.codes.ok:
        print(query_recordings.__name__ + " Failed", r.status_code, r.reason)
        return
    
    recordings = r.json()
    return recordings

def supported_export_formats(host,token):
    r = requests.get(url.backend(host)+"/timerecording/supported_export_formats", verify=False)
    if r.status_code != requests.codes.ok:
        print(supported_export_formats.__name__ + " Failed", r.status_code, r.reason)
        return
    formats = r.json()
    return formats

def export(host, session_token, deviceHostId, deviceId, recording_id, formatExt, path, overwrite=False):

    filename = recording_id.split('.')[-1]
    local_path = os.path.join(path, host,"tdms", deviceHostId, deviceId)
    if not os.path.isdir(local_path): 
        os.makedirs(local_path)
    local_filename =os.path.join(local_path, filename+"."+formatExt)
    
    if not overwrite and os.path.isfile(local_filename):
        return local_filename, False

    # NOTE the stream=True parameter below
    with requests.post(url.backend(host)+"/timerecording/recording/export", data={'session_token': session_token, 'recordingId':recording_id,'deviceHostId':deviceHostId, 'deviceId':deviceId, 'format':formatExt}, stream=True, verify=False) as r:
        r.raise_for_status()
        
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
                    # f.flush()
    return local_filename, True

def get_recordings_by_device(host, session_token, deviceHostId, deviceId, start, end ):
    r = requests.get(url.backend(host)+"/timerecording/recordings", data={'session_token': session_token, 'deviceHostId':deviceHostId, 'deviceId':deviceId, 'start':start, 'end':end}, verify=False)
    if r.status_code != requests.codes.ok:
        print(get_reccording_by_device.__name__ + " Failed", r.status_code, r.reason)
        return
    recordings = r.json()
    return recordings


def raw_data_all_channels(host, session_token, deviceHostId, deviceId, recording_id):
    r = requests.get(url.backend(host)+"/timerecording/recording/raw", data={'session_token': session_token, 'recordingId':recording_id,'deviceHostId':deviceHostId, 'deviceId':deviceId}, verify=False)
    if r.status_code != requests.codes.ok:
        print(raw_data_all_channels.__name__ + " Failed", r.status_code, r.reason)
        return
    raw = r.json()
    return raw

def raw_data_by_channel(host, session_token,  deviceHostId, deviceId, recording_id, channel=1):
    r = requests.get(url.backend(host)+"/timerecording/recording/channel/raw", data={'session_token': session_token, 'recordingId':recording_id, 'deviceHostId':deviceHostId, 'deviceId':deviceId, 'channel':channel}, verify=False)
    if r.status_code != requests.codes.ok:
        print(raw_data_by_channel.__name__ + " Failed", r.status_code, r.reason)
        return None
    raw = r.json()
    return raw

def parameter_dataset(host, session_token,  deviceHostId, deviceId, recording_id):
    r = requests.get(url.backend(host)+"/timerecording/recording/parameters", data={'session_token': session_token, 'recordingId':recording_id, 'deviceHostId':deviceHostId, 'deviceId':deviceId}, verify=False)
    if r.status_code != requests.codes.ok:
        print(parameter_dataset.__name__ + " Failed", r.status_code, r.reason)
        return None
    raw = r.json()
    return raw
    #OQ
def get_spectrum_names(host,session_token):    
    r=requests.get(url.backend(host)+"/TimeRecording/recording/dataprocessing/setup/spectra",data={'session_token': session_token})
    if r.status_code != requests.codes.ok:
        print(parameter_dataset.__name__ + " Failed", r.status_code, r.reason)
        return None
    spectra_names=r.json()
    return spectra_names  
    #OQ 
def download_spectrum(host, session_token,  deviceHostId, deviceId, recording_id, spectrum_setup_name, channel=1,path="..\\spectra",overwrite=False):
    print(recording_id)
    #recordingid is a sort of timestamp
    filename = recording_id.split('.')[-1]
    
    local_path = os.path.join(path,host,spectrum_setup_name, deviceHostId, deviceId,"channel_"+str(channel+1))
    formatExt="json"
    if not os.path.isdir(local_path): 
        os.makedirs(local_path)

    local_filename =os.path.join(local_path, filename+"."+formatExt)  
    #print( local_filename)  
    if (not overwrite) and os.path.isfile(local_filename):
        return local_filename, False
    
    #Make request package
    data={'session_token': session_token, 'deviceHostId':deviceHostId, 'deviceId':deviceId,'recordingId':recording_id,'channel':channel,'name':spectrum_setup_name}
    print(data)
    #Send the request
    r = requests.get(url.backend(host)+"/TimeRecording/recording/dataprocessing/spectrum", data=data, verify=False)
    if r.status_code != requests.codes.ok:
          print(parameter_dataset.__name__ + " Failed", r.status_code, r.reason)
          return local_filename+"FAIL" ,False
    spectra=r.json()
    with open(local_filename, 'w') as f:
        f.write(json.dumps(spectra))
        f.close()   
    return local_filename, True 
  


def delete_recording(host, session_token,  deviceHostId, deviceId, recording_id):
    r = requests.post(url.backend(host)+"/timerecording/recording/delete", data={'session_token': session_token, 'recordingId':recording_id, 'deviceHostId':deviceHostId, 'deviceId':deviceId}, verify=False)
    if r.status_code != requests.codes.ok:
        print(delete_recording.__name__ + " Failed", r.status_code, r.reason)
        return False
    return True