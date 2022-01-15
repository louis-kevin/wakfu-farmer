from src.bots.bot import Bot
from src.matcher import Matcher

PATH_CAPTCHA = 'images/captcha/mob'
PATH_MOB = 'mob.png'


class CaptchaBot(Bot):
    def __init__(self):
        super().__init__()
        self.matcher = Matcher(PATH_CAPTCHA, threshold=0.8)

    def run(self):
        while not self.stopped:
            if not self.has_screen():
                continue

            found = self.matcher.match(self.screen)
            self.update_captcha_on_screen(found)
            if found:
                self.update_position(self.matcher.position)
