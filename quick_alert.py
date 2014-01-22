__author__ = 'Aran'

import os
import win32com
import pyttsx
import pythoncom
from xml.dom import minidom
import urllib
import time
from utilities import *

def cal_alert(event_name, time_till):
    pythoncom.CoInitialize()
    # Checks for light on before alerting
    kill = True
    for light in HueCommand(0, []).get_states([1, 2, 3]):
        if light['on'] == True:
            kill = False
    if kill:
        return
    # Todo may remove the on lights check...
    engine = pyttsx.init()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate-10)
    engine.say('Uhh run... your event '+str(event_name)+'... starts in '+str(time_till)+'... minutes')
    HueCommand(0, [BulbState(1, {'alert' : 'select'}),
                   BulbState(2, {'alert' : 'select'}),
                   BulbState(3, {'alert' : 'select'})]).execute()
    engine.runAndWait()
