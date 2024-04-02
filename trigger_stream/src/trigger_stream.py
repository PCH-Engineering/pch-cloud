import pch_iot_api as pch
import json
import logging
import os
import time
import pandas as pd
from multiprocessing.dummy import Pool
import requests

session = requests.Session()
log = logging.getLogger("trigger_stream")
log.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s [%(levelname)s]: %(message)s')
ch.setFormatter(formatter)
# add the handlers to the logger
log.addHandler(ch)

pool = Pool(10)

def get_gateways_filtered(base_url, token, log, session=None):

    gateways = pch.get_gateways(base_url, token, log, session)

    # save gateways to json file
    json.dump(gateways, open("./data/gateways.json", "w"))
    
    return [gateway for gateway in gateways if gateway['enabled'] and gateway['online'] and gateway['type'] == 'Etherbridge']

def scan_timestreams(config, log, session=None):
    scan_window = pd.Timedelta(config['scan_since'])
    if not pch.version(config["base_url"], log, session):
        log.error("API not reachable")
        return {}
    token = pch.login(config["base_url"], config["username"], config["password"], log, session)['token']
    gateways = get_gateways_filtered(config["base_url"], token, log, session)
    
    # save gateways to json file
    json.dump(gateways, open("./data/gateways_filtered.json", "w"))
    
    recordings = {}

    end = pd.Timestamp.utcnow()
    start = end-scan_window
    for gateway in gateways: 
        

        deviceHostId = gateway['deviceHostId']
        devices = gateway['devices']
        for device in devices:

            # dump device to json file
            json.dump(device, open(f"./data/device_{device['deviceId']}.json", "w"))
            deviceId = device['deviceId']

            fullId =  f"{deviceHostId}.{deviceId}" 
            recordings[fullId] = pch.get_recordings_by_device(config["base_url"], token, deviceHostId, deviceId,start, end, log, session)
            log.info(f"device: {fullId}, recordings: {len(recordings[fullId])}")

    pch.logout(config["base_url"], token, session)
    # save recordings to json file
    json.dump(recordings, open("./data/recordings.json", "w")) 

    return recordings

def save_timestreams(recordings, config, log, session):
    token = pch.login(config["base_url"], config["username"], config["password"], log, session)['token']
    
    # fetch raw data and save to json file
    for gateway in recordings.keys():
        for recording in recordings[gateway]:

            # get all channels
            channels = recording['channels']
            for channel in channels.keys():
                channelNumber = int(channel)+1 # channel is 0 based and channel number is 1 based

                raw = pch.raw_data_by_channel_v2(config["base_url"], token, recording['deviceHostId'], recording['deviceId'], recording['id'], channelNumber, log=log, session=session)
                
                # save raw data to json file
                json.dump(raw, open(f"./raw/{recording['deviceHostId']}_{recording['id']}_ch_{channelNumber}.json", "w"))


    pch.logout(config["base_url"], token, session)


def start_timestream(config, log, session=None):
    
    timeskew_max = pd.Timedelta(config['timeskew_max']).total_seconds()
    token = pch.login(config["base_url"], config["username"], config["password"], log, session)['token']
    gateways = get_gateways_filtered(config["base_url"], token, log, session)
    futures_meas = []

    # measure time diff between etherbridges (dont request stream if time diff is too large)

    for gateway in gateways: 
        deviceHostId = gateway['deviceHostId']
        futures_meas.append(pool.apply_async(pch.meausure_time_diff2, [config["base_url"], token, deviceHostId, log, session]))
        #time_diff = pch.meausure_time_diff2(config["base_url"], token, deviceHostId, log, session)
        
    time_diffs = [future.get() for future in futures_meas]
    log.info(f'time diffs, {time_diffs}')
    do_request_stream = len(time_diffs) >= 1
    if len(time_diffs) > 1:

        timeskew = max([abs(x-time_diffs[0]) for x in time_diffs if x is not None])
        if timeskew > timeskew_max:
            do_request_stream = False
            # do resync
            log.info(f'max time skew exeeded - request resync , time skew: {timeskew}, time skew max: {timeskew_max}')

            for gateway in gateways:

                deviceHostId = gateway['deviceHostId']
                pch.gateway_reset(config["base_url"], token, deviceHostId, 3, log=log)
            

    if do_request_stream:
        futures = []
        for gateway in gateways: 
            deviceHostId = gateway['deviceHostId']
            log.info(f'request stream, {pch.humanize_devicehost(deviceHostId)}')
            futures.append(pool.apply_async(pch.start_stream, [config["base_url"], token, deviceHostId, log, session]))
        
        log.info(f'request stream, {[future.get() for future in futures]}') 
  
    pch.logout(config["base_url"], token, session)
    
    return do_request_stream

config = {
    "base_url": "http://localhost:5000/api",
    "username": "admin",
    "password": "admin",
    "timeskew_max":"15s",
    "loop_sleep": "60s",
    "scan_since":"10m", 
}

def init():
    if not os.path.exists("./data"):
        os.makedirs("./data")
    if not os.path.exists("./raw"):
        os.makedirs("./raw")

if __name__ == "__main__":
    triggers = 0
    last_requesttime = None
    init()
    try:
        while True:

            # scan for timestreams
            recordings = scan_timestreams(config, log, session)
            # save timestreams
            save_timestreams(recordings, config, log, session)
            # triigger new timestream
            if start_timestream(config, log, session ):
                triggers += 1
                last_requesttime = pd.Timestamp.utcnow()
                log.info(f"triggers: {triggers}, last trigger: {last_requesttime}")
                
            log.info(f"wait {pd.Timedelta(config['loop_sleep']).total_seconds()} sec ...")
            time.sleep(pd.Timedelta(config['loop_sleep']).total_seconds()) 

    except KeyboardInterrupt:
        pass