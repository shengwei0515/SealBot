import os
import sys
import logging
import threading
from dotenv import dotenv_values
from controllers.twitch_bot_provider import TwitchBot
from services.seal_coin import SealCoinService

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)

logger.addHandler(handler)


if __name__ == "__main__":
    seal_coin_service = SealCoinService()


    config = dotenv_values(".env") 
    twitch_bot = TwitchBot(config, seal_coin_service)

    thread_coin_service = threading.Thread(target=seal_coin_service.start_share_coin, args=()) 
    thread_coin_service.start()

    # setup bot thread, it should be the final thread to be setup in main
    thread_bot = threading.Thread(target=twitch_bot.run, args=()) 
    thread_bot.start()

    # # use join to run forever
    thread_bot.join()
    thread_coin_service.join()