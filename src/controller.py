import time
from random import random
from threading import Lock, Thread

import mss

import cv2
import numpy as np
import pyautogui

from utils import add_randomness, get_random_tween


class Controller:
    OFFSET_Y = 50

    def __init__(self, monitor_index=3):
        self.lock = Lock()
        self.monitor = Controller.monitor(monitor_index)
        self.sct = mss.mss()
        self.stopped = True
        self.screenshot = None

    def take_screenshot(self):
        screenshot = self.sct.grab(self.monitor)
        screenshot = np.array(screenshot)
        screenshot = np.flip(screenshot[:, :, :3], 2)
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2RGB)
        y = self.OFFSET_Y
        x = 0
        h = self.monitor['height'] - 200
        w = self.monitor['width']
        screenshot = screenshot[y:y + h, x:x + w]
        return screenshot

    def update_screenshot(self, screenshot=None):
        self.lock.acquire()
        self.screenshot = screenshot
        self.lock.release()

    def start(self):
        self.stopped = False
        t = Thread(target=self.run)
        t.start()

    def stop(self):
        self.stopped = True

    def run(self):
        start = time.time()
        while not self.stopped:
            screenshot = self.take_screenshot()
            self.update_screenshot(screenshot)
            # print('FPS '+str(1/(time.time() - start)))
            start = time.time()

    @staticmethod
    def click(position, right=False, duration=None):
        if duration is None:
            duration = 0.2 + random() / 2
        x, y = position
        y += Controller.OFFSET_Y
        monitor = Controller.monitor()
        real_x = monitor['left'] + x
        real_y = monitor['top'] + y
        if position != pyautogui.position():
            pyautogui.moveTo(add_randomness(real_x, 2), add_randomness(real_y, 2), duration,
                             tween=get_random_tween())
        if duration is not None:
            time.sleep(duration)
        if right:
            pyautogui.rightClick()
        else:
            pyautogui.click()
        time.sleep(0.1 + random() / 2)

    @staticmethod
    def press(key):
        pyautogui.press(key)

    @staticmethod
    def monitor(monitor_index=3):
        monitors = Controller.monitors()
        return monitors[monitor_index]

    @staticmethod
    def monitors():
        sct = mss.mss()
        return sct.monitors
