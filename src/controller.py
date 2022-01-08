import time
from random import random

import cv2
import numpy as np
import pyautogui

from utils import add_randomness


class Controller:
    @staticmethod
    def click(position, right=False):
        duration = 0.2 + random() / 2
        x, y = position
        if position != pyautogui.position():
            pyautogui.moveTo(add_randomness(x - 10, 2), add_randomness(y - 10, 2), duration, tween=pyautogui.easeInQuad)
        time.sleep(duration)
        if right:
            pyautogui.rightClick()
        else:
            pyautogui.click()

    @staticmethod
    def drag(positions):
        duration = 0.2 + random() / 2
        x, y = positions[0]
        pyautogui.moveTo(add_randomness(x - 10, 2), add_randomness(y - 10, 2), duration, tween=pyautogui.easeInQuad)
        time.sleep(duration)

        for position in positions:
            duration = 0.2 + random() / 2
            x, y = position
            pyautogui.dragTo(x, y, duration, button='left')
            time.sleep(duration)

    @staticmethod
    def press(key):
        pyautogui.press(key)

    @staticmethod
    def screenshot():
        img = pyautogui.screenshot('screen.png')
        return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
