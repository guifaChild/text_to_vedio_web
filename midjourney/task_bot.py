from os import getenv

import __init__  # noqa
from midjourney.exceptions import MissRequiredVariableError
from midjourney.task.bot.listener import bot

BOT_TOKEN = getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise MissRequiredVariableError("Missing required environment variable: [BOT_TOKEN]")


def start_robot():
    bot.run(BOT_TOKEN)
    print("机器人启动成功")
if __name__ == '__main__':
    bot.run(BOT_TOKEN)
