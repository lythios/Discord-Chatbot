import discord
from discord.ext import commands
import asyncio
import rawpi
import champggapi
import requests
import json
import sys

class league():
	def __init__(self, bot):
		self.bot = bot
		with open('data.json') as data_file:
			self.registeredSummoner = json.load(data_file)
		print (self.registeredSummoner)
		self.userLists={}
		
	@commands.command(pass_context=True, description="Prints summoner name")
	async def summoner(self, ctx, *, summonerName : str=None):
		#TODO: Make this work for pre-30 summoners
		if summonerName == None:
			if ctx.message.author.name not in self.registeredSummoner:
				await self.bot.say('''I don't know your League username yet.  Please register it with !register "yourUsernameHere"''')
				return
			else:
				summonerName = self.registeredSummoner[ctx.message.author.name][0]

		summonerName = summonerName.replace(" ", "").lower()

		parsedSumm = rawpi.get_summoner_by_name("na", summonerName).json()
		try: 
			pulledError = parsedSumm["status"]["status_code"]
			if pulledError == 404:
				await self.bot.say("Couldn't find that summoner. Wrong spelling maybe?")
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

		response = "\n__" + pulledName + "__ (ID #" + pulledID + ")\nLevel " + pulledLevel + \
					" summoner on region NA"

		parsedRank = rawpi.get_league_entry("na", pulledID).json()
		try:
			pulledError = parsedRank["status"]["status_code"]
			
			if pulledError == 404 and int(pulledLevel) == 30:
				response += "\nUnranked (No league information)"
			elif pulledError == 429:
				response += "\nUnknown (Request limit exceeded, try again)"
		except KeyError:
			pulledRankName = parsedRank[pulledID][0]["name"]
			pulledRankTier = parsedRank[pulledID][0]["tier"].lower().capitalize()
			pulledDivision = parsedRank[pulledID][0]["entries"][0]["division"]
			pulledLeaguePoints = str(parsedRank[pulledID][0]["entries"][0]["leaguePoints"])

			response += "\n" + pulledRankTier + " " + pulledDivision + " (" + \
					pulledLeaguePoints + " LP) in " + pulledRankName

		print(response)

		await self.bot.say(response)


	@commands.command(pass_context=True, description="Registers a summoner name to a discord User")
	async def register(self,ctx,*, summonerName : str=None):
		print (ctx.message)

		parsedSumm = rawpi.get_summoner_by_name("na", summonerName.lower()).json()
		try: 
			pulledError = parsedSumm["status"]["status_code"]
			if pulledError == 404:
				print("Couldn't find that summoner. Wrong spelling maybe?")
			elif pulledError == 429:
				print("Request limit exceeded. " + \
									"I can only take 10 requests per 10 seconds... slow down!")
			else:
				print("Failed with error code " + str(pulledError) + \
									". Maybe try turning it off and on again?")
			return
		except KeyError:
			pulledName = parsedSumm[summonerName.lower()]["name"]
			pulledID = str(parsedSumm[summonerName.lower()]["id"])

		self.registeredSummoner[ctx.message.author.name] = [pulledName, pulledID]
		print (self.registeredSummoner)
		with open('data.json', 'w') as outfile:
			json.dump(self.registeredSummoner, outfile, sort_keys = True, indent = 4, ensure_ascii=False)
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

	@commands.command(pass_context=True, description="Notifies you when a summoner finishes their game")
	async def track(self, ctx, *, summonerName : str=None):
		print(summonerName)
		if summonerName in self.registeredSummoner:
			summonerName = self.registeredSummoner[summonerName][0]
			print("Successfully matched discord name to League Username")
		if summonerName == None:
			await self.bot.say("You probably don't mean to track yourself. Give me a summoner name.")
			return

		summonerName = summonerName.replace(" ", "").lower()

		parsedSumm = rawpi.get_summoner_by_name("na", summonerName).json()
		try: 
			pulledError = parsedSumm["status"]["status_code"]
			if pulledError == 404:
				await self.bot.say("Couldn't find that summoner. Wrong spelling maybe?")
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
		
		pulledGame = rawpi.get_current_game("na", "NA1", pulledID).json()
		try: 
			pulledError = pulledGame["status"]["status_code"]
			if pulledError == 404:
				await self.bot.say("__" + pulledName + "__ is not currently in game. " + \
									"You should track them down in person. :slight_smile:")
			elif pulledError == 429:
				await self.bot.say("Request limit exceeded. " + \
									"I can only take 10 requests per 10 seconds... slow down!")
			else:
				await self.bot.say("Failed with error code " + str(pulledError) + \
									". Maybe try turning it off and on again?")
			return
		except KeyError:
			pulledGameLength = pulledGame["gameLength"]

		minutes = int(pulledGameLength / 60.0)
		seconds = (pulledGameLength) - (minutes * 60)

		response = "Ok! I'll let you know when __" + pulledName + "__ is out of game. "
		if (minutes > 0):
			response += "That summoner has been in game for " + str(minutes + 5) + " minutes and " + \
						str(seconds) + " seconds so far."
		else:
			response += "They've been in game for about 5 minutes so far (can't get an exact number until later)."

		await self.bot.say(response)

		while True:
			await asyncio.sleep(5)
			pulledGame = rawpi.get_current_game("na", "NA1", pulledID).json()
			try:
				pulledError = pulledGame["status"]["status_code"]
				if pulledError == 404:
					await self.bot.say("Hey, " + str(ctx.message.author.mention) + ", __" + pulledName + "__ just finished playing.")
				elif pulledError == 429:
					await self.bot.say("Request limit exceeded (just tried to see if __" + pulledName + \
										"__ was in game). Slow down!")
				else:
					await self.bot.say("Failed checking whether __" + pulledName + \
										"__ was in game. Error code " + str(pulledError) + \
										". Maybe try turning it off and on again?")
				return
			except KeyError:
				print (pulledName + " is still in game.")

		

	
	@commands.command(description="Lists the top five counters to a champion")
	async def counter(self, champName : str=None, role : str=None, size : int=None):
		if champName == None:
			await self.bot.say("Counter nothing by playing nothing. Trust me.")
			return

		parsedMatchups = champggapi.get_matchups(champName).json()

		try:
			pulledError = parsedMatchups["error"]
			await self.bot.say("Error: " + pulledError)
			return
		except:
			roleNum = len(parsedMatchups)

		if role != None:
			for x in range(roleNum):
				if role.lower() == parsedMatchups[x]["role"].lower():
					roleIndex = x
					break
				else:
					roleIndex = -1
		else:
			roleIndex = 0

		if roleIndex == -1:
			await self.bot.say("I haven't seen " + champName.lower().capitalize() + " " + role + " before...")
			return

		searchingRole = parsedMatchups[roleIndex]["role"]
		unsortedMatchups = parsedMatchups[roleIndex]["matchups"]

		# Reverse so it's descending order
		sortedMatchups = sorted(unsortedMatchups, key=lambda k: k["winRate"], reverse=True)
		print(sortedMatchups)

		if size == None:
			size = 5
		elif size > len(sortedMatchups):
			size = len(sortedMatchups)

		response = "\n" + champName.lower().capitalize() + "'s top " + str(size) + " (" + searchingRole + ") counters, sorted by win rate:\n"
		for x in range(size):
			response += sortedMatchups[x]["key"] + ": " + str(sortedMatchups[x]["winRate"]) + "%\n"

		await self.bot.say(response)
		
	def checkUsers(self):
		for member in self.bot.get_all_members():
			if (member.status == member.status.online and member.name in self.registeredSummoner and member.name not in self.userLists):
				self.userLists[member.name]=["pentas","mastery"]
				print (member.name + " should be added")
				print (member.game)
			print(member.name.encode(sys.stdout.encoding, errors='replace'), member.status)
		print ("User list:" + repr(self.userLists))


class summoner():
	def __init__(self, name : str):
		self.name = name

		parsedSumm = rawpi.get_summoner_by_name("na", name.lower()).json()
		try: 
			pulledError = parsedSumm["status"]["status_code"]
			if pulledError == 404:
				print("Couldn't find that summoner. Wrong spelling maybe?")
			elif pulledError == 429:
				print("Request limit exceeded. " + \
									"I can only take 10 requests per 10 seconds... slow down!")
			else:
				print("Failed with error code " + str(pulledError) + \
									". Maybe try turning it off and on again?")
			return
		except KeyError:
			pulledName = parsedSumm[name.lower()]["name"]
			pulledID = str(parsedSumm[name.lower()]["id"])

		self.id = pulledID





def setup(bot): # I have no idea what this does but it makes the bot work
	bot.add_cog(league(bot))