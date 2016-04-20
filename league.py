import discord
from discord.ext import commands
import asyncio
import rawpi
import requests
import json

class league():
	def __init__(self, bot):
		self.bot = bot
		with open('data.json') as data_file:
			self.summonerIds = json.load(data_file)
		print (self.summonerIds)

	@commands.command(pass_context=True, description="Prints summoner name")
	async def summoner(self, ctx,*, summonerName : str=None):
		#TODO: Make this work for pre-30 summoners
		if summonerName == None:
			if ctx.message.author.name not in self.summonerIds:
				await self.bot.say('''I don't know your League username yet.  Please register it with !register "yourUsernameHere"''')
				return
			else:
				summonerName = self.summonerIds[ctx.message.author.name]

		summonerName = summonerName.replace(" ", "").lower()

		parsedSumm = rawpi.get_summoner_by_name("na", summonerName).json()
		try: 
			pulledError = parsedSumm["status"]["status_code"]
			if pulledError == 404:
				await self.bot.say("Couldn't find that summoner. Maybe that was the wrong spelling?")
			elif pulledError == 429:
				await self.bot.say("Request limit exceeded. " + \
									"I can only take 10 requests per 10 seconds... slow down!")
			else:
				await self.bot.say("Failed with error code " + str(pulledError) + \
									". Maybe try turning it off and on again?")
			return
		except KeyError:
			pulledName = parsedSumm[summonerName]["name"]
			pulledID = str(parsedSumm[summonerName]["id"])
			pulledLevel = str(parsedSumm[summonerName]["summonerLevel"])

		parsedRank = rawpi.get_league_entry("na", pulledID).json()
		try:
			parsedRank["status"]["status_code"]
			pulledRankName = "Morello's Subarus"
			pulledRankTier = "Unranked"
			pulledDivision = "0"
			pulledLeaguePoints = "0"	
		except KeyError:
			pulledRankName = parsedRank[pulledID][0]["name"]
			pulledRankTier = parsedRank[pulledID][0]["tier"].lower().capitalize()
			pulledDivision = parsedRank[pulledID][0]["entries"][0]["division"]
			pulledLeaguePoints = str(parsedRank[pulledID][0]["entries"][0]["leaguePoints"])

		response = "\n__" + pulledName + "__ (ID #" + pulledID + ")\nLevel " + pulledLevel + \
					" summoner on region NA\n" + pulledRankTier + " " + pulledDivision + " (" + \
					pulledLeaguePoints + " LP) in " + pulledRankName
		print(response)

		await self.bot.say(response)

	@commands.command(pass_context=True, description="Registers a summoner name to a discord User")
	async def register(self,ctx,*, summonerName : str=None):
		print (ctx.message)
		self.summonerIds[ctx.message.author.name]=summonerName
		print (self.summonerIds)
		with open('data.json', 'w') as outfile:
			json.dump(self.summonerIds, outfile, sort_keys = True, indent = 4, ensure_ascii=False)
		await self.bot.say("Your username has been registered!")
		return
		
	@commands.command(description="Lists the free champs of the week")
	async def freechamps(self):
		pulledChamps = rawpi.get_champions("na", True).json()
		try:
			pulledError = pulledChamps["status"]["status_code"]
			if pulledError == 429:
				await self.bot.say("Request limit exceeded. " + \
					"I can only take 10 requests per 10 seconds... slow down!")
			else:
				await self.bot.say("Failed with error code " + str(pulledError) + \
									". Maybe try turning it off and on again?")
			return
		except KeyError:
			champList = []

		for x in range(10):
			champID = pulledChamps["champions"][x]["id"]
			champName = rawpi.get_champion_list_by_id("na", champID).json()["name"]
			print(champName)
			champList.append(champName)

		response = "The free champions of the week are " + champList[0]
		for x in range(8):
			response += ", " + champList[x+1]
		response += " and " + champList[9] + "."

		await self.bot.say(response)


	@commands.command(description="Notifies you when a summoner finishes their game")
	async def track(self, *, summonerName : str=None):
		#TODO: Make this print an error in chat if the bot can't find the summoner
		if summonerName == None:
			await self.bot.say("You probably don't mean to track yourself. Give me a summoner name.")
			return

		summonerName = summonerName.replace(" ", "").lower()

		parsedSumm = rawpi.get_summoner_by_name("na", summonerName).json()

		pulledName = parsedSumm[summonerName]["name"]
		pulledID = str(parsedSumm[summonerName]["id"])
		
		pulledGame = rawpi.get_current_game("na", "NA1", pulledID).json()

		pulledGameLength = pulledGame["gameLength"]

		minutes = int(pulledGameLength / 60.0)
		seconds = (pulledGameLength) - (minutes * 60)

		response = "Ok! I'll let you know when __" + pulledName + "__ is out of game (WHEN IMPLEMENTED). Currently ingame for "

		if (minutes > 0):
			response += str(minutes) + " minutes, "
		
		response += str(seconds) + " seconds, and counting..."

		await self.bot.say(response)





def setup(bot): # I have no idea what this does but it makes the bot work
	bot.add_cog(league(bot))