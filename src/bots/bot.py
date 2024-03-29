import time
from threading import Lock, Thread

import cv2


class Bot:
    MOVEMENT_STOPPED_THRESHOLD = 0.99

    def __init__(self):
        self.screen = None
        self.last_screen = None
        self.lock = Lock()
        self.stopped = True
        self.position = None
        self.state = None
        self.filter = None
        self.has_filter = False
        self.captcha_on_screen = False
        self.has_captcha = False
        self.has_target = False
        self.last_positions = []

    def get_screen(self):
        return self.screen

    def has_screen(self):
        return self.screen is not None

    def update_screen(self, screen):
        self.lock.acquire()
        self.screen = screen
        self.lock.release()

    def update_state(self, state):
        self.lock.acquire()
        self.state = state
        self.lock.release()

    def update_position(self, position):
        self.lock.acquire()
        self.position = position
        self.lock.release()

    def update_captcha_on_screen(self, captcha_on_screen):
        self.lock.acquire()
        self.captcha_on_screen = captcha_on_screen
        self.lock.release()

    def update_has_target(self, has_target):
        self.lock.acquire()
        self.has_target = has_target
        self.lock.release()

    def is_stopped(self):
        return not self.is_moving()

    def is_moving(self):
        if self.last_screen is None:
            self.last_screen = self.screen.copy()
            return True

        result = cv2.matchTemplate(self.screen, self.last_screen, cv2.TM_CCOEFF_NORMED)
        similarity = result[0][0]
        # print('Movement detection similarity: {}'.format(similarity))
    
        if similarity >= self.MOVEMENT_STOPPED_THRESHOLD:
            # print('Movement detected stop')
            return False

        self.last_screen = self.screen.copy()
        return True

    def start(self):
        self.stopped = False
        t = Thread(target=self.run)
        t.start()

    def run(self):
        raise Exception('Missing method run')

    def stop(self):
        self.stopped = True
