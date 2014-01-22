__author__ = 'Aran'
import urllib
import time
from utilities import *
import os
import glob
import mp3play
import MySQLdb
import pyttsx
import pythoncom
from datetime import datetime
from random import choice

def get_mp3s():
    mp3s =[]
    os.chdir(r'PATH TO MUSIC LIBRARY')
    for files in glob.glob("*.mp3"):
        mp3s.append(files)
    return mp3s

def get_playlists():
    playlists =[]
    os.chdir(r'PATH TO MUSIC LIBRARY WITH TXT PLAYLISTS')
    for files in glob.glob("*.txt"):
        playlists.append(files)
    return playlists

class Playlist:
    def __init__(self, listname):
        self.file = r'PATH TO MUSIC LIBRARY WITH TXT PLAYLISTS'+listname
        with open(self.file) as f:
            self.songs = f.readlines()

    def nextsong(self):
        return choice(self.songs).rstrip('\n')+'.mp3'

def media_loop():
    myDB = MySQLdb.connect(host="************",user="**********",passwd="*********",db="***********")
    SONG = None
    SONG_NAME = ""
    LIST_NAME = ""
    lastrecord = datetime.now()
    updated = False
    naturalpause = False
    currentlist = None
    while True:
        cHandler = myDB.cursor()

        # update past state list every 10 seconds
        delta = datetime.now() - lastrecord
        if delta.seconds > 10 or updated:
            action = '0'
            if SONG is not None:
                currentsong = str(SONG_NAME)
                if SONG.isplaying():
                    action = '1'
            else:
                currentsong = None

            if currentlist is not None:
                playinglist = str(LIST_NAME)
            else:
                playinglist = None

            trip = HueCommand(None, None).get_states([1])
            if not trip[0]['on']:
                on = '0'
            else:
                on = '1'

            try:
                    if currentsong is not None:
                        if playinglist is not None:
                            cHandler.execute("INSERT INTO paststates (song, playlist, action, lightstate1, lighthue1, lightbri1) VALUES ('"+currentsong.replace("'", "\\'")+"', '"+playinglist.replace("'", "\\'")+"', '"+action+"', '"+on+"', '"+str(trip[0]['hue'])+"', '"+str(trip[0]['bri'])+"')")
                        else:
                            cHandler.execute("INSERT INTO paststates (song, action, lightstate1, lighthue1, lightbri1) VALUES ('"+currentsong.replace("'", "\\'")+"', '"+action+"', '"+on+"', '"+str(trip[0]['hue'])+"', '"+str(trip[0]['bri'])+"')")
                    else:
                        cHandler.execute("INSERT INTO paststates (lightstate1, lighthue1, lightbri1) VALUES ('"+on+"', '"+str(trip[0]['hue'])+"', '"+str(trip[0]['bri'])+"')")
            except Exception as e:
                    myDB = MySQLdb.connect(host="****************",user="*********",passwd="*********",db="************")
                    print("disconnected... with "+ e.message)
                    continue

            # Reset events
            lastrecord = datetime.now()
            if updated:
                updated = False


        # handle song ending
        if SONG is not None and not SONG.isplaying() and not naturalpause:
            if currentlist is not None:
                song_name = currentlist.nextsong()
            else:
                song_name = choice(get_mp3s())
            SONG.stop()
            base_path = r'PATH TO MUSIC'
            path = base_path + song_name
            try:
                mp3 = mp3play.load(path)
                mp3.play()
            except:
                print "error playing "+song_name
                continue
            SONG = mp3
            SONG_NAME = song_name

        time.sleep(1.5)

        # Scan for web commands
        try:
            cHandler.execute("SELECT * FROM goalstates ORDER BY time")
        except:
            myDB = MySQLdb.connect(host="************",user="**********",passwd="*******",db="**********")
            print("disconnected... retrying")
            continue
        command = cHandler.fetchone()

        # Execute commands
        if command is not None:
            updated = True
            # Clear command from db
            try:
                cHandler.execute("DELETE FROM goalstates WHERE id = '"+str(command[0])+"'")
            except:
                myDB = MySQLdb.connect(host="**********",user="********",passwd="***********",db="************88")
                print("disconnected... retrying")
                continue

            # Pull all command data
            song = str(command[1])
            playlist = str(command[2])
            action = int(command[3])
            voice = str(command[4])
            light1state = int(command[5])
            light1hue = int(command[6])
            light1bri = int(command[7])

            # Lights Stuff
            light1command = {}
            if light1state == 1:
                light1command['on'] = True
            elif light1state == 0:
                light1command['on'] = False
            if light1hue != -1:
                light1command['hue'] = int(light1hue)
            if light1bri != -1:
                light1command['bri'] = int(light1bri)

            if len(light1command.keys()) > 0:
                try:
                    HueCommand(0, [BulbState(1, light1command),
                           BulbState(2, light1command),
                           BulbState(3, light1command)]).execute()
                except:
                    print "unable to change lights"


            # VOICE STUFF
            if len(voice) > 0:
                pythoncom.CoInitialize()
                engine = pyttsx.init()
                rate = engine.getProperty('rate')
                engine.setProperty('rate', rate-13)
                engine.say(voice)
                if SONG is not None:
                    SONG.pause()
                engine.runAndWait()
                if SONG is not None:
                    SONG.unpause()

            # MP3 STUFF
            if playlist is not None and len(playlist) > 0:
                currentlist = Playlist(playlist)
                if SONG is not None:
                    SONG.stop()
                list_song = currentlist.nextsong()
                try:
                    mp3 = mp3play.load(r'PATH TO MUSIC' + list_song)
                    mp3.play()
                except:
                    print "error playing "+list_song
                    continue
                LIST_NAME = playlist
                SONG_NAME = list_song
                SONG = mp3
            elif song is not None and len(song) > 0:
                if SONG is not None:
                    SONG.stop()
                try:
                    mp3 = mp3play.load(r'PATH TO MUSIC' + song)
                    mp3.play()
                except:
                    print "error playing "+song
                    continue
                SONG = mp3
                SONG_NAME = song
                currentlist = None
            elif action != 0 and SONG != None:
                if action == 1:
                    if SONG.ispaused():
                        SONG.unpause()
                        naturalpause = False
                elif action == 2:
                    if SONG.isplaying():
                        SONG.pause()
                        naturalpause = True
                elif action == 4:
                    SONG.stop()
                    SONG = None
                    currentlist = None
                elif action == 3:
                    if currentlist is not None:
                        song_name = currentlist.nextsong()
                    else:
                        song_name = choice(get_mp3s())
                    SONG.stop()
                    base_path = r'PATH TO MUSIC'
                    path = base_path + song_name
                    try:
                        mp3 = mp3play.load(path)
                        mp3.play()
                    except:
                        print "error playing "+song_name
                        continue
                    SONG_NAME = song_name
                    SONG = mp3



def update_stored_state():
    myDB = MySQLdb.connect(host="**********",user="*********",passwd="*********",db="***********")
    cHandler = myDB.cursor()
    cHandler.execute("DELETE FROM paststates")
    cHandler.execute("DELETE FROM musiclibrary")
    cHandler.execute("DELETE FROM playlists")
    for mp3 in get_mp3s():
        sane_mp3 = str(mp3).replace("'", "\\'")
        cHandler.execute("INSERT INTO musiclibrary (song) VALUES ('"+sane_mp3+"')")
        print "inserting song "+sane_mp3+" into library"
    for plist in get_playlists():
        sane_plist = str(plist).replace("'", "\\'")
        cHandler.execute("INSERT INTO playlists (list) VALUES ('"+sane_plist+"')")
        print "inserting playlist "+sane_plist+" into library"