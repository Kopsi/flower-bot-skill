import serial,time,os

z1baudrate = 57600
z1port = '/dev/ttyACM0'  # set the correct port before run it

z1serial = serial.Serial(port=z1port, baudrate=z1baudrate)
z1serial.timeout = 2



def getTouchValue():
    if z1serial.is_open:
        while True:
            size = z1serial.inWaiting()
            if size:
                data = z1serial.readline(size)

                if data.decode().startswith(" moist_"):

                    pieces = data.split()
                    if len(pieces) > 5:
                        touchPieces = pieces[5].decode().split("_")
                        if len(touchPieces) > 0:
                            touchValueString = touchPieces[1]


                    touchValue = float(touchValueString)

                    return (touchValue)

            else:
                return 0
            time.sleep(1)
    else:
        return 0

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
                        if(lastValue-touchValue > 15):
                            if(isTouched == 0):
                                print("BERÜHRT")
                                isTouched = 1;
                                os.system("aplay /home/osboxes/mycroft-core/mimic/stop.wav")
                        else:
                            isTouched = 0;
                            lastValue = touchValue;
                else:
                    print(0)
    z1serial.flushInput()
    time.sleep(110.0 / 1000.0)
