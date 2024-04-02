# Python script for trigger time stream and download time recordings in json format
When the script is running it will automatic scan for new RAW time stream data files and save in json format.
If trigger stream is enabled the script will trigger time stream recording on all attached/online and enabled etherbridges.
The script run in an infite loop. 

# Setup 

The Setup steps may be different on different platforms. However the basic priciple is the same.

1. Create virtual environment 
    ```
    python3 -m venv env
    ```

2. Activate virtual environment
    ```
    .\env\bin\activate
    ```

3. Install requirements listed in requirements.txt

    ```
    pip3 install -r requirements.txt
    ```
4. Run script 
    ```
    python3 .\src\run.py
    ```
    To get help for command arguments  
    ```
    python3 .\src\run.py --help
    ```
    The script may be execute on a different pc than the edge pc. In that case the host argument must be set
    
    ```
    python3 .\src\trigger_stream.py
    ```


