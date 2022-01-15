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
        self.selected_matcher = Matcher('images', file_find=['selected_floor.png'], threshold=0.67)
        self.state = PlantBotState.INITIALIZING
        self.shortcut = shortcut
        self.filter_floor = FilterApplier.load_filter(PATH_FLOOR, self.FARM_NAME, from_control=True)
        self.filter = self.filter_floor
        self.has_filter = True
        self.processed_screen = None

    def search_floor(self):
        print('Searching Floor')
        self.processed_screen = self.filter.apply(self.screen)
        found = self.matcher.match(self.processed_screen, self.last_positions)
        if not found:
            print('No Floor found')
            self.stop()
            return
        self.update_position(self.matcher.position)

    def has_selected_floor(self):
        print('Searching Selected Floor')
        self.processed_screen = self.filter.apply(self.screen)
        found = self.selected_matcher.match(self.screen)
        if not found:
            print('No Selected Floor found')
            return False
        return True

    def focus(self):
        print('Clicking')
        Controller.click(self.position)
        print('Moving')
        self.update_state(PlantBotState.MOVING)

    def plant(self):
        if not self.has_selected_floor():
            print('Clicking with right')
            Controller.click(self.position, right=True)
        print('Pressing ' + self.shortcut)
        Controller.press(self.shortcut)
        time.sleep(random() / 2)
        if not self.has_selected_floor():
            self.last_positions.append(self.position)
            return
        self.last_positions = []
        print('Clicking')
        Controller.click(self.position)
        print('Moving')
        self.update_state(PlantBotState.MOVING)
        print('Planting')

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
                self.update_state(PlantBotState.SEARCHING)
