from src.bots.farm_bot import FarmBot
from src.bots.plant_bot import PlantBot


def run():
    print('Olá ao WakBot Farmer 2000')
    print('O que você deseja fazer?')
    print('0 - Plantar')
    print('1 - Colher')
    result = int(input())
    if result == 0:
        print('Para plantar, você precisa de um shortcut para a semente')
        print('Em qual tecla do teclado está o shortcut?')
        result = str(input())
        PlantBot.run(result)
    elif result == 1:
        print('O que você deseja colher?')
        options = FarmBot.options()
        for index, option in enumerate(options):
            print(str(index) + ' - ' + str(option))

        result = int(input())
        if result >= len(options):
            print('Ops, não temos essa opção')
            return
        selected = options[result]
        print('Você quer colher semente ou cortar o recurso?')
        print('0 - Colher Semente')
        print('1 - Cortar Recurso')
        result = int(input())
        if result != 0 and result != 1:
            print('Ops, não temos essa opção')
            return

        FarmBot.run(selected, result)
    else:
        print('Ops, não temos essa opção')


if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        print(e)
