# Python script for "Basic" dashboard UI

Simple dashboard UI for showing a list of scalar values.

## Install

The installation steps may be different on different platforms. However the basic priciple is the same.

1. Create virtual environment 
```
py -m venv env
```

2. Activate virtual environment
```
.\env\Scripts\activate
```

3. Install requirements listed in requirements.txt

```
pip3 install -r requirements.txt
```

## Setting up
In order for the script to run - 2 files are required. The files must be locatated in the same folder as the script

1. **hosts.json** for setting up urls to backend-services

    ```
    {
        "pchcloud": {
            "backend": "https://pchcloud.pch-engineering.dk/backend",
            "usermanager": "https://pchcloud.pch-engineering.dk/usermanager",
            "devicemanager": "https://pchcloud.pch-engineering.dk/devicemanager"
        },

        "local": {
            "backend": "http://localhost:5000/api",
            "usermanager": "http://localhost:5020/api",
            "devicemanager": "http://localhost:5030/api" 
        },
        
    }
    ```
    
    The example has two known hosts. 
    
    * **"pchcloud"** can be used if the data is download from https://pchcloud.pch-engineering.dk 
    * **"local"** can be used if the backend-services are running on the same pc as the script is executed.

    More hosts can be added by inserting a new section, for example

    ```
     "mypc": {
            "backend": "http://192.168.1.105:5000/api",
            "usermanager": "http://192.168.1.105:5020/api",
            "devicemanager": "http://192.168.1.105:5030/api" 
        },
    ``` 

    To the **host.json**

     ```
    {
        "pchcloud": {
            "backend": "https://pchcloud.pch-engineering.dk/backend",
            "usermanager": "https://pchcloud.pch-engineering.dk/usermanager",
            "devicemanager": "https://pchcloud.pch-engineering.dk/devicemanager"
        },
        "local": {
            "backend": "http://localhost:5000/api",
            "usermanager": "http://localhost:5020/api",
            "devicemanager": "http://localhost:5030/api" 
        },
        "mypc": {
            "backend": "http://192.168.1.105:5000/api",
            "usermanager": "http://192.168.1.105:5020/api",
            "devicemanager": "http://192.168.1.105:5030/api" 
        },
    
    }
    
    ```
    This can be usefull is the backend-services is running on another pc. 



2. **config.json** is for configurtion settings

    ```
    {
    "host":"pchcloud",
    "username": "demo",
    "password": "password",
    "data": [
        {
            "deviceHostId":"Demo IoT.ub",
            "deviceId":"PCH1232-2017190014",
            "scalars": [
                {
                    "name":"P index 1",
                    "scalarIndex":1
                }
            ]
        },
        {
            "deviceHostId":"Demo IoT.ub",
            "deviceId":"PCH1232-2017190015",
            "scalars": [
                {
                    "name":"P 2",
                    "scalarIndex":0
                }
            ]
        }
    ]
    }
    ```
    
    * "host" sets the server connections from the list of known hosts in the **hosts.json* file
    * "username" and "password" is the account login. If connecting to local the default username is 'local' and the password is 'pass'
    * "data", is the list of scalars that are displayed. It is a list of devices, identified by deviceHostId and deviceId and for each device item a list of scalars: with display        name and scalar index.  


## Execute python script
py ./app.py






    



