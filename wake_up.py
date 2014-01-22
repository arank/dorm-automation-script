__author__ = 'Aran'

import mp3play
from random import choice
from utilities import *
import wx
import threading
import time


GLOBAL_STOP = False

class Experience:
    def __init__(self, sound, show):
        self.filename = sound
        self.state_list = show

    def play(self):
        if self.filename is None:
            for hcmd in self.state_list:
                hcmd.execute()
        else:
            mp3 = mp3play.load(self.filename)
            mp3.play()

            # Let it play till the show ends or song does, then stop it.
            for hcmd in self.state_list:
                if GLOBAL_STOP:
                    break
                hcmd.execute()
                if not mp3.isplaying():
                    return
            mp3.stop()

def intialize_scenes():
    scenes = []
    # Ocean
    scenes.append(Experience(
        r'PATH TO WAKE UP SONG',
        [HueCommand(
            10,
            [BulbState(1, {'on' : False}),
             BulbState(2, {'on' : False}),
             BulbState(3, {'on' : False})]),
        HueCommand(
            3,
            [BulbState(1, {'on' : True, 'bri' : 0, 'sat': 255, 'hue' : 46920}),
             BulbState(2, {'on' : True, 'bri' : 0, 'sat': 100, 'hue' : 12750}),
             BulbState(3, {'on' : True, 'bri' : 0, 'sat': 100, 'hue' : 12750})]),
        HueCommand(
             20,
             [BulbState(1, {'on' : True, 'bri' : 50, 'sat': 255, 'hue' : 46920, 'transitiontime' : 200}),
              BulbState(2, {'on' : True, 'bri' : 50, 'sat': 155, 'hue' : 12750, 'transitiontime' : 200}),
              BulbState(3, {'on' : True, 'bri' : 50, 'sat': 155, 'hue' : 12750, 'transitiontime' : 200})]),
        HueCommand(
             20,
             [BulbState(1, {'on' : True, 'bri' : 100, 'sat': 255, 'hue' : 46920, 'transitiontime' : 200}),
              BulbState(2, {'on' : True, 'bri' : 100, 'sat': 155, 'hue' : 12750, 'transitiontime' : 200}),
              BulbState(3, {'on' : True, 'bri' : 100, 'sat': 155, 'hue' : 12750, 'transitiontime' : 200})]),
        HueCommand(
             20,
             [BulbState(1, {'on' : True, 'bri' : 150, 'sat': 255, 'hue' : 46920, 'transitiontime' : 200}),
              BulbState(2, {'on' : True, 'bri' : 150, 'sat': 155, 'hue' : 12750, 'transitiontime' : 200}),
              BulbState(3, {'on' : True, 'bri' : 150, 'sat': 155, 'hue' : 12750, 'transitiontime' : 200})]),
        HueCommand(
             15,
             [BulbState(1, {'on' : True, 'bri' : 200, 'sat': 255, 'hue' : 46920, 'transitiontime' : 150}),
              BulbState(2, {'on' : True, 'bri' : 200, 'sat': 155, 'hue' : 12750, 'transitiontime' : 150}),
              BulbState(3, {'on' : True, 'bri' : 200, 'sat': 155, 'hue' : 12750, 'transitiontime' : 150})]),
        HueCommand(
             15,
             [BulbState(1, {'on' : True, 'bri' : 254, 'sat': 255, 'hue' : 46920, 'transitiontime' : 150}),
              BulbState(2, {'on' : True, 'bri' : 254, 'sat': 155, 'hue' : 12750, 'transitiontime' : 150}),
              BulbState(3, {'on' : True, 'bri' : 254, 'sat': 155, 'hue' : 12750, 'transitiontime' : 150})])]
    ))
    # Forest
    scenes.append(Experience(
        r'PATH TO WAKE UP SONG',
        [HueCommand(
            10,
            [BulbState(1, {'on' : False}),
             BulbState(2, {'on' : False}),
             BulbState(3, {'on' : False})]),
        HueCommand(
            3,
            [BulbState(1, {'on' : True, 'bri' : 0, 'sat': 255, 'hue' : 25500}),
             BulbState(2, {'on' : True, 'bri' : 0, 'sat': 100, 'hue' : 12750}),
             BulbState(3, {'on' : True, 'bri' : 0, 'sat': 100, 'hue' : 12750})]),
        HueCommand(
             20,
             [BulbState(1, {'on' : True, 'bri' : 50, 'sat': 255, 'hue' : 25500, 'transitiontime' : 200}),
              BulbState(2, {'on' : True, 'bri' : 50, 'sat': 155, 'hue' : 12750, 'transitiontime' : 200}),
              BulbState(3, {'on' : True, 'bri' : 50, 'sat': 155, 'hue' : 12750, 'transitiontime' : 200})]),
        HueCommand(
             20,
             [BulbState(1, {'on' : True, 'bri' : 100, 'sat': 255, 'hue' : 25500, 'transitiontime' : 200}),
              BulbState(2, {'on' : True, 'bri' : 100, 'sat': 155, 'hue' : 12750, 'transitiontime' : 200}),
              BulbState(3, {'on' : True, 'bri' : 100, 'sat': 155, 'hue' : 12750, 'transitiontime' : 200})]),
        HueCommand(
             20,
             [BulbState(1, {'on' : True, 'bri' : 150, 'sat': 255, 'hue' : 25500, 'transitiontime' : 200}),
              BulbState(2, {'on' : True, 'bri' : 150, 'sat': 155, 'hue' : 12750, 'transitiontime' : 200}),
              BulbState(3, {'on' : True, 'bri' : 150, 'sat': 155, 'hue' : 12750, 'transitiontime' : 200})]),
        HueCommand(
             15,
             [BulbState(1, {'on' : True, 'bri' : 200, 'sat': 255, 'hue' : 25500, 'transitiontime' : 150}),
              BulbState(2, {'on' : True, 'bri' : 200, 'sat': 155, 'hue' : 12750, 'transitiontime' : 150}),
              BulbState(3, {'on' : True, 'bri' : 200, 'sat': 155, 'hue' : 12750, 'transitiontime' : 150})]),
         HueCommand(
             15,
             [BulbState(1, {'on' : True, 'bri' : 254, 'sat': 255, 'hue' : 25500, 'transitiontime' : 150}),
              BulbState(2, {'on' : True, 'bri' : 254, 'sat': 155, 'hue' : 12750, 'transitiontime' : 150}),
              BulbState(3, {'on' : True, 'bri' : 254, 'sat': 155, 'hue' : 12750, 'transitiontime' : 150})])]
    ))
    # Orchestra
    scenes.append(Experience(
        r'PATH TO WAKE UP SONG',
        [HueCommand(
            10,
            [BulbState(1, {'on' : False}),
             BulbState(2, {'on' : False}),
             BulbState(3, {'on' : False})]),
        HueCommand(
            3,
            [BulbState(1, {'on' : True, 'bri' : 0, 'sat': 255, 'hue' : 56100}),
             BulbState(2, {'on' : True, 'bri' : 0, 'sat': 100, 'hue' : 12750}),
             BulbState(3, {'on' : True, 'bri' : 0, 'sat': 100, 'hue' : 12750})]),
        HueCommand(
             20,
             [BulbState(1, {'on' : True, 'bri' : 50, 'sat': 255, 'hue' : 56100, 'transitiontime' : 200}),
              BulbState(2, {'on' : True, 'bri' : 50, 'sat': 155, 'hue' : 12750, 'transitiontime' : 200}),
              BulbState(3, {'on' : True, 'bri' : 50, 'sat': 155, 'hue' : 12750, 'transitiontime' : 200})]),
        HueCommand(
             20,
             [BulbState(1, {'on' : True, 'bri' : 100, 'sat': 255, 'hue' : 56100, 'transitiontime' : 200}),
              BulbState(2, {'on' : True, 'bri' : 100, 'sat': 155, 'hue' : 12750, 'transitiontime' : 200}),
              BulbState(3, {'on' : True, 'bri' : 100, 'sat': 155, 'hue' : 12750, 'transitiontime' : 200})]),
        HueCommand(
             20,
             [BulbState(1, {'on' : True, 'bri' : 150, 'sat': 255, 'hue' : 56100, 'transitiontime' : 200}),
              BulbState(2, {'on' : True, 'bri' : 150, 'sat': 155, 'hue' : 12750, 'transitiontime' : 200}),
              BulbState(3, {'on' : True, 'bri' : 150, 'sat': 155, 'hue' : 12750, 'transitiontime' : 200})]),
        HueCommand(
             15,
             [BulbState(1, {'on' : True, 'bri' : 200, 'sat': 255, 'hue' : 56100, 'transitiontime' : 150}),
              BulbState(2, {'on' : True, 'bri' : 200, 'sat': 155, 'hue' : 12750, 'transitiontime' : 150}),
              BulbState(3, {'on' : True, 'bri' : 200, 'sat': 155, 'hue' : 12750, 'transitiontime' : 150})]),
         HueCommand(
             15,
             [BulbState(1, {'on' : True, 'bri' : 254, 'sat': 255, 'hue' : 56100, 'transitiontime' : 150}),
              BulbState(2, {'on' : True, 'bri' : 254, 'sat': 155, 'hue' : 12750, 'transitiontime' : 150}),
              BulbState(3, {'on' : True, 'bri' : 254, 'sat': 155, 'hue' : 12750, 'transitiontime' : 150})])]
    ))
    return scenes

def initialzie_scene(major_hue, minor_hue):
    # Pretty lights
    wake_it =[]

    for i in range(100):

        wake_it.append(HueCommand(
             1,
             [BulbState(1, {'on' : True, 'bri' : 1, 'sat': 255, 'hue' : major_hue, 'transitiontime' : 10}),
              BulbState(2, {'on' : True, 'bri' : 1, 'sat': 155, 'hue' : minor_hue, 'transitiontime' : 10}),
              BulbState(3, {'on' : True, 'bri' : 1, 'sat': 155, 'hue' : minor_hue, 'transitiontime' : 10})]))

    return  wake_it


def initialize_fuck():
    # Get The Fuck Up
    fuck_it =[]

    for i in range(38):
        fuck_it.append(HueCommand(
             1,
             [BulbState(1, {'on' : True, 'bri' : 1, 'sat': 255, 'hue' : 65280, 'transitiontime' : 10}),
              BulbState(2, {'on' : True, 'bri' : 1, 'sat': 255, 'hue' : 65280, 'transitiontime' : 10}),
              BulbState(3, {'on' : True, 'bri' : 1, 'sat': 255, 'hue' : 65280, 'transitiontime' : 10})]))
        fuck_it.append(HueCommand(
             1,
             [BulbState(1, {'on' : True, 'bri' : 254, 'sat': 255, 'hue' : 65280, 'transitiontime' : 10}),
              BulbState(2, {'on' : True, 'bri' : 254, 'sat': 255, 'hue' : 65280, 'transitiontime' : 10}),
              BulbState(3, {'on' : True, 'bri' : 254, 'sat': 255, 'hue' : 65280, 'transitiontime' : 10})]))

    return Experience(r'PATH TO WAKE UP SONG', fuck_it)

def wake_the_fuck_up():
    scenes = intialize_scenes()
    # Gradual wake up
    choice(scenes).play()

    if not GLOBAL_STOP:
        get_the_fuck_up = initialize_fuck()
        # Get out of bed lazy
        get_the_fuck_up.play()

    # Deactivate
    Experience(None, [HueCommand(0,
             [BulbState(1, {'on' : True, 'bri' : 200, 'sat': 175, 'hue' : 12750, 'transitiontime' : 50}),
              BulbState(2, {'on' : True, 'bri' : 200, 'sat': 175, 'hue' : 12750, 'transitiontime' : 50}),
              BulbState(3, {'on' : True, 'bri' : 200, 'sat': 175, 'hue' : 12750, 'transitiontime' : 50})])]).play()


class MyFrame(wx.Frame):
    """make a frame, inherits wx.Frame"""
    def __init__(self):
        # create a frame, no parent, default to wxID_ANY
        wx.Frame.__init__(self, None, wx.ID_ANY, 'wxButton',
            pos=(0, 0), size=wx.DisplaySize())
        self.SetBackgroundColour("green")

        self.button1 = wx.Button(self, id=-1, label='OFF',
            pos=(8, 8), size=(175, 28))
        self.button1.Bind(wx.EVT_BUTTON, self.button1Click)
        # optional tooltip
        self.button1.SetToolTip(wx.ToolTip("click for off"))
        # show the frame
        self.Show(True)
        self.ToggleWindowStyle(wx.STAY_ON_TOP)
        global GLOBAL_STOP
        GLOBAL_STOP = False
        self.prog = threading.Thread(target=wake_the_fuck_up)
        self.prog.start()
        #listen for natural death
        self.killthread = threading.Thread(target=self.on_timer)
        self.killthread.start()

    def on_timer(self):
        while self.prog.is_alive():
            time.sleep(0.1)
        application.Exit()

    def button1Click(self,event):
        self.button1.Hide()
        self.SetTitle("Alert Terminated")
        global GLOBAL_STOP
        GLOBAL_STOP = True


application = wx.PySimpleApp()
def alarm_clock():
    # call class MyFrame
    window = MyFrame()
    # start the event loop
    application.MainLoop()
