import json

with open('../config/hosts.json') as f:
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