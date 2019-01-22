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

import serial,time,os

z1baudrate = 57600
z1port = '/dev/ttyACM0'  # set the correct port before run it

z1serial = serial.Serial(port=z1port, baudrate=z1baudrate)
z1serial.timeout = 2


lastValue = 0;
isTouched = 0;

while True:
    size = z1serial.inWaiting()
    if(size):
        data = z1serial.readline(size)
        if data.decode().startswith(" moist_"):
            pieces = data.split()
            if len(pieces) > 5:
                touchPieces = pieces[5].decode().split("_")
                if len(touchPieces) > 0:
                    touchValueString = touchPieces[1]
                    touchValue = float(touchValueString)
                    print(touchValue)
                    if(lastValue == 0):
                        lastValue = touchValue
                    else:
                        if(lastValue-touchValue > 5):
                            if(isTouched == 0):
                                print("BERÜHRT")
                                isTouched = 1;
                                # ws = create_connection(uri)
                                # result = ws.send(message)
                                # ws.close()

                        else:
                            isTouched = 0;
                            lastValue = touchValue;
                else:
                    print(0)
    z1serial.flushInput()
    time.sleep(110.0 / 1000.0)
