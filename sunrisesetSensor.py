#!/usr/bin/env python3

import psycopg2
from sensorStateClass import sensorState
from datetime import datetime, timedelta

conn = psycopg2.connect(host='localhost', dbname='tank', user='tank', password='skinner2')
conn.autocommit = True
cur = conn.cursor()


def getRowCount(sql):
    cur.execute(sql)
    rows = cur.fetchall()

    return len(rows)

def main():
    mySensorState = sensorState()
    
    sql = "SELECT * FROM public.\"sunrisesetLatestDetail\";"
    cur.execute(sql)
    rows = cur.fetchall()
    
    if len(rows) > 0:
        row  = rows[0]
        sunrise = row[2]
        sunset = row[3]
        
        irrigationPeriod = 5
        isTimeToIrrigate = 0
        
        nowStartTime = datetime.now()
        nowEndTime = (datetime.now() + timedelta(minutes = irrigationPeriod))
        
        nowStartInt = (nowStartTime.hour * 60) + nowStartTime.minute
        nowEndInt = (nowEndTime.hour * 60) + nowEndTime.minute
        nowSunrise = (sunrise.hour * 60) + sunrise.minute
        nowSunset = (sunset.hour * 60) + sunset.minute
        
        if nowSunrise > nowStartInt and nowSunrise < nowEndInt:
            isTimeToIrrigate = 1
        else:
            isTimeToIrrigate = 0

        mySensorState.setSensorID('10000002')
        mySensorState.setSensorType('sun-rise')
        mySensorState.setSensorValue(isTimeToIrrigate)
        mySensorState.setSatus()
    
        if nowSunset > nowStartInt and nowSunset < nowEndInt:
            isTimeToIrrigate = 1
        else:
            isTimeToIrrigate = 0

        mySensorState.setSensorID('10000003')
        mySensorState.setSensorType('sun-set')
        mySensorState.setSensorValue(isTimeToIrrigate)
        mySensorState.setSatus()

main()

