# Python scripts for downloading scalar data and status data for all devices within a spefic time range

The download_scalars.py is an example of an python script for automatated download of scalar data and scalar alarm limits for all devices within a time range

1. The script will logon to pchcloud or local server.

2. Query for devices

3. For each device it will query for all scalar values

4. For each scalar value it will get the scalar timeserie in a specified time range: from 'now'-1day to now

5. For each scalar the alarm limits in the same time range will also be fetched.

The download_status_flags.py is an example of an python script for automatated download of status flags data for all devices within a time range

1. The script will logon to pchcloud or local server.

2. Query for devices

3. For each device it will query for all status flags

4. For each status flag it will get the status flag timeserie in a specified time range: from 'now'-1day to now


## Install 
install requirements listed in requirements.txt

```
pip install -r requirements.txt
```


## Setting up
In order for the script to run - 2 files are required. The files most be put in the same folder as the script

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
        "query_passed_days": 1
    }
    ```
    
    * "host" sets the server connections from the list of known hosts in the **hosts.json* file
    * "username" and "password" is the account login. If connecting to local the default username is 'local' and the password is 'pass'
    * "delete_on_server", if true recordings WILL BE DELETED on the server 
    * "query_passed_days", query time range number of days back from current time


## Execute python script
py ./download_scalars.py

or

py ./download_status_flags.py



