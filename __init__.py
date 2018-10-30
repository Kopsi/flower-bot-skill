from mycroft import MycroftSkill, intent_file_handler


class FlowerBot(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('bot.flower.intent')
    def handle_bot_flower(self, message):
        self.speak_dialog('bot.flower')


def create_skill():
    return FlowerBot()

