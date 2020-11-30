import pyglet
import os
import usermanager
import device as device_api
import json
import pprint
from datetime import datetime, timedelta
pp = pprint.PrettyPrinter(indent=4)


window = pyglet.window.Window(resizable=True, fullscreen=True)

with open('config.json') as config_file:
        config = json.load(config_file)

        print("Configuration: ")
        pp.pprint(config)

        # login 
        host = config["host"]
        session = usermanager.login(host, config["username"], config["password"])
        token = session['token']
        labels = []
        label_names = []
        
        for item in config['data']:
            for scalarItem in item['scalars']:
                label_names.append(scalarItem['name'])
        ystep = (window.height-10) // len(label_names)
        y_pos =  window.height-5
        for name in label_names:
            labels.append(pyglet.text.Label(name+': ',
                        font_name='Arial',
                        font_size=36,
                        x=10,
                        y=y_pos ,
                        color = (0,255,0,100),
                        anchor_x='left',
                        anchor_y='top'))
            y_pos-=ystep
        

def update(dt):
    index = 0
    for item in config['data']:

        device_data = device_api.get_device_data(host, token,  item['deviceHostId'], item['deviceId'])
        for scalarItem in item['scalars']:
            scalar_data = device_data['scalars'][scalarItem['scalarIndex']]
            
            labels[index].text = "{}: {:6.2f} {}".format(label_names[index], scalar_data['value'], scalar_data['unit'])
            labels[index].color = (0,255,0,255)
            index+=1

@window.event
def on_resize(width, height):

    y_step = (window.height-10) // len(label_names)
    y_pos =  window.height-5
    for label in labels:
    # Keep text vertically centered in the window
        label.y = y_pos
        y_pos-=y_step

@window.event
def on_draw():
    window.clear()
    for label in labels:
        label.draw()


pyglet.clock.schedule_interval(update, 5.0) # update at 1Hz


pyglet.app.run()