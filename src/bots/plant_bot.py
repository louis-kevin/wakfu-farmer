import time

from src.bots.bot import Bot
from src.controller import Controller
from src.filters.filter_applier import FilterApplier
from src.matcher import Matcher

PATH_FLOOR = 'images/floor'
PATH_SELECTED_FLOOR = 'images/selected_floor'


class PlantBotState:
    INITIALIZING = 1
    SEARCHING = 2
    PLANTING = 3
    MOVING = 4


class PlantBot(Bot):
    FARM_NAME = 'floor'
    SELECTED_FLOOR_NAME = 'selected_floor'

    def __init__(self, shortcut='2'):
        super().__init__()
        self.matcher = Matcher(PATH_FLOOR, threshold=0.32)
        self.selected_matcher = Matcher(PATH_SELECTED_FLOOR, threshold=0.4)
        self.state = PlantBotState.INITIALIZING
        self.shortcut = shortcut
        self.filter_floor = FilterApplier.load_filter(PATH_FLOOR, self.FARM_NAME, from_control=False)
        self.filter_selected_floor = FilterApplier.load_filter(PATH_SELECTED_FLOOR, self.SELECTED_FLOOR_NAME, from_control=False)
        # self.filter = self.filter_floor
        # self.has_filter = True
    
    def get_screen(self):
        return self.filter_floor.apply(self.screen)
    
    def search_floor(self):
        print('Searching Floor')
        processed_screen = self.filter_floor.apply(self.screen)
        found = self.matcher.match(processed_screen, self.last_positions)
        if not found:
            print('No Floor found')
            return False
        self.update_position(self.matcher.position)
        self.controller.move(self.position)
        return True

    def has_selected_floor(self):
        print('Searching Selected Floor')
        processed_screen = self.filter_selected_floor.apply(self.screen)
        found = self.selected_matcher.match(processed_screen)
        if not found:
            print('No Selected Floor found')
            return False
        print('Has floor selected')
        return True

    def focus(self):
        print('Clicking')
        self.controller.click()

    def plant(self):
        if not self.has_selected_floor():
            print('Clicking with right')
            self.controller.click(right=True)
            print('Pressing ' + self.shortcut)
            Controller.press(self.shortcut)
            time.sleep(0.1)
       
        if not self.has_selected_floor():
            self.last_positions.append(self.position)
            self.update_state(PlantBotState.SEARCHING)
            return
        self.last_positions = []
        print('Clicking')
        self.controller.click()
        print('Planting')

    def run(self):
        while not self.stopped:
            if not self.has_screen():
                continue
            elif self.state == PlantBotState.INITIALIZING:
                success = self.search_floor()
                if not success:
                    continue
                self.focus()
                self.update_state(PlantBotState.SEARCHING)
            elif self.is_moving():
                print('Moving')
                time.sleep(0.5)
                continue
            elif self.state == PlantBotState.SEARCHING:
                success = self.search_floor()
                if not success:
                    continue
                self.update_state(PlantBotState.PLANTING)
            elif self.state == PlantBotState.PLANTING:
                self.plant()
                self.update_state(PlantBotState.SEARCHING)
                
