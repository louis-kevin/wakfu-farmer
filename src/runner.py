import cv2
from pynput import mouse

from src.bots.catpcha_bot import CaptchaBot
from src.controller import Controller
from src.filters.filter_controller import FilterController


class Runner:
    def __init__(self, bot, captcha=False, monitor_index=3):
        self.controller = Controller(monitor_index)
        self.captcha_bot = CaptchaBot()
        self.bot = bot
        self.captcha = captcha
        self.stopped = False
        self.listener = mouse.Listener(on_click=self.on_click)

    def on_click(self, ___, __, button, _):
        if mouse.Button.middle == button:
            self.stopped = True
            print('Stopping')
            return False

    def show(self, position=None, screen=None):
        if screen is None:
            screen = self.bot.get_screen()
        if screen is None:
            return

        if position is None:
            position = self.bot.position

        if position:
            cv2.circle(screen, position, 2, (0, 255, 0), 2)
        cv2.imshow('screen', screen)
        cv2.waitKey(1)

    def init_gui_filter(self):
        if self.bot.has_filter:
            FilterController.init_control_gui(self.bot.filter)

    def run(self, show=True):
        self.init_gui_filter()
        self.listener.start()
        self.controller.start()
        self.bot.start()
        captcha = self.captcha
        if captcha:
            self.captcha_bot.start()

        while not self.stopped:
            screen = self.controller.screenshot
            if screen is None:
                continue
            if captcha:
                self.captcha_bot.update_screen(screen)
                self.bot.update_has_captcha(self.captcha_bot.has_captcha)
            self.bot.update_screen(screen)
            self.show()
            key = cv2.waitKey(1) & 0xFF
            if key == ord('s'):
                FilterController.save(self.bot.path, self.bot.name)

        self.controller.stop()
        self.bot.stop()
        self.captcha_bot.stop()
        exit()
