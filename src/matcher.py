from os import walk
from threading import Thread, Lock

import cv2
import numpy as np

THRESHOLD_FLOOR = .90


class Matcher:
    def __init__(self, path, file_find=None, threshold=None, log=False):
        self.screenshot = None
        self.lock = Lock()
        self.stopped = True
        self.images = Matcher.files(path, file_find, log)
        self.screen = None
        self.log = log
        self.rectangles = []
        self.locations = []
        self.position = None
        self.threshold = threshold

    def update_position(self, position=None):
        self.lock.acquire()
        self.position = position
        self.lock.release()

    def update_rectangles(self, rectangles=None):
        if rectangles is None:
            rectangles = []
        self.lock.acquire()
        self.rectangles = rectangles
        self.lock.release()

    def match(self, screen, last_positions=None):
        if last_positions is None:
            last_positions = []
        self.update_position()
        self.update_rectangles()
        self.screen = screen

        if self.screen is None:
            return False

        images = self.images

        threads = []

        for index in range(len(images)):
            floor = images[index]
            thread = Thread(target=self.run, args=(floor, screen))
            threads.insert(index, thread)
            threads[index].start()

        for index in range(len(images)):
            threads[index].join()

        if not list(self.rectangles):
            return False

        def take_max_value(elem):
            return elem[4]

        self.rectangles.sort(key=take_max_value)
        while True:
            if not len(self.rectangles):
                return False
            rectangle = self.rectangles.pop(0)

            x, y, w, h, _ = rectangle
            position = (x + int(w / 2), y + int(h / 2))
            if position not in last_positions:
                break

        self.update_position(position)
        return True

    def run(self, floor, screen):
        result = cv2.matchTemplate(screen, floor, cv2.TM_CCOEFF_NORMED)

        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        if self.threshold is not None and max_val < self.threshold:
            return

        w = floor.shape[1]
        h = floor.shape[0]
        value = [int(max_loc[0]), int(max_loc[1]), int(w), int(h), max_val]

        rectangles = self.rectangles
        rectangles.append(value)
        self.update_rectangles(rectangles)

    @staticmethod
    def files(path, file_find=None, log=False):
        if file_find is None:
            file_find = []

        images = []
        for (_, dir_names, filenames) in walk(path):
            for filename in filenames:
                if file_find and filename not in file_find:
                    continue
                if '.png' not in filename:
                    continue
                file = path + '/' + filename
                images.append(cv2.imread(file))
        if not images:
            raise Exception('Images not found for path ' + path)

        return images
