from time import time

import cv2
import numpy as np

from src.bots.farm_bot import FarmBot
from src.bots.plant_bot import PlantBot
from src.controller import Controller
from src.runner import Runner


def create_bot():
    # return PlantBot()
    return FarmBot('enjua', 1)
    print('Olá ao WakBot Farmer 2000')
    print('O que você deseja fazer?')
    print('0 - Plantar')
    print('1 - Colher')
    result = int(input())
    if result == 0:
        print('Para plantar, você precisa de um shortcut para a semente')
        print('Em qual tecla do teclado está o shortcut?')
        result = str(input())
        return PlantBot(result)
    elif result == 1:
        print('O que você deseja colher?')
        options = FarmBot.options()
        for index, option in enumerate(options):
            print(str(index) + ' - ' + str(option))

        result = int(input())
        if result >= len(options):
            print('Ops, não temos essa opção')
            return None
        selected = options[result]
        print('Você quer colher semente ou cortar o recurso?')
        print('0 - Colher Semente')
        print('1 - Cortar Recurso')
        result = int(input())
        if result != 0 and result != 1:
            print('Ops, não temos essa opção')
            return None

        return FarmBot(selected, result)
    else:
        print('Ops, não temos essa opção')
        return None


def performance():
    loop_time = time()
    a = Controller()
    while True:
        img = a.take_screenshot()
        cv2.imshow('screen', img)

        print('FPS {}'.format(1 / (time() - loop_time)))
        loop_time = time()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    bot = create_bot()
    runner = Runner(bot, monitor_index=1)
    runner.run(False)
