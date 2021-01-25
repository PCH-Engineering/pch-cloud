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
    
    with open('../config/spectrum_config.json') as config_file:
        config = json.load(config_file)
        #print("Configuration: ")
        #pp.pprint(config)
        host = config["host"]
        download_path=config['download_path']
        setup_dir=download_path+"/"+host+"/"
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
        with open(setup_dir+'devices.json',"w") as s:
            s.write(json.dumps(devices))
            s.close()
     
        
        spectrum_total=timerecording.get_spectrum_names(host,token)
        #print(spectrum_total) 
        spectrum_setups=spectrum_total['spectrumSetups']
        with open(setup_dir+'spectrum_names_setup.json',"w") as s:
            s.write(json.dumps(spectrum_setups))
            s.close()
      
        name_array=[]
        print('\nSPECTRUM NAMES\n')
        for elm in spectrum_setups:                        
            name_array.append(elm['name'])
            print(elm['name'])
        with open(setup_dir+'spectrum_names.json',"w") as s:
            s.write(json.dumps(name_array))
            s.close()
        print("three .json files are made at for documentation at " +setup_dir )    
        


   
