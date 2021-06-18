import os
import time
import datetime
import threading
import asyncio
from dotenv import load_dotenv
from twitchio.ext import commands

# load environment variables from .env file
load_dotenv()

# set up the bot
bot = commands.Bot(
    irc_token=os.environ['TMI_TOKEN'],
    client_id=os.environ['CLIENT_ID'],
    nick=os.environ['BOT_NICK'],
    prefix=os.environ['BOT_PREFIX'],
    initial_channels=[os.environ['CHANNEL']]
)

# this function will be triggered when your bot join the char room
# it will send a "/me has landed" message
@bot.event
async def event_ready():
    'Called once when the bot goes online.'
    print(f"{os.environ['BOT_NICK']} is online!")
    ws = bot._ws  # this is only needed to send messages within event_ready
    await ws.send_privmsg(os.environ['CHANNEL'], f"/me has landed!")

# a hello reploy event, but i don't want now
# @bot.event
# async def event_message(ctx):
#     'Runs every time a message is sent in chat.'

#     # make sure the bot ignores itself and the streamer
#     if ctx.author.name.lower() == os.environ['BOT_NICK'].lower():
#         return

#     await bot.handle_commands(ctx)

#     # await ctx.channel.send(ctx.content)

#     if 'hello' in ctx.content.lower():
#         await ctx.channel.send(f"Hi, @{ctx.author.name}!")

# this function will be triggered when sombody sat !test, it will reply test passwed!
@bot.command(name='test')
async def test(ctx):
    await ctx.send('test passed!')

# this function will be triggered when sombody sat !ok, it will reply some cool worlds!
@bot.command(name='ok56')
async def test(ctx):
    await ctx.send('@是伍陸: 幹嘛 先ALL IN再來跟我說話')

# this function will monitor all messages in the chat room and print it to console
@bot.listen(event="event_message")
async def extra_message(message):
    print(message.content)

# this function is a scheduler, which will ask you to eat something when 02:07 AM
async def timer_function():
    while True:
        time.sleep(60)
        now = datetime.datetime.now().strftime("%H:%M")
        print(now)
        if now == "02:07":
            chan = bot.get_channel(os.environ['CHANNEL'])
            await chan.send("半夜 02:07 啦，大家吃宵夜沒")
            del chan

# to make timer_function to become a callback function for threading
def timer_function_worker():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(timer_function())
    loop.close()

if __name__ == "__main__":
    # setup scheduler thread
    thread_timer = threading.Thread(target=timer_function_worker, args=()) 
    thread_timer.start()

    # setup bot thread, it should be the final thread to be setup in main
    thread_bot = threading.Thread(target=bot.run, args=()) 
    thread_bot.start()

    # use join to run forever
    thread_bot.join()
    thrthread_timeread_bot.join()