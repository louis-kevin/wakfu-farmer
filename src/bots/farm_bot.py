import time

import yaml
from random import random, sample

from src.bots.catpcha_bot import CaptchaBot
from src.controller import Controller
from src.matcher import Matcher, THRESHOLD_FLOOR

PATH_FARM = 'images/farm'
PATH_BUTTON = 'images/buttons'
PATH_BUTTON_GATHER = 'gather.png'
PATH_BUTTON_HARVEST = 'harvest.png'
last_position = None

class FarmBot:
    @staticmethod
    def options():
        with open("farm.yml", 'r') as stream:
            data_loaded = yaml.safe_load(stream)
            return data_loaded['farm']

    @staticmethod
    def find_gather_button():
        positions_buttons = Matcher.match(PATH_BUTTON, file_find=[PATH_BUTTON_GATHER], log=False)
        if not positions_buttons:
            return
        return positions_buttons[0]

    @staticmethod
    def find_harvest_button():
        positions_buttons = Matcher.match(PATH_BUTTON, file_find=[PATH_BUTTON_HARVEST], log=False)
        if not positions_buttons:
            return
        return positions_buttons[0]

    @staticmethod
    def find_and_click(path, find_button, log=False, threshold=THRESHOLD_FLOOR):
        positions = Matcher.match(path, log=log, threshold=threshold)
        if not positions:
            raise Exception('No Items found')

        print('Found ' + str(len(positions)) + ' items')
        print('Collecting...')
        position = sample(positions, 1)[0]
        Controller.click(position, right=True)
        time.sleep(0.1 + random() / 2)
        button = find_button()
        if not button:
            print('No Button have been found')
            return False
        Controller.click(button)
        time.sleep(1)
        print('Collected')
        return True

    @staticmethod
    def run(farm, action):
        action_method = FarmBot.find_harvest_button if action == 1 else FarmBot.find_gather_button
        path = PATH_FARM + '/' + farm
        while True:
            start = time.time()
            print('Searching for ' + farm + '...')
            result = FarmBot.find_and_click(path, action_method, log=False)
            end = time.time()
            result_time = end - start
            print('Finished in ' + str(result_time) + 's')
            if not result:
                continue
