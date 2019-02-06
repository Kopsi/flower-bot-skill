import os,pty,serial,pymysql,time, datetime

db = pymysql.connect("localhost", "flowerbot", "mycroft", "sensordata")
curs=db.cursor()

z1baudrate = 57600
z1port = '/dev/ttyACM0'  # set the correct port before run it

z1serial = serial.Serial(port=z1port, baudrate=z1baudrate)
z1serial.timeout = 2

def getCurrentSensorData():
    errorcount = 0
    if z1serial.is_open:
        while True:
            size = z1serial.inWaiting()
            if (size):
                try:
                    data = z1serial.readline()
                except SerialException as e:
                    print("serial exception")

                dataString = ""
                try:
                    dataString = data.decode();
                except UnicodeDecodeError as e:
                    print("decode error")

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

                    try:
                        moist = float(moistString)
                    except ValueError as er:
                        print("moisture not readable")
                        moist = 0

                    try:
                        lux = float(luxString)
                    except ValueError as er:
                        print("lux not readable")
                        lux = 0

                    try:
                        pressure = float(pressureString)
                    except ValueError as er:
                        print("lux not readable")
                        pressure = 0

                    try:
                        hum = float(humString)
                    except ValueError as er:
                        print("lux not readable")
                        hum = 0

                    try:
                        temp = float(tempString)
                    except ValueError as er:
                        print("lux not readable")
                        temp = 0

                    return (moist, lux, pressure, hum, temp)

            else:
                errorcount+=1
                if errorcount > 100:
                   return "no data"
            z1serial.flushInput()
            time.sleep(60.0/1000.0)
    else:
        return "serial not open"


def getSensorData(time):
    select_stmt = "SELECT moisture, lux, pressure, humidity, temperature FROM history ORDER BY ABS(DATEDIFF(date, %s))"

    with db:
        curs.execute(select_stmt, time)

    sensordata = curs.fetchone()
    return sensordata


def getLastWatered():
    select_stmt = "SELECT date FROM watering ORDER BY date DESC"
    with db:
        curs.execute(select_stmt)

    last_watered = curs.fetchone()

    now = datetime.datetime.now()

    days = now-last_watered[0]

    return days.days

