# import pchcloud api
import usermanager
import timerecording
import device

import pprint
import json
from datetime import datetime, timedelta

import dateutil.parser
import os

pp = pprint.PrettyPrinter(indent=4)


if __name__ == "__main__":
   
    # gets all time recordings from the last 5 days
    # get current time 
    
    with open('config.json') as config_file:
        config = json.load(config_file)

        print("Configuration: ")
        pp.pprint(config)

        host = config["host"]
        delete_on_server = config['delete_on_server']
        query_passed_days = config['query_passed_days']
        # set timerange  
        end = datetime.utcnow()
        start = end - timedelta(days=query_passed_days)
    
        # login 
        session = usermanager.login(host, config["username"], config["password"])
        token = session['token']

        # get devices

        devices = device.get_device_list(host, token)
        for device in devices:

            deviceHostId = device['deviceHostId']
            deviceId = device['deviceId']
            # get recordings in interval
            recordings = timerecording.get_recordings_by_device(host, token, deviceHostId, deviceId, start, end)
            
            if recordings is None or len(recordings) == 0:
                print(f'No recordings for device: {deviceHostId}.{deviceId}', "start: ", start, "end:", end)
                continue
            # get the recording data
            print(f'Get recordings, device: {deviceHostId}.{deviceId}, start: {start}, end: {end}, recordings: {len(recordings)}')
            for recordingInfo in recordings:
                numberOfChannels = recordingInfo['numberOfChannels']
                parameters = recordingInfo['parameters']
                print('parameters')
                for parameter in parameters:
                    print(f'name: {parameter["name"]}, value: {parameter["value"]} {parameter["unit"]}')
                for channel in range(numberOfChannels):
                    # get data
                    data = timerecording.raw_data_by_channel(host, token, deviceHostId, deviceId, recordingInfo['id'], channel+1)
                    # do something with the data
                    numberOfSamples = len(data['samples'])
                    unit = data['unit']


                    print(f'Got data, device: {deviceHostId}.{deviceId}, channel: {channel+1}, numberOfSamples: {numberOfSamples},  unit: {unit}')
            
                # should we delete the file on the server ?
                if delete_on_server :
                    if not timerecording.delete_recording(host, token, deviceHostId, deviceId, recordingInfo['id']):
                        id = recordingInfo['id']
                        print(f'Failed to delete recording, device: {deviceHostId}.{deviceId}, id: {id}')
