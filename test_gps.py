from datetime import datetime
import serial
import time
import string
import pynmea2
import sqlite

def CreateDb():
    Database = r".\db\sensornodedb.db"

    sql_create_GpsData_table = """ CREATE TABLE IF NOT EXISTS GpsData (
                                        GpsDateTime text PRIMARY KEY,
                                        Lat real NOT NULL,
                                        Long real NOT NULL,
                                        Speed real
                                    ); """

    # create a database connection
    Conn = sqlite.Create_Connection(Database)
    with Conn:
        # create GpsData table
        sqlite.Create_Table(Conn,sql_create_GpsData_table)

    return Conn

Conn=CreateDb()

while True:
	port="/dev/ttyAMA0"
	ser=serial.Serial(port, baudrate=9600, timeout=0.5)
	dataout = pynmea2.NMEAStreamReader()
	readdata=ser.readline()
	newdata=readdata.decode('latin-1')
	if newdata[0:6] == "$GPRMC":
		newmsg=pynmea2.parse(newdata)
		lat=newmsg.latitude
		lng=newmsg.longitude
		speed=25.2
		print (newmsg.timestamp)
		gps = "Latitude=" + str(lat) + "and Longitude=" + str(lng)
		print(gps)
        # insert GPS data
		GpsData = (datetime.now(), lat, lng,speed)
		sqlite.Insert_GpsData(Conn, GpsData)
