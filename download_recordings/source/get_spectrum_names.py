# import pchcloud api
import usermanager
import timerecording
import device

import pprint
import json
from datetime import datetime, timedelta

import dateutil.parser
import os
from  pathlib import Path
parentdir = Path(__file__).parents[1] 
pp = pprint.PrettyPrinter(indent=4)


if __name__ == "__main__":
   
    # gets all time recordings from the last 5 days
    # get current time  
    configfile=parentdir.joinpath('config/spectrum_config.json')
    with open(configfile) as config_file:
        config = json.load(config_file)
        #print("Configuration: ")
        #pp.pprint(config)
        host = config["host"]
        download_path=config['download_path']
        setup_dir=parentdir.joinpath(download_path,host)
        os.makedirs(setup_dir,exist_ok=True)

        delete_on_server = config['delete_on_server']
        query_passed_days = config['query_passed_days']
        # set timerange  
        end = datetime.utcnow()
        start = end - timedelta(days=query_passed_days)
    
        # login 
        session = usermanager.login(host, config["username"], config["password"])
        token = session['token']

        devices = device.get_device_list(host, token)
        devicefile=parentdir.joinpath(download_path,host,'devices.json')
        with open(devicefile,"w") as s:
            s.write(json.dumps(devices))
            s.close()
     
        
        spectrum_total=timerecording.get_spectrum_names(host,token)
        #print(spectrum_total) 
        spectrum_setups=spectrum_total['spectrumSetups']
        spectrumsetups=parentdir.joinpath(download_path,host,'spectrum_setups.json')

        with open(spectrumsetups,"w") as s:
            s.write(json.dumps(spectrum_setups))
            s.close()
        spectrumnames=parentdir.joinpath(download_path,host,'spectrum_names.json')    
      
        name_array=[]
        print('\nSPECTRUM NAMES\n')
        for elm in spectrum_setups:                        
            name_array.append(elm['name'])
            print(elm['name'])
        with open(spectrumnames,"w") as s:
            s.write(json.dumps(name_array))
            s.close()
        print("three .json files are made at for documentation at: \n" + str(devicefile)  +"\n" + str(spectrumsetups) +"\n" + str(spectrumnames) )    
        


   
