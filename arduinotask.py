import datetime,pymysql

db=pymysql.connect("localhost", "monitor", "password", "flowerbot")
curs=db.cursor()

from arduinodata import getCurrentSensorData

sensordata = getCurrentSensorData()

select_stmt = "SELECT moisture FROM history ORDER BY date DESC)"

with db:
    curs.execute(select_stmt)

currentMoisture = curs.fetchone()

insert_stmt = (
  "INSERT INTO history (moisture, lux, pressure, humidity, temperature) " "VALUES (%s, %s, %s, %s, %s)"
)

with db:
    curs.execute (insert_stmt, sensordata)

