#!/usr/bin/env python3

from websocket import create_connection
uri = 'ws://localhost:8181/core'
#ws = create_connection(uri)
#print("Sending to " + uri + "...")

message = '{"type": "mycroft.mic.listen", "data": {}}'
#result = ws.send(message)
#print("Receiving..." )
#result = ws.recv()
#print("Received '%s'" % result)
#ws.close()

import serial,time,os,pymysql,sys
from serial import SerialException

db = pymysql.connect("localhost", "flowerbot", "mycroft", "sensordata")
curs=db.cursor()
insert_stmt = ("INSERT INTO watering (moisture) " "VALUES (%s)")

z1baudrate = 57600
z1port = '/dev/ttyACM0'  # set the correct port before run it

z1serial = serial.Serial(port=z1port, baudrate=z1baudrate)
z1serial.timeout = 2

count = 0
varCount = 0
averageValue = 0
totalValue = 0
maxVariance = 0

valDiff = 0

isTouched = 0

watering = 0
moist = 0
prevMoist1 = 0
prevMoist2 = 0
waterDecay = 0
lux = 0
pressure = 0
hum = 0
temp = 0

while True:
    size = z1serial.inWaiting()
    if(size):
        try:
            data = z1serial.readline()
        except SerialException as e:
            print("serial exception")

        dataString = ""
        try:
            dataString = data.decode()
        except UnicodeDecodeError as e:
            print("datastring incomplete")

        if dataString.startswith(" moist_"):
            #print(dataString)
            pieces = data.split()
            if len(pieces) > 0:
                moistPieces = pieces[0].decode().split("_")
                if len(moistPieces) > 0:
                    try:
                        moistString = moistPieces[1]
                    except IndexError as er:
                        print("moisture not readable")


            if len(pieces) > 1:
                luxPieces = pieces[1].decode().split("_")
                if len(luxPieces) > 0:
                    try:
                        luxString = luxPieces[1]
                    except IndexError as er:
                        print("lux not readable")

            if len(pieces) > 2:
                pressurePieces = pieces[2].decode().split("_")
                if len(pressurePieces) > 0:
                    try:
                        pressureString = pressurePieces[1]
                    except IndexError as er:
                        print("pressure not readable")

            if len(pieces) > 3:
                humPieces = pieces[3].decode().split("_")
                if len(humPieces) > 0:
                    try:
                        humString = humPieces[1]
                    except IndexError as er:
                        print("humidity not readable")

            if len(pieces) > 4:
                tempPieces = pieces[4].decode().split("_")
                if len(tempPieces) > 0:
                    try:
                        tempString = tempPieces[1]
                    except IndexError as er:
                        print("temperature not readable")

            prevMoist2 = prevMoist1
            prevMoist1 = moist

            try:
                moist = float(moistString)
            except ValueError as er:
                moist = 0

            try:
                lux = float(luxString)
            except ValueError as er:
                lux = 0

            try:
                pressure = float(pressureString)
            except ValueError as er:
                pressure = 0

            try:
                hum = float(humString)
            except ValueError as er:
                hum = 0

            try:
                temp = float(tempString)
            except ValueError as er:
                temp = 0

            if (moist-prevMoist2 >= 7 and moist-prevMoist2 <= 300 and watering == 0):
                watering = 1
                with db:
                    curs.execute(insert_stmt, prevMoist2)
                print("WATERING...")
                time.sleep(300)
                count = 0
                varCount = 0
                averageValue = 0
                totalValue = 0

            if len(pieces) > 5 and watering == 0:
                touchPieces = pieces[5].decode().split("_")
                if len(touchPieces) > 0:
                    try:
                        touchValueString = touchPieces[1]
                    except IndexError as er:
                        touchValueString = 0
                        print("touch not readable")
                    if touchValueString != 0:
                        touchValue = float(touchValueString)
                        if count >= 100:
                            averageValue = totalValue / 100
                            totalValue = 0
                            count = 0
                        else:
                            count = count + 1
                            totalValue = totalValue + touchValue

                        if averageValue > 0 and varCount <= 100:
                            if averageValue - touchValue > maxVariance:
                                maxVariance = averageValue - touchValue
                                print("maxVariance is:" + str(maxVariance))
                            if averageValue - touchValue > 0:
                                varCount = varCount + 1

                        if (varCount > 100 and averageValue - touchValue > maxVariance):
                            valDiff = valDiff + averageValue - touchValue
                            print(valDiff)

                            if (valDiff >= maxVariance * 3 and moist - prevMoist1 <= 5):
                                print("BERUEHRT")
                                totalValue = totalValue + valDiff
                                valDiff = 0
                                averageValue = 0
                                varCount = 0

                        else:
                            valDiff = 0
                else:
                    print(0)

    sys.stdout.flush()
    z1serial.flushInput()
    time.sleep(60.0 / 1000.0)


