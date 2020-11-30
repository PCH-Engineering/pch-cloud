# import pchcloud api
import usermanager
import scalars
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
            scalarItems = scalars.get_device_scalars(host, token, deviceHostId, deviceId)
            
            if scalarItems is None or len(scalarItems) is 0:
                continue
            # get the scalar data
            print(f'Get scalars, device: {deviceHostId}.{deviceId}, start: {start}, end: {end}, number of scalars: {len(scalarItems)}')
            for scalarInfo in scalarItems:
                # get scalar time series
                scalar_timeserie = scalars.get_scalar_timeserie(host, token, deviceHostId, deviceId, scalarInfo['scalarId'], start, end)
                
                # do something with the data
                numberOfValues = scalar_timeserie['length']
                unit = scalarInfo['unit']
                scalarName = scalarInfo['name']
                
                print(f'Got data, device: {deviceHostId}.{deviceId}, scalar: {scalarName}, unit: {unit}, length: {numberOfValues} ')

                # get scalar alarm limits
                alarmlimits_timeseries = scalars.get_alarmlimits_timeseries(host, token, deviceHostId, deviceId, scalarInfo['scalarId'], start, end)
                if len(alarmlimits_timeseries) > 0 : 
                    # do something with the alarm limits.
                    print(f'Got alarm limits, device: {deviceHostId}.{deviceId}, scalar: {scalarName}, number of alarm limits: {len(alarmlimits_timeseries)}')


