#These are the imports google said to include
import gdata.calendar.service
import gdata.service
import atom.service
import gdata.calendar
import gdata.calendar
import atom
import getopt
import sys
import string
import time
import wake_up
import morning_report
import quick_alert
import wx
import web_query
import mp3play
import threading

import xe #for the time comparator
from feed.date.rfc3339 import tf_from_timestamp #also for the comparator
from datetime import datetime #for the time on the rpi end
from datetime import timedelta
from apscheduler.scheduler import Scheduler #this will let us check the calender on a regular interval


# def AlarmQuery(calendar_service, text_query='wake'):
#     print 'Full text query for wake events on Primary Calendar: \'%s\'' % ( text_query,)
#     query = gdata.calendar.service.CalendarEventQuery('default', 'private', 'full', text_query)
#     feed = calendar_service.CalendarQuery(query)
#     for i, an_event in enumerate(feed.entry):
#         for a_when in an_event.when:
#             print "---"
#             print an_event.title.text ,"Number:",i,"Event Time:",time.strftime('%d-%m-%Y %H:%M',time.localtime(tf_from_timestamp(a_when.start_time))),"Current Time:",time.strftime('%d-%m-%Y %H:%M')
#
#             if time.strftime('%d-%m-%Y %H:%M',time.localtime(tf_from_timestamp(a_when.start_time))) == time.strftime('%d-%m-%Y %H:%M'):
#                 print "Comparison: Pass"
#                 print "---"
#                 wake_up.alarm_clock()
#                 morning_report.report()
#             else:
#                 print "Comparison:Fail" #the "wake" event's start time != the system's current time

def EventQuery(calendar_service):
    print "checking for events"
    start_date = datetime.now().date().isoformat()
    end_date = datetime.now() + timedelta(days=1)
    end_date = end_date.date().isoformat()
    query = gdata.calendar.service.CalendarEventQuery('default', 'private', 'full')
    query.start_min = start_date
    query.start_max = end_date
    feed = calendar_service.CalendarQuery(query)
    now = datetime.now()
    for i, an_event in enumerate(feed.entry):
        for a_when in an_event.when:
            # special for alarm clock
            if an_event.title.text == 'wake':
                if time.strftime('%d-%m-%Y %H:%M',time.localtime(tf_from_timestamp(a_when.start_time))) == time.strftime('%d-%m-%Y %H:%M'):
                    print "Alarm comparison pass"
                    wake_up.alarm_clock()
                    morning_report.report()
            else:
                delta = datetime.fromtimestamp(time.mktime(time.localtime(tf_from_timestamp(a_when.start_time)))) - now
                if delta.days < 0:
                    continue
                delta_in_min = int(delta.total_seconds() / 60)
                print str(an_event.title.text)
                print delta_in_min
                if delta_in_min <= 15 and delta_in_min >= 0:
                    print str(an_event.title.text)+ " occuring in "+str(delta_in_min)
                    if delta_in_min % 5 == 0:
                        quick_alert.cal_alert(str(an_event.title.text), delta_in_min)


web_query.update_stored_state()

# Start my stateful music shit in parrallel with restart logic
prog = threading.Thread(target=web_query.media_loop)
prog.start()

def main_loop():
    print "------------start-----------"
    #this is more stuff google told me to do, but essentially it handles the login credentials
    calendar_service = gdata.calendar.service.CalendarService()
    calendar_service.email = '*****************' #your google email
    calendar_service.password = '***************' #your google password
    calendar_service.source = 'Google-Calendar_Python_Sample-1.0'
    calendar_service.ProgrammaticLogin()
    # Check calender for events
    EventQuery(calendar_service)
    # Check room monitoring system status and restart
    global prog
    if not prog.isAlive():
        prog = threading.Thread(target=web_query.media_loop)
        prog.start()
    print "-------------end------------"


scheduler1 = Scheduler(standalone=True)
scheduler1.add_interval_job(main_loop,seconds=35)
# add cal loop
scheduler1.add_interval_job(web_query.update_stored_state, days=1)
scheduler1.start()

