import time
from random import random, sample
from threading import Lock

from src.bots.bot import Bot
from src.controller import Controller
from src.filters.filter_applier import FilterApplier
from src.matcher import Matcher

PATH_FLOOR = 'images/floor'
PATH_ICON = 'icons'


class PlantBotState:
    INITIALIZING = 1
    SEARCHING = 2
    MOVING = 3


class PlantBot(Bot):
    FARM_NAME = 'floor'

    def __init__(self, shortcut='2'):
        super().__init__()
        self.path = PATH_FLOOR
        self.name = self.FARM_NAME
        self.matcher = Matcher(PATH_FLOOR, threshold=0.32)
        self.state = PlantBotState.INITIALIZING
        self.shortcut = shortcut
        self.filter_floor = FilterApplier.load_filter(PATH_FLOOR, self.FARM_NAME, from_control=True)
        self.filter = self.filter_floor
        self.has_filter = True
        self.processed_screen = None

    def search_floor(self):
        print('Searching Floor')
        self.processed_screen = self.filter.apply(self.screen)
        found = self.matcher.match(self.processed_screen)
        if not found:
            print('No Floor found')
            self.stop()
            return
        self.update_position(self.matcher.position)

    def focus(self):
        print('Clicking')
        Controller.click(self.position)
        print('Moving')
        self.update_state(PlantBotState.MOVING)

    def plant(self):
        print('Clicking with right')
        Controller.click(self.position, right=True)
        print('Pressing ' + self.shortcut)
        Controller.press(self.shortcut)
        time.sleep(random() / 2)
        print('Clicking')
        Controller.click(self.position)
        print('Moving')
        self.update_state(PlantBotState.MOVING)

    def run(self):
        while not self.stopped:
            if not self.has_screen():
                continue
            elif self.state == PlantBotState.INITIALIZING:
                self.search_floor()
                self.focus()

            elif self.state == PlantBotState.SEARCHING:
                self.search_floor()
                self.plant()

            elif self.state == PlantBotState.MOVING and self.is_stopped():
                print('Planting')
                time.sleep(4)
                self.update_state(PlantBotState.SEARCHING)
