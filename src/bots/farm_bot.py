import time

import yaml
from src.filters.filter_applier import FilterApplier

from src.bots.bot import Bot
from src.controller import Controller
from src.matcher import Matcher

PATH_FARM = 'images/farm'
PATH_BUTTON = 'images/buttons'
PATH_BUTTON_GATHER = 'gather.png'
PATH_BUTTON_HARVEST = 'harvest.png'


class FarmBotState:
    INITIALIZING = 1
    SEARCHING = 2
    MOVING = 3
    SEARCHING_BUTTON = 4


class FarmBot(Bot):
    MOVEMENT_STOPPED_THRESHOLD = 0.99

    ACTIONS = {
        0: PATH_BUTTON_GATHER,
        1: PATH_BUTTON_HARVEST,
    }

    def __init__(self, farm, action):
        super().__init__()
        if not any(actionKey == action for actionKey in FarmBot.ACTIONS.keys()):
            raise Exception('Action {} is Not valid'.format(str(action)))

        if not any(farmName == farm for farmName in FarmBot.options()):
            raise Exception('Farm {} is Not valid'.format(str(farm)))

        button_img = FarmBot.ACTIONS[action]
        self.path = PATH_FARM + '/' + farm
        self.name = farm
        self.matcher_plant = Matcher(self.path, threshold=0.5)
        self.matcher_button = Matcher(PATH_BUTTON, threshold=0.8, file_find=[button_img])
        self.state = FarmBotState.SEARCHING
        self.has_captcha = True
        self.controller = None
        self.load_filter()

    def load_filter(self):
        file = self.path + '/' + self.name
        if FilterApplier.has_file(file):
            self.filter = FilterApplier.load_filter(self.path, self.name)
            self.has_filter = True

    def search(self):
        print('Searching Plant')
        found = self.matcher_plant.match(self.screen, self.last_positions)

        if not found:

            print('No plants found')
            self.stop()
            return False
        self.update_position(self.matcher_plant.position)
        self.controller.click(self.position, right=True)
        self.update_state(FarmBotState.SEARCHING_BUTTON)
        return True

    def search_button(self):
        print('Searching Button')
        success = self.matcher_button.match(self.screen)
        if not success:
            print('Button Not found, going to next plant')
            self.last_positions.append(self.position)
            self.update_state(FarmBotState.SEARCHING)
            return False
        self.last_positions = []
        print('Button Found')
        self.update_position(self.matcher_button.position)
        self.controller.click(self.position)
        self.update_state(FarmBotState.MOVING)
        print('Started Moving')

        return True

    def check_movement(self):
        if self.is_moving():
            return
        print('Stopped Moving')
        time.sleep(2)
        self.update_state(FarmBotState.SEARCHING)

    def run(self):
        if self.controller is None:
            raise Exception('Missing Controller on Bot')
        
        while not self.stopped:
            if not self.has_screen() or self.captcha_on_screen:
                continue
            elif self.state == FarmBotState.SEARCHING:
                self.search()
            elif self.state == FarmBotState.SEARCHING_BUTTON:
                self.search_button()
            elif self.state == FarmBotState.MOVING:
                self.check_movement()

    @staticmethod
    def options():
        with open("farm.yml", 'r') as stream:
            data_loaded = yaml.safe_load(stream)
            return data_loaded['farm']
