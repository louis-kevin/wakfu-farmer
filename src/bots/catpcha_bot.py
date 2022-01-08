from src.matcher import Matcher

PATH_CAPTCHA = 'images/captcha'
PATH_MOB = 'mob.png'


class CaptchaBot:
    @staticmethod
    def has_captcha():
        positions = Matcher.match(PATH_CAPTCHA, file_find=[PATH_MOB])
        if not positions:
            return False

        return True
