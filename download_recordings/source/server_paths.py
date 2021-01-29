import json
#import os
#fn= os.path.abspath(__file__ +  "/../../")
#hostfile =os.path.join(fn,'config/hosts.json')
from pathlib import Path;
parent = Path(__file__).parents[1]
hostfile=parent.joinpath('config/hosts.json')
with open(hostfile) as f:
    hosts = json.load(f)

def service_url(host, service):
    return hosts[host][service]

def backend(host):
    return service_url(host, 'backend')

def usermanager(host):
    return service_url(host, 'usermanager')

def devicemanager(host):
    return service_url(host, 'devicemanager')

if __name__ == "__main__":
    
    
    print("Local:")
    print(backend('local'))
    print(usermanager('local'))
    print(devicemanager('local'))
    
    print("pchcloud:")
    print(backend('pchcloud'))
    print(usermanager('pchcloud'))
    print(devicemanager('pchcloud'))

    print("pchcloud:")
    print(backend('pchcloud2'))
    print(usermanager('pchcloud2'))
    print(devicemanager('pchcloud2'))