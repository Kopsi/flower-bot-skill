import os,pty,serial,pymysql,time, datetime

db = pymysql.connect("localhost", "monitor", "password", "flowerbot")
curs=db.cursor()

z1baudrate = 9600
z1port = '/dev/ttyACM0'  # set the correct port before run it

z1serial = serial.Serial(port=z1port, baudrate=z1baudrate)
z1serial.timeout = 2

def getCurrentSensorData():
    errorcount = 0
    if z1serial.is_open:
        while True:
            size = z1serial.inWaiting()
            if size:
                data = z1serial.readline(size)

                if data.decode().startswith(" moist_"):

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

                    moist = float(moistString)
                    lux = float(luxString)
                    pressure = float(pressureString)
                    hum = float(humString)
                    temp = float(tempString)
                    return (moist, lux, pressure, hum, temp)

            else:
                errorcount+=1
                if errorcount > 5:
                    return "no data"
            time.sleep(1)
    else:
        return "serial not open"


def getSensorData(time):
    select_stmt = "SELECT moisture, lux, pressure, humidity, temperature FROM history ORDER BY ABS(DATEDIFF(date, %s))"

    with db:
        curs.execute(select_stmt, time)

    sensordata = curs.fetchone()
    return sensordata

