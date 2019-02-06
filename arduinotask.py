import datetime,pymysql

db=pymysql.connect("localhost", "flowerbot", "mycroft", "sensordata")
curs=db.cursor()

from arduinodata import getCurrentSensorData

sensordata = getCurrentSensorData()

select_stmt = "SELECT moisture,last_watered FROM history ORDER BY date DESC"

with db:
    curs.execute(select_stmt)

moistureInfo = curs.fetchone()

moistDifference = sensordata[0] - float(moistureInfo[0])

datalist = list(sensordata)

if(moistDifference > 100):
    currentTime= datetime.datetime.now()
    datalist.append(currentTime)
else:
    datalist.append(moistureInfo[1])

print(datalist)

insert_stmt = (
  "INSERT INTO history (moisture, lux, pressure, humidity, temperature, last_watered) " "VALUES (%s, %s, %s, %s, %s, %s)"
)

with db:
    curs.execute (insert_stmt, datalist)
