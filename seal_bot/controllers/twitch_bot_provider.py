import os
import time
import logging
import datetime
import threading
import asyncio
from twitchio.ext import commands

logger = logging.getLogger(__name__)

class TwitchBot(commands.Bot):

    def __init__(self, dot_env_config: dict, seal_coin_service):
        self.dot_env_config = dot_env_config
        self.seal_coin_service = seal_coin_service
        super().__init__(
            irc_token=dot_env_config['TMI_TOKEN'],
            client_id=dot_env_config['CLIENT_ID'],
            nick=dot_env_config['BOT_NICK'],
            prefix=dot_env_config['BOT_PREFIX'],
            initial_channels=[dot_env_config['CHANNEL']]
        )

# this function will be triggered when your bot join the char room
# it will send a "/me has landed" message
    async def event_ready(self):
        'Called once when the bot goes online.'
        print(f"{self.dot_env_config['BOT_NICK']} is online!")
        # await self._ws.send_privmsg(self.dot_env_config['CHANNEL'], f"/me has landed!")

# a hello reploy event, but i don't want now
    async def event_message(self, message):
        await self.handle_commands(message)
        logger.debug("user: " + message._author.name, " message: ", message.content)

# this function will be triggered when sombody sat !test, it will reply test passwed!
    @commands.command(name='test')
    async def test(self, ctx):
        await ctx.send('test passed!')

    async def event_join(self, user):
        self.seal_coin_service.add_audience(user.name)
        logger.debug("user join: " + user.name)

    async def event_part(self, user):
        self.seal_coin_service.remove_audience(user.name)
        logger.debug("user leave: " + user.name)
# # this function is a scheduler, which will ask you to eat something when 02:07 AM
# async def timer_function():
#     while True:
#         time.sleep(60)
#         now = datetime.datetime.now().strftime("%H:%M")
#         print(now)
#         if now == "02:07":
#             chan = bot.get_channel(os.environ['CHANNEL'])
#             await chan.send("半夜 02:07 啦，大家吃宵夜沒")
#             del chan

# to make timer_function to become a callback function for threading
# def timer_function_worker():
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     loop.run_until_complete(timer_function())
#     loop.close()