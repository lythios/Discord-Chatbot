import discord
from discord.ext import commands
import asyncio
import rawpi
import random
import os
from league import league

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


description = "Warren's bot"
bot = commands.Bot(command_prefix="!", description=description)


@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("------")
    

    avatar_dict = { 0: "avatar_yellow.png",
    				1: "avatar_blue.png",
    				2: "avatar_red.png"}
    key = random.randint(0,2) # Used to choose a random league trinket as profile picture

    with open("images/" + avatar_dict[key], "rb") as fp:
    	avatar_pic = fp.read()
    await bot.edit_profile(avatar=avatar_pic)

    myGame = discord.Game(name="with fire")
    bot.loop.create_task(bot.change_status(game=myGame, idle=False))

    bot.load_extension("fluff")
    bot.load_extension("league")

    with open(os.path.join(__location__, 'config'), 'r') as f:
        try:
            config = json.load(f)
        except ValueError:
            config = {'token': ""}

    TOKEN = config["token"]


@bot.event
async def on_message(message):

	if message.content.startswith("hello doran"):##You should move this to the fluff extension warren
		await bot.send_message(message.channel, "Greetings, summoner. :)")

	await bot.process_commands(message)


async def backgroundCheckUsers():
    await bot.wait_until_ready()
    counter = 0
    LoL=league(bot)
    while not bot.is_closed:
        counter += 1
        LoL.checkUsers()
        await asyncio.sleep(5)

loop = asyncio.get_event_loop()


try:
    loop.create_task(backgroundCheckUsers())
    loop.run_until_complete(bot.run(TOKEN)) # This is the bot's token
    loop.run_until_complete(bot.connect())
except:
    loop.run_until_complete(bot.close())
finally:
    loop.close()