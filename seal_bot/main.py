import os
import threading
from dotenv import dotenv_values
from controllers.twitch_bot_provider import TwitchBot

if __name__ == "__main__":
    config = dotenv_values(".env") 
    twitch_bot = TwitchBot(config)
    # twitch_bot.run()
    # # setup scheduler thread
    # thread_timer = threading.Thread(target=twitchbot.timer_function_worker, args=()) 
    # thread_timer.start()

    # setup bot thread, it should be the final thread to be setup in main
    thread_bot = threading.Thread(target=twitch_bot.run, args=()) 
    thread_bot.start()

    # # use join to run forever
    thread_bot.join()
    # thrthread_timeread_bot.join()