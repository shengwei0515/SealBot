import os
import time
import datetime
import threading
import asyncio
from twitchio.ext import commands

class TwitchBot(commands.Bot):

    def __init__(self, dot_env_config: dict):
        self.dot_env_config = dot_env_config
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
        print(message._author.name, " ", message.content)

# this function will be triggered when sombody sat !test, it will reply test passwed!
    @commands.command(name='test')
    async def test(self, ctx):
        await ctx.send('test passed!')

    async def event_join(self, user):
        print("join: " + user.name)

    async def event_part(self, user):
        print("leave: " + user.name)
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