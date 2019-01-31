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



class FlowerBotSkill(MycroftSkill):

    water = 0
    light = 0
    airPressure = 0
    airMoisture = 0
    temperature = 0
    waterTime = 0

    # The constructor of the skill, which calls MycroftSkill's constructor
    def __init__(self):
        super(FlowerBotSkill, self).__init__(name="FlowerBotSkill")
        # Initialize working variables used within the skill.
        sensorData = arduinodata.getCurrentSensorData()

#TODO: values need to be adjusted
    @intent_handler(IntentBuilder("").require("Flower"))
    def handle_flower_intent(self, message):
        updateData()
        logger.info(self.water)
        if self.water < 400:
            self.speak_dialog("need.water")
        elif self.water > 800:
            self.speak_dialog("too.much.water")
        elif self.light < 50:
            self.speak_dialog("need.light")
        elif self.light > 400:
            self.speak_dialog("too.much.light")
        else:
            self.speak_dialog("feeling.good")

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