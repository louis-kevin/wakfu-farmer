from src.bots.farm_bot import FarmBot
from src.main import create_bot
from src.runner import Runner


bot = FarmBot('dendro',1)
runner = Runner(bot, monitor_index=2)
runner.run(show=False)