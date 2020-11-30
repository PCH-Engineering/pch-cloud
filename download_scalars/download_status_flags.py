# import pchcloud api
import usermanager
import device
import statusFlags

import pprint
import json
from datetime import datetime, timedelta

import dateutil.parser
import os

pp = pprint.PrettyPrinter(indent=4)

if __name__ == "__main__":
   
    # gets all scalars 
    
    with open('config.json') as config_file:
        config = json.load(config_file)

        print("Configuration: ")
        pp.pprint(config)

        host = config["host"]
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
            # get device scalars
            items = statusFlags.get_device_statusFlags(host, token, deviceHostId, deviceId)
            
            if items is None or len(items) == 0:
                continue
            # get the scalar data
            print(f'Get status flags, device: {deviceHostId}.{deviceId}, start: {start}, end: {end}, number of flags: {len(items)}')


            for n, statusFlagInfo in enumerate(items):

                # get scalar time series
                data = statusFlags.get_statusFlag_timeserie(host, token, deviceHostId, deviceId, statusFlagInfo['statusFlagId'], start, end)
                if data is None:
                    continue
                # do something with the data
                numberOfValues = data['length']
                statusFlagName = statusFlagInfo['name']
                if numberOfValues > 0:
                    dataPoints = data['dataPoints'][numberOfValues-1]

                    print(f'{n+1} of {len(items)}, status flag: {statusFlagName}, length: {numberOfValues}, last value: {dataPoints}')
                else:
                    print(f'{n+1} of {len(items)}, status flag: {statusFlagName}, No values')
                

