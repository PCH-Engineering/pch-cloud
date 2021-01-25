import usermanager
import timerecording
import device as dev
#import matplotlib.pyplot as plt
import pprint
import json
from datetime import datetime, timedelta
import time
import dateutil.parser
import os

def get_spectrum(host, token,  selected_device_hostid,spectrum_setup_name,start,end):
    pass   
              
                    

pp = pprint.PrettyPrinter(indent=4)
if __name__ == "__main__":
   
    # gets all time recordings from the last 5 days
    # get current time 
    
    with open('../config/spectrum_config.json') as config_file:
        config = json.load(config_file)
        print("Configuration: ")
        pp.pprint(config)
        host = config["host"]
        delete_on_server = config['delete_on_server']
        query_passed_days = config['query_passed_days']
        download_path = config['download_path']
        spectrum_name=config['spectrum_name']
        selected_device_hostids=config['deviceHostIds']
        selected_devices=config['devices']


        time_delay=config['time_delay']
        download_path=config['download_path']
        #def get_spectrum(host, session_token,  deviceHostId, deviceId, recording_id, spectrum_setup_name, channel=1):
        end = datetime.utcnow()


        start = end - timedelta(days=query_passed_days)
        End=end.isoformat()
        Start=start.isoformat()
        print('start: '+str(start)+'('+Start+' ) end: '+str(end) + ' ('+End+')' )

    

        # login 
        session = usermanager.login(host, config["username"], config["password"])
        token = session['token']
        #get_spectrum(host, token,selected_device_hostid,spectrum_name,start,end)
        cnt=0
        devices = dev.get_device_list(host, token)
        for device in devices:
            deviceHostId = device['deviceHostId']
            deviceId = device['deviceId']
            if selected_devices[0]!='all':
                print('Selecting individual devices is NOT implemented see line 62 in download_spectra (TODO)')

            '''   
            for sel_device in selected_devices:
                if sel_device==deviceId or selected_devices[0]=='all':                  
            '''
            for devicehost in selected_device_hostids:
                if devicehost==deviceHostId or selected_device_hostids[0]=='all':
    
                    print(deviceId)
                                # get recordings in interval
                    recordings = timerecording.get_recordings_by_device(host, token, deviceHostId, deviceId, start, end)
                    
                    for recordingInfo in recordings:                       
                        numberOfChannels = recordingInfo['numberOfChannels']
                        recording_id=recordingInfo['id']
                        parameters = recordingInfo['parameters']
                        #print(parameters)
                        #recordingId=parameters['recordingId']
                        for parameter in parameters:
                            pass
                            #print(f'name: {parameter["name"]}, value: {parameter["value"]} {parameter["unit"]}')                                         

                            
                        for channel in range(numberOfChannels):    
                            cnt=cnt+1    
                            print(host+' '+ token+' '+ deviceHostId+' '+  deviceId+' '+  recording_id+' '+  spectrum_name+' '+ str(channel)+' '+ download_path)
                            print(type(timerecording.download_spectrum))
                            local_filename , is_downloaded = timerecording.download_spectrum(host, token,  deviceHostId, deviceId, recording_id, spectrum_name,channel,download_path)
                            if is_downloaded:
                                print(local_filename+' is downloaded')
                                time.sleep(time_delay)
                                print(cnt)
                            else:
                                print(local_filename+' existed and is not downloaded' )
    
                        if delete_on_server :
                            if not timerecording.delete_recording(host, token, deviceHostId, deviceId, recording_id):
                                id = recordingInfo['id']
                                print(f'Failed to delete recording, device: {deviceHostId}.{deviceId}, id: {id}')


        
    
                    
                    
               
  