import time
from os import walk
from threading import Thread

import cv2

from controller import Controller
from logger import Logger

THRESHOLD_FLOOR = .90


class Matcher(Thread):
    @staticmethod
    def match(path, log=False, file_find=None, threshold=THRESHOLD_FLOOR):
        if file_find is None:
            file_find = []
        images = []
        if log:
            print('Finding Images in ' + path)
        for (_, dir_names, filenames) in walk(path):
            for filename in filenames:
                if file_find and not any(x == filename for x in file_find):
                    continue
                file = path + '/' + filename
                images.append(cv2.imread(file))
        if not images:
            raise Exception('Images not found for path ' + path)
        if log:
            print('Found ' + str(len(images)) + ' in ' + path)
            print('Taking a Screenshot')
        screen = Controller.screenshot()

        rectangles = []
        threads = []
        if log:
            print('Creating Matchers')
        for index in range(len(images)):
            floor = images[index]
            threads.insert(index, Matcher(screen, floor, index, threshold, log))
            threads[index].start()

        for index in range(len(images)):
            threads[index].join()
            rectangles += threads[index].rectangles

        rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.25)
        positions = []
        for x, y, w, h in rectangles:
            position = (x + int(w / 2), y + int(h / 2))
            positions.append(position)

        if log:
            Logger.show_rectangles(rectangles, screen)

        return positions

    def __init__(self, screen, floor, index, threshold, logs=False):
        Thread.__init__(self)
        self.screen = screen
        self.floor = floor
        self.rectangles = []
        self.index = index
        self.logs = logs
        self.threshold = threshold

    def run(self):
        start = 0
        if self.logs:
            print('\nThread ' + str(self.index) + ' Running')
            start = time.time()
        scale = 0.5
        a = cv2.resize(self.screen, (0, 0), fx=scale, fy=scale)
        b = cv2.resize(self.floor, (0, 0), fx=scale, fy=scale)
        a = cv2.cvtColor(a, cv2.COLOR_BGR2GRAY)
        b = cv2.cvtColor(b, cv2.COLOR_BGR2GRAY)

        result = cv2.matchTemplate(a, b, cv2.TM_CCOEFF_NORMED)

        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        w = self.floor.shape[1]
        h = self.floor.shape[0]
        self.rectangles.append([int(max_loc[0]), int(max_loc[1]), int(w), int(h)])
        self.rectangles.append([int(max_loc[0]), int(max_loc[1]), int(w), int(h)])

        if self.logs:
            end = time.time()
            result_time = end - start
            print('Thread ' + str(self.index) + ' Finished in ' + str(result_time) + 's')
        return self.rectangles
