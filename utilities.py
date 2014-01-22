__author__ = 'Aran'
import time
from phue import Bridge

class BulbState:
    def __init__(self, id, cmd):
        self.id = id
        self.cmd = cmd

class HueCommand:
    def __init__(self, duration, states):
        self.b = Bridge('********')
        self.duration = duration
        self.states = states

    def get_states(self, ids):
        lights =[]
        for light_id in ids:
            is_on = self.b.get_light(light_id, 'on')
            bri = self.b.get_light(light_id, 'bri')
            hue = self.b.get_light(light_id, 'hue')
            lights.append({'id': light_id, 'on': is_on, 'hue': hue, 'bri': bri})
        return lights

    def execute(self):
        # set hue bulbs
        self.b.connect()
        # Get a dictionary with the light ids as the key
        # lights = self.b.get_light_objects('id')

        for state in self.states:
            try:
                self.b.set_light(state.id, state.cmd)
            except Exception as e:
                print e.message
                continue

        time.sleep(self.duration)

