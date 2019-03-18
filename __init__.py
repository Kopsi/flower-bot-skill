# TODO: Add an appropriate license to your skill before publishing.  See
# the LICENSE file for more information.

# Below is the list of outside modules you'll be using in your skill.
# They might be built-in to Python, from mycroft-core or from external
# libraries.  If you use an external library, be sure to include it
# in the requirements.txt file so the library is installed properly
# when the skill gets installed later by a user.

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.util.log import LOG
import time, threading

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('/opt/mycroft/skills/flower-bot-skill.kopsi/customskill.log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

import importlib.util
spec = importlib.util.spec_from_file_location("", "/opt/mycroft/skills/flower-bot-skill.kopsi/arduinodata.py")
arduinodata = importlib.util.module_from_spec(spec)
spec.loader.exec_module(arduinodata)

import serial

class FlowerBotSkill(MycroftSkill):

    water = 0
    light = 0
    airPressure = 0
    airMoisture = 0
    temperature = 0
    waterTime = 0
    comfortCounter = 0
    ct=0

    # The constructor of the skill, which calls MycroftSkill's constructor
    def __init__(self):
        super(FlowerBotSkill, self).__init__(name="FlowerBotSkill")
        # Initialize working variables used within the skill.
        sensorData = arduinodata.getCurrentSensorData()

#TODO: values might need to be readjusted
    @intent_handler(IntentBuilder("").require("Flower"))
    def handle_flower_intent(self, message):

        z1serial = serial.Serial('/dev/ttyACM0', 57600)

        updateData()
        logger.info(self.water)

        if self.water < 400:
            self.speak_dialog("need.water")
            self.comfortCounter += 1
        if self.water > 800:
            self.speak_dialog("too.much.water")
            self.comfortCounter += 1
        if self.light < 50:
            self.speak_dialog("need.light")
            self.comfortCounter += 1
        if self.light > 800:
            self.speak_dialog("too.much.light")
            self.comfortCounter += 1
        if self.temperature > 30:
            self.speak_dialog("too.hot")
            self.comfortCounter += 1
        if self.temperature < 10:
            self.speak_dialog("too.cold")
            self.comfortCounter += 1

        if self.comfortCounter >= 2:
            try:
                z1serial.write(b'rrr\n')
            except Exception as e:
                LOG.info(str(e))
        elif self.comfortCounter >= 1:
            try:
                z1serial.write(b'bbb\n')
            except Exception as e:
                LOG.info(str(e))
        else:
            self.speak_dialog("feeling.good")
            try:
                z1serial.write(b'ggg\n')
            except Exception as e:
                LOG.info(str(e))
        LOG.info("COMFORTCOUNTER = " + str(self.comfortCounter))
        LOG.info("water: " + str(self.water) + " lux: " + str(self.light) + " temperature: " + str(self.temperature))
        self.comfortCounter = 0


    # def handle_watered(self):
    #     updateData()
    #     logger.info(self.waterTime)
    #     if(self.waterTime==0&self.ct==0):
    #         self.speak_dialog("received.water")
    #         self.ct+=1
    #     else:
    #         self.ct=0
    #     threading.Timer(10, handle_watered).start()

    @intent_handler(IntentBuilder("").require("Water.Check"))
    def handle_water_check_intent(self, message):
        updateData()
        logger.info(self.waterTime)
        self.speak_dialog("last.time.watered", data={"waterTime": self.waterTime})  #,"time.ago")        # if self.waterTime == 0:
        #     self.speak_dialog("last.time.watered.today")
        # elif self.waterTime == 1:
        #     self.speak_dialog("last.time.watered.yesterday")
        # elif self.waterTime > 1:
        #     self.speak_dialog("last.time.watered", data={"waterTime":self.waterTime})#,"time.ago")

    @intent_handler(IntentBuilder("").require("Need.Water"))
    def handle_need_water_intent(self, message):
        self.speak_dialog("need.water")

    @intent_handler(IntentBuilder("").require("Need.Light"))
    def handle_need_water_intent(self, message):
        self.speak_dialog("need.light")

    @intent_handler(IntentBuilder("").require("Edible"))
    def handle_edible_intent(self, message):
        self.speak_dialog("edible")

    @intent_handler(IntentBuilder("").require("About"))
    def handle_need_water_intent(self, message):
        self.speak_dialog("about")


    # The "stop" method defines what Mycroft does when told to stop during
    # the skill's execution. In this case, since the skill's functionality
    # is extremely simple, there is no need to override it.  If you DO
    # need to implement stop, you should return True to indicate you handled
    # it.
    #
    # def stop(self):
    #    return False


# The "create_skill()" method is used to create an instance of the skill.
# Note that it's outside the class itself.
def create_skill():
    return FlowerBotSkill()

def updateData():
    sensorData = arduinodata.getCurrentSensorData()
    FlowerBotSkill.water = sensorData[0]
    FlowerBotSkill.light = sensorData[1]
    FlowerBotSkill.airPressure = sensorData[2]
    FlowerBotSkill.airMoisture = sensorData[3]
    FlowerBotSkill.temperature = sensorData[4]