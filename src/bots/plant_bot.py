import time
from random import random, sample

from src.controller import Controller
from src.matcher import Matcher

PATH_FLOOR = 'images/floor'


class PlantBot:
    @staticmethod
    def find_and_click(shortcut):
        print('Searching...')
        positions = Matcher.match(PATH_FLOOR)
        if not positions:
            print('No floors found')
            return False
        print('Found ' + str(len(positions)) + ' floors')
        position = sample(positions, 1)[0]

        time.sleep(0.2 + random() / 2)
        Controller.press(shortcut)
        Controller.click(position)
        time.sleep(2)
        return True

    @staticmethod
    def run(shortcut):
        time.sleep(3)
        positions = Matcher.match(PATH_FLOOR)
        position = positions[0]
        Controller.click(position, right=True)
        while True:
            start = time.time()
            if not PlantBot.find_and_click(shortcut):
                break
            end = time.time()
            result_time = end - start
            print('Finished in ' + str(result_time) + 's')

