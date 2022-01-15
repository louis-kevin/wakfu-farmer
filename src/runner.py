import cv2
from pynput import mouse

from src.controller import Controller
from src.filters.filter_controller import FilterController


class Runner:
    def __init__(self, bot, captcha=False, monitor_index=3):
        self.controller = Controller(monitor_index)
        self.bot = bot
        self.captcha = captcha
        self.stopped = False
        self.listener = mouse.Listener(on_click=self.on_click)

    def on_click(self, ___, __, button, _):
        if mouse.Button.middle == button:
            self.stopped = True
            print('Stopping')
            return False

    def show(self):
        img = self.bot.get_screen()
        if img is None:
            return
        position = self.bot.position
        if position:
            cv2.circle(img, position, 2, (0, 255, 0), 2)
        cv2.imshow('screen', img)
        cv2.waitKey(1)

    def init_gui_filter(self):
        if self.bot.has_filter:
            FilterController.init_control_gui(self.bot.filter)

    def run(self, show=True):
        self.listener.start()
        self.controller.start()
        self.bot.start()

        while not self.stopped:
            if self.controller.screenshot is None:
                continue
            self.bot.update_screen(self.controller.screenshot)
            if show:
                self.show()
            key = cv2.waitKey(1) & 0xFF
            if key == ord('s'):
                FilterController.save(self.bot.path, self.bot.name)

        self.controller.stop()
        self.bot.stop()
        exit()
