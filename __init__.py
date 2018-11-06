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
from arduinodata import getCurrentSensorData


# Each skill is contained within its own class, which inherits base methods
# from the MycroftSkill class.  You extend this class as shown below.

# TODO: Change "Template" to a unique name for your skill
class FlowerBotSkill(MycroftSkill):

    # The constructor of the skill, which calls MycroftSkill's constructor
    def __init__(self):
        super(FlowerBotSkill, self).__init__(name="FlowerBotSkill")

        # Initialize working variables used within the skill.
        sensorData = getCurrentSensorData
        self.count = 0
        self.water = sensorData[0]
        self.light = sensorData[1]
        self.airPressure = sensorData[2]
        self.airMoisture = sensorData[3]
        self.temperature = sensorData[4]
        self.waterTime = 0

        @intent_handler(IntentBuilder("").require("Count").require("Dir"))

    # def handle_count_intent(self, message):
    #     if message.data["Dir"] == "up":
    #         self.count += 1
    #     else:  # assume "down"
    #         self.count -= 1
    #     self.speak_dialog("count.is.now", data={"count": self.count})

        @intent_handler(IntentBuilder("").require("Flower"))
        def handle_flower_intent(self, message):
            if self.water < 350:
                self.speak_dialog("need.water")
            elif self.water > 900:
                self.speak_dialog("too.much.water")
            elif self.light < 50:
                self.speak_dialog("need.light")
            elif self.light > 400:
                self.speak_dialog("too.much.light")
            else:
                self.speak_dialog("feeling.good")

    @intent_handler(IntentBuilder("").require("Water.Check"))
    def handle_water_check_intent(self, message):
        if self.waterTime == 0:
            self.speak_dialog("last.time.watered.today")
        elif self.waterTime == 1:
            self.speak_dialog("last.time.watered.yesterday")
        elif self.waterTime > 1:
            self.speak_dialog("last.time.watered", data ={"waterTime":self.waterTime})#,"time.ago")

    # @intent_handler(IntentBuilder("").require("Need.Water")
    # def handle_need_water_intent(self, message)
    #     self.speak_dialog("need.water")

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
