__author__ = 'Aran'

import os
import win32com
import pyttsx
import pythoncom
from xml.dom import minidom
import urllib
from utilities import *
import threading
import wx

GLOBAL_STOP = False

def play_report():
    pythoncom.CoInitialize()
    engine = pyttsx.init()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate-10)
    time.sleep(2)
    if GLOBAL_STOP:
        return True
    engine.say('Good Morning... Uhh run... I hope you had a good sleep')
    engine.runAndWait()
    HueCommand(1, [BulbState(1, {'on' : True, 'bri' : 200, 'sat': 200, 'hue' : 46920, 'transitiontime' : 20}),
                   BulbState(2, {'on' : True, 'bri' : 200, 'sat': 200, 'hue' : 46920, 'transitiontime' : 20}),
                   BulbState(3, {'on' : True, 'bri' : 200, 'sat': 200, 'hue' : 46920, 'transitiontime' : 20})]).execute()
    if GLOBAL_STOP:
        return True
    engine.say(weather())
    engine.runAndWait()
    HueCommand(1, [BulbState(1, {'on' : True, 'bri' : 200, 'sat': 175, 'hue' : 25000, 'transitiontime' : 20}),
                   BulbState(2, {'on' : True, 'bri' : 200, 'sat': 175, 'hue' : 25000, 'transitiontime' : 20}),
                   BulbState(3, {'on' : True, 'bri' : 200, 'sat': 175, 'hue' : 25000, 'transitiontime' : 20})]).execute()
    if GLOBAL_STOP:
        return True
    engine.say(quote())
    engine.runAndWait()
    if GLOBAL_STOP:
        return True
    # Deactivate
    engine.say("I hope you have a good day... Uhh run")
    HueCommand(1, [BulbState(1, {'on' : True, 'bri' : 200, 'sat': 175, 'hue' : 12750, 'transitiontime' : 50}),
                   BulbState(2, {'on' : True, 'bri' : 200, 'sat': 175, 'hue' : 12750, 'transitiontime' : 50}),
                   BulbState(3, {'on' : True, 'bri' : 200, 'sat': 175, 'hue' : 12750, 'transitiontime' : 50})]).execute()
    engine.runAndWait()
    return False

def weather():
    wurl = 'http://xml.weather.yahoo.com/forecastrss?p=%s'
    wser = 'http://xml.weather.yahoo.com/ns/rss/1.0'
    zipcode = '02238'
    url = wurl % zipcode +'&u=c'
    dom = minidom.parse(urllib.urlopen(url))
    forecasts = []
    for node in dom.getElementsByTagNameNS(wser, 'forecast'):
        forecasts.append({
            'date': node.getAttribute('date'),
            'low': node.getAttribute('low'),
            'high': node.getAttribute('high'),
            'condition': node.getAttribute('text')
        })
    ycondition = dom.getElementsByTagNameNS(wser, 'condition')[0]

    return "The current temp is... "+ycondition.getAttribute('temp')+" degrees... and the current condition is "+ycondition.getAttribute('text')+"... it is projected to be... "+forecasts[0]['high']+" degrees... and the weather will be "+forecasts[0]['condition']

def quote():
    wurl = 'http://www.swanandmokashi.com/Homepage/Webservices/QuoteOfTheDay.asmx/GetQuote?'
    wser = 'http://swanandmokashi.com'
    dom = minidom.parse(urllib.urlopen(wurl))
    return "Your quote for the day is... "+dom.getElementsByTagName('QuoteOfTheDay')[0].firstChild.nodeValue


def run_report():
    if play_report():
       HueCommand(1, [BulbState(1, {'on' : True, 'bri' : 200, 'sat': 175, 'hue' : 12750, 'transitiontime' : 50}),
                   BulbState(2, {'on' : True, 'bri' : 200, 'sat': 175, 'hue' : 12750, 'transitiontime' : 50}),
                   BulbState(3, {'on' : True, 'bri' : 200, 'sat': 175, 'hue' : 12750, 'transitiontime' : 50})]).execute()


class MyFrame(wx.Frame):
    """make a frame, inherits wx.Frame"""
    def __init__(self):
        # create a frame, no parent, default to wxID_ANY
        wx.Frame.__init__(self, None, wx.ID_ANY, 'wxButton',
            pos=(0, 0), size=wx.DisplaySize())
        self.SetBackgroundColour("green")

        self.button1 = wx.Button(self, id=-1, label='SILENCE',
            pos=(8, 8), size=(175, 28))
        self.button1.Bind(wx.EVT_BUTTON, self.button1Click)
        # optional tooltip
        self.button1.SetToolTip(wx.ToolTip("click for off"))
        # show the frame
        self.Show(True)
        self.ToggleWindowStyle(wx.STAY_ON_TOP)
        global GLOBAL_STOP
        GLOBAL_STOP = False
        self.prog = threading.Thread(target=run_report)
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
def report():
    # call class MyFrame
    window = MyFrame()
    # start the event loop
    application.MainLoop()