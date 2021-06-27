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
        await self._ws.send_privmsg(self.dot_env_config['CHANNEL'], f"全台最火豹的上線賭場上線啦!!女裝科科在線發牌，陪您一起嗨翻天～請大家排隊進場 SeemsGood")

# log all message in chat
    async def event_message(self, message):
        await self.handle_commands(message)
        logger.info("user: " + message._author.name + " message: " + message.content)

# this function will be triggered when sombody sat !test, it will reply test passwed!
    # @commands.command(name='test')
    # async def test(self, ctx):
    #     await ctx.send('test passed!')

    @commands.command(name='查帳', aliases=['p', 'P'])
    async def query_coin(self, ctx):
        logger.info("Get query coin command: " + ctx.author.name + " arg: " + str(ctx.args))
        try:
            coin = self.seal_coin_service.query_coin(ctx.author.name)
            await ctx.send(f'@{ctx.author.name} 你現在有 {coin} 豹仔幣')
        except:
            await ctx.send(f'@{ctx.author.name} 目前豹仔銀行查不到你的存款喔 QQ')

    @commands.command(name='賭', aliases=['r', 'R'])
    async def gamble(self, ctx, gamble_arg):
        # logger.info("Get gamble command: " + ctx.author.name + " arg: " + str(ctx.args))
        print("Get gamble command: ", ctx.author.name, " arg: ", gamble_arg)
        gamble_result_message = self.seal_coin_service.gamble(ctx.author.name, gamble_arg)
        await ctx.send(gamble_result_message)        

    @commands.command(name="給錢",  aliases=['give'])
    async def give_coin(self, ctx, receiver, num_of_coin):
        logger.info("Get give coin command: " + ctx.author.name + " arg: " + str(ctx.args))
        give_result = self.seal_coin_service.give_coin(ctx.author.name, receiver, num_of_coin, False)
        await ctx.send(give_result)

    # only mod can use this command
    @commands.command(name="發錢", aliases=['mod_give'])
    async def give_coin_by_mod(self, ctx, receiver, num_of_coin):
        logger.info("Get give coin command" + ctx.author.name + " arg: " + str(ctx.args))
        if not ctx.author.is_mod:
            await ctx.send(f"{ctx.author.name} 不是 mod 不能使用這個指令喔 WutFace")
        give_result = self.seal_coin_service.give_coin(ctx.author.name, receiver, num_of_coin, True)
        await ctx.send(give_result)

    async def event_join(self, user):
        self.seal_coin_service.add_audience(user.name)
        logger.info("user join: " + user.name)

    async def event_part(self, user):
        self.seal_coin_service.remove_audience(user.name)
        logger.info("user leave: " + user.name)
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