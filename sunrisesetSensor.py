#!/usr/bin/env python3

import psycopg2
from sensorStateClass import sensorState
from settings import settingsClass
from datetime import datetime

conn = psycopg2.connect(host='localhost', dbname='tank', user='tank', password='skinner2')
conn.autocommit = True
cur = conn.cursor()


def getRowCount(sql):
    cur.execute(sql)
    rows = cur.fetchall()

    return len(rows)

def main():
    mySensorState = sensorState()
    mySettings = settingsClass()
    
    sql = "SELECT * FROM public.\"sunrisesetLatestDetail\";"
    cur.execute(sql)
    rows = cur.fetchall()
    
    if len(rows) > 0:
        row  = rows[0]
        sunrise = row[2]
        sunset = row[3]
        
        irrigationPeriod = mySettings.settings["pumpduration"]
        isTimeToIrrigate = 0
        
        nowStartTime = datetime.now()
        nowStartInt = (nowStartTime.hour * 60) + nowStartTime.minute

        nowSunriseStart = (sunrise.hour * 60) + sunrise.minute
        nowSunriseEnd = (sunrise.hour * 60) + sunrise.minute + irrigationPeriod
        
        nowSunsetStart = (sunset.hour * 60) + sunset.minute
        nowSunsetEnd = (sunset.hour * 60) + sunset.minute + irrigationPeriod
        
        if nowSunriseStart <= nowStartInt <= nowSunriseEnd:
            isTimeToIrrigate = 1
        else:
            isTimeToIrrigate = 0

        mySensorState.setSensorID('10000002')
        mySensorState.setSensorType('sun-rise')
        mySensorState.setSensorValue(isTimeToIrrigate)
        mySensorState.setSatus()
    
        if nowSunsetStart <= nowStartInt <= nowSunsetEnd:
            isTimeToIrrigate = 1
        else:
            isTimeToIrrigate = 0

        mySensorState.setSensorID('10000003')
        mySensorState.setSensorType('sun-set')
        mySensorState.setSensorValue(isTimeToIrrigate)
        mySensorState.setSatus()

main()

