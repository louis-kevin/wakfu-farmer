import cv2
from pynput import mouse

from src.bots.catpcha_bot import CaptchaBot
from src.bots.plant_bot import PlantBot
from src.controller import Controller
from src.filters.filter_controller import FilterController


class RunnerState:
    FARMING = 0
    PLANTING = 1


class Runner:
    def __init__(self, bot, monitor_index=3):
        self.controller = Controller(monitor_index)
        self.captcha_bot = CaptchaBot()
        self.bot = bot
        self.bot.controller = self.controller
        self.captcha = bot.has_captcha
        self.stopped = False
        self.listener = mouse.Listener(on_click=self.on_click)
        self.listener.start()

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

    def update_screen_on_bot(self, bot, screen):
        if bot.stopped:
            bot.start()
            return

        if bot.has_captcha:
            self.captcha_bot.update_screen(screen)
            bot.update_captcha_on_screen(self.captcha_bot.captcha_on_screen)
        bot.update_screen(screen)
        return bot.has_target

    def run(self, show=True):
        self.init_gui_filter()
        self.controller.start()
        self.bot.start()
        captcha = self.captcha
        if captcha:
            self.captcha_bot.start()

        while not self.stopped:
            screen = self.controller.screenshot
            if screen is None:
                continue
            self.update_screen_on_bot(self.bot, screen)
            if show:
                self.show()
            key = cv2.waitKey(1) & 0xFF
            if key == ord('s') and self.bot.has_filter:
                filter = self.bot.filter
                if filter:
                    FilterController.save(filter.path, filter.name)

        self.controller.stop()
        self.bot.stop()
        self.captcha_bot.stop()
        exit()
