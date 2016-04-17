import discord
from discord.ext import commands
import asyncio
import RiotAPI
import requests
import json

class league():
	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context=True, description="Prints summoner name")
	async def summoner(self, ctx,*, summonerName : str=None):
		#TODO: Make this work for summoner names that have spaces and make region an argument
		if summonerName == None:
			summonerName = str(ctx.message.author.name)

		parsedSumm = RiotAPI.getSummoner("na", summonerName, "689e58e2-23b2-415c-aca7-183ea7fe3535")
		if type(parsedSumm) == int: # If something went wrong...
			await self.bot.say("Failed with error code " + str(parsedSumm) + ". Maybe try turning it off and on again?")
			return
		parsedRank = RiotAPI.getRankedData("na", str(parsedSumm[summonerName.lower()]["id"]), "689e58e2-23b2-415c-aca7-183ea7fe3535")

		pulledName = parsedSumm[summonerName.lower()]["name"]
		pulledID = str(parsedSumm[summonerName.lower()]["id"])
		pulledLevel = str(parsedSumm[summonerName.lower()]["summonerLevel"])
		if type(parsedRank) == int:
			pulledRankName = "Morello's Subarus"
			pulledRankTier = "Unranked"
			pulledDivision = "0"
			pulledLeaguePoints = "0"
		else:
			pulledRankName = parsedRank[str(parsedSumm[summonerName.lower()]["id"])][0]["name"]
			pulledRankTier = parsedRank[str(parsedSumm[summonerName.lower()]["id"])][0]["tier"].lower().capitalize()
			pulledDivision = parsedRank[str(parsedSumm[summonerName.lower()]["id"])][0]["entries"][0]["division"]
			pulledLeaguePoints = str(parsedRank[str(parsedSumm[summonerName.lower()]["id"])][0]["entries"][0]["leaguePoints"])

		response = "\n__" + pulledName + "__" + "\nLevel " + pulledLevel + " summoner on region NA\n" + \
					pulledRankTier + " " + pulledDivision + " (" + pulledLeaguePoints + " LP) in " + \
					pulledRankName
		print(response)

		await self.bot.say(response)


	@commands.command(descrption="Lists the free champs of the week")
	async def freechamps(self):
		pulledChamps = RiotAPI.getFreeChamps("na", "689e58e2-23b2-415c-aca7-183ea7fe3535")

		champList = []

		for x in range(10):
			champID = pulledChamps["champions"][x]["id"]
			champName = RiotAPI.getChampByID("na", champID, "689e58e2-23b2-415c-aca7-183ea7fe3535")
			champList.append(champName)

		response = "The free champions of the week are " + champList[0]
		for x in range(8):
			response += ", " + champList[x+1]
		response += " and " + champList[9] + "."

		await self.bot.say(response)





def setup(bot): # I have no idea what this does but it makes the bot work
	bot.add_cog(league(bot))