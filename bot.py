import discord
import asyncio
import RiotAPI
import random
import os

client = discord.Client()


@client.event
async def on_ready():
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)
    print("------")

    avatar_dict = { 0: "avatar_yellow.png",
    				1: "avatar_blue.png",
    				2: "avatar_red.png"}
    key = random.randint(0,2) # Used to choose a random league trinket as profile picture

    with open("images/" + avatar_dict[key], "rb") as fp:
    	avatar_pic = fp.read()
    await client.edit_profile(avatar=avatar_pic)

    myGame = discord.Game(name="with fire")
    client.loop.create_task(client.change_status(game=myGame, idle=False))


@client.event
async def on_message(message):
    if message.content.startswith("!ping"):
    	await client.send_message(message.channel, "pong!")

    elif message.content.startswith("!count"):
        count = 0;
        tmp = await client.send_message(message.channel, count)
        for x in range (0, 10):
            await asyncio.sleep(1)
            count += 1
            await client.edit_message(tmp, count)

    elif message.content.startswith("!lolsummoner"):
    	# TODO: Make this function take region and summonerName as arguments
    	parsed = (RiotAPI.getSummoner("na", "Cryrore", "689e58e2-23b2-415c-aca7-183ea7fe3535"))

    	response = (parsed["cryrore"]["name"] + " is a level " + str(parsed["cryrore"]["summonerLevel"]) + \
    		" summoner with ID number " + str(parsed["cryrore"]["id"]) + ".")

    	await client.send_message(message.channel, response)



client.run("MTcwNjE3NTk5NTI3MjIzMzA2.CfLThQ.uM6EunSPIt3byB7fs36whc9cHIs") # This is the bot's token