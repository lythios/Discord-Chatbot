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
		parsedSumm = RiotAPI.getSummoner("na", str(message.author.name), "689e58e2-23b2-415c-aca7-183ea7fe3535")
		parsedRank = RiotAPI.getRankedData("na", str(parsedSumm[message.author.name.lower()]["id"]), "689e58e2-23b2-415c-aca7-183ea7fe3535")

		banter_dict = { 0: " *still* trying to climb out of ",
						1: " perpetually stuck in ",
						2: " lounging around in ",
						3: " climbing through ",
						4: " enjoying the weather in ",
						5: " vaynespotting across ",
						6: " walking the lonely road up "}
		key = random.randint(0,6)

		response = "**" + str(parsedSumm[message.author.name.lower()]["name"]) + "** (ID#" + \
			str(parsedSumm[message.author.name.lower()]["id"]) + ") is an NA summoner" + \
			banter_dict[key] + str(parsedRank[str(parsedSumm[message.author.name.lower()]["id"])][0]["tier"]) + " " + \
			str(parsedRank[str(parsedSumm[message.author.name.lower()]["id"])][0]["entries"][0]["division"]) + \
			" (" + str(parsedRank[str(parsedSumm[message.author.name.lower()]["id"])][0]["entries"][0]["leaguePoints"]) + \
			" LP)."

		await client.send_message(message.channel, response)


	elif message.content.startswith("!hello"):
		if message.author.name == "Cryrore":
			await client.send_message(message.channel, "Hello, " + str(message.author.name) + \
				"! I could have sworn I was just talking to you...")

		else:
			await client.send_message(message.channel, "Hiya, " + str(message.author.name) + "!")


	elif message.content.startswith("!summon"):
		await client.send_message(message.channel, "http://i.imgur.com/z5Vayfy.jpg")



client.run("MTcwNjE3NTk5NTI3MjIzMzA2.CfLThQ.uM6EunSPIt3byB7fs36whc9cHIs") # This is the bot's token