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

import serial,time,os,pymysql

db = pymysql.connect("localhost", "flowerbot", "mycroft", "sensordata")
curs=db.cursor()
insert_stmt = (
  "INSERT INTO watering (moisture) " "VALUES (%s)"
)

z1baudrate = 57600
z1port = '/dev/ttyACM0'  # set the correct port before run it

z1serial = serial.Serial(port=z1port, baudrate=z1baudrate)
z1serial.timeout = 2

count = 0
averageValue = 0
totalValue = 0

valDiff = 0

isTouched = 0

watering = 0
moist = 0
prevMoist1 = 0
prevMoist2 = 0
lux = 0
pressure = 0
hum = 0
temp = 0

#calling the servo
def turnServo():
    z1serial.write(b'aaaa\n')

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
            pieces = data.split()
            if len(pieces) > 0:
                moistPieces = pieces[0].decode().split("_")
                if len(moistPieces) > 0:
                    moistString = moistPieces[1]

            if len(pieces) > 1:
                luxPieces = pieces[1].decode().split("_")
                if len(luxPieces) > 0:
                    luxString = luxPieces[1]

            if len(pieces) > 2:
                pressurePieces = pieces[2].decode().split("_")
                if len(pressurePieces) > 0:
                    pressureString = pressurePieces[1]

            if len(pieces) > 3:
                humPieces = pieces[3].decode().split("_")
                if len(humPieces) > 0:
                    humString = humPieces[1]

            if len(pieces) > 4:
                tempPieces = pieces[4].decode().split("_")
                if len(tempPieces) > 0:
                    tempString = tempPieces[1]

            prevMoist2 = prevMoist1
            prevMoist1 = moist

            moist = float(moistString)
            lux = float(luxString)
            pressure = float(pressureString)
            hum = float(humString)
            temp = float(tempString)

            print(moist-prevMoist1)

            if (moist-prevMoist2 >= 7 and moist-prevMoist2 <= 300 and watering == 0):
                watering = 1
                with db:
                    curs.execute(insert_stmt, prevMoist2)
                print("WATERING")
                time.sleep(5)

            if len(pieces) > 5 and watering == 0:
                touchPieces = pieces[5].decode().split("_")
                if len(touchPieces) > 0:
                    touchValueString = touchPieces[1]
                    touchValue = float(touchValueString)
                    if count >= 100:
                        averageValue = totalValue/100
                        totalValue = 0;
                        count = 0;
                        #print("  avg:")
                        #print(averageValue)
                    else:
                        count = count +1
                        totalValue= totalValue +touchValue

                    if(averageValue-touchValue >= 3):
                        valDiff = valDiff + averageValue-touchValue;

                        if(valDiff >= 30 and moist-prevMoist1 <= 5):
                            print("BERÜHRT")
                            #turnServo()
                            os.system("aplay /home/pi/mycroft-core/mycroft/res/snd/start_listening.wav")
                            #os.system("aplay /home/osboxes/mycroft-core/mycroft/res/snd/start_listening.wav")
                            #ws = create_connection(uri)
                            #result = ws.send(message)
                            #ws.close()
                            totalValue=totalValue+valDiff
                            valDiff= 0

                            time.sleep(2)
                    else:
                        valDiff = 0
                else:
                    print(0)

    z1serial.flushInput()
    time.sleep(60.0 / 1000.0)
