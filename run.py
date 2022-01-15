from src.main import create_bot
from src.runner import Runner


bot = create_bot()
runner = Runner(bot, monitor_index=2)
runner.run()