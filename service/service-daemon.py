#!/usr/bin/python
import sys
import time
import datetime
import subprocess
from astral import Astral

TURN_LIGHT_ON_CMD = "/home/pi/git/HomeAutomation/turnRoomsOn.sh"
TURN_LIGHT_OFF_CMD = "/home/pi/git/HomeAutomation/turnRoomsOff.sh"
DIM_DESK_LIGHT_LIGHT_CMD = "/home/pi/git/HomeAutomation/dimDeskLight.sh"

def isBeforeSunriseSunsetState():
    now = datetime.datetime.now()
    astral = Astral()
    astral.solar_depression = 'civil'
    city = astral["San Francisco"]
    sun = city.sun(date=datetime.datetime(now.year, now.month, now.day, now.hour), local=True)
    current_time = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute)
    before_sunset = sun['sunset'].timestamp() > current_time.timestamp()
    before_sunrise = sun['sunrise'].timestamp() > current_time.timestamp()
    return before_sunrise, before_sunset

# Global initialization to ensure a state change upon calling updateState() first time
after_noon = datetime.datetime.now().time() < datetime.time(12)
prev_before_sunrise, prev_before_sunset = (after_noon, after_noon)
lightsOn = False
print("Initial State: after_noon, prev_before_sunrise, prev_before_sunset:\n",
      after_noon, prev_before_sunrise, prev_before_sunset, "\n")

def updateState():
    global prev_before_sunrise
    global prev_before_sunset
    global lightsOn
    
    ### Execute this command every minute, no logging
    completedFrequent = subprocess.run(DIM_DESK_LIGHT_LIGHT_CMD, shell=True)
    # print("Completed DIM_DESK_LIGHT_LIGHT_CMD:", completedFrequent) 

    before_sunrise, before_sunset = isBeforeSunriseSunsetState()

    if (prev_before_sunrise != before_sunrise or prev_before_sunset != before_sunset): # Something changed
        if (before_sunrise == True and before_sunset == True):
            lightsOn = True
            print("It is still too early in the morning, re-affirm the lights are ON...", datetime.datetime.now())
            print(datetime.datetime.now())
        elif (before_sunrise == False and before_sunset == True):
            lightsOn = False
            print("It is a bright day, turn the lights OFF...", datetime.datetime.now())
        elif (before_sunrise == False and before_sunset == False):
            lightsOn = True
            print("It is evening and dark, turn the lights ON...", datetime.datetime.now())
            print(datetime.datetime.now())
            
        if (lightsOn):
            print("Tuning Lights ON\n")
            sys.stdout.flush()
            completed = subprocess.run(TURN_LIGHT_ON_CMD, shell=True)
            print("Completed:", completed, "\n")
            sys.stdout.flush()
        else:
            print("Turning Lighsts OFF\n")
            sys.stdout.flush()
            completed = subprocess.run(TURN_LIGHT_OFF_CMD, shell=True)
            print("Completed:", completed, "\n")
            sys.stdout.flush()
        
        print("State updated:\nOld State: before_sunrise, before_sunset, prev_before_sunrise, prev_before_sunset:\n",
              before_sunrise, before_sunset, prev_before_sunrise, prev_before_sunset)
        # Save the last state
        prev_before_sunrise = before_sunrise
        prev_before_sunset = before_sunset
        print("New State: before_sunrise, before_sunset, prev_before_sunrise, prev_before_sunset:\n",
              before_sunrise, before_sunset, prev_before_sunrise, prev_before_sunset, "\n")
    else:
        #print("Nothing changed, before_sunrise, before_sunset, prev_before_sunrise, prev_before_sunset:\n",
        #      before_sunrise, before_sunset, prev_before_sunrise, prev_before_sunset, "\n")
        return

class App():
    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path =  '/tmp/foo.pid'
        self.pidfile_timeout = 5
    def run(self):
        print("App started...", datetime.datetime.now())
        sys.stdout.flush()
        ####################
        #return
        ####################
        while True:
            updateState()
            sys.stdout.flush()
            time.sleep(60)

app = App()
app.run()
