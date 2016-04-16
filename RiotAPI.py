import requests
import json

def getSummoner(region, summonerName, APIKey):

    URL = "https://" + region + ".api.pvp.net/api/lol/" + region + "/v1.4/summoner/by-name/" + \
    	summonerName + "?api_key=" + APIKey

    print ("Requesting summoner data for " + summonerName + " on region " + region + "...")
    r = requests.get(URL)
    print ("done.")

    parsed = r.json()
    print (parsed[summonerName.lower()]["id"])
    print (parsed[summonerName.lower()]["name"])
    print (parsed[summonerName.lower()]["summonerLevel"])
    return r.json()


def getRankedData(region, ID, APIKey):

    URL = "https://" + region + ".api.pvp.net/api/lol/" + region + "/v2.5/league/by-summoner/" + \
    	ID + "/entry?api_key=" + APIKey

    print ("Requesting ranked data for summoner ID " + ID + " on region " + region + "...")
    r = requests.get(URL)
    print ("done.")

    parsed = r.json()

    print (parsed[ID][0]["name"])
    print (parsed[ID][0]["tier"])
    print (parsed[ID][0]["entries"][0]["division"])
    print (parsed[ID][0]["entries"][0]["leaguePoints"])

    return parsed


def getRecentGames(region, ID, APIKey):

    URL = "https://" + region + ".api.pvp.net/api/lol/" + region + "/v1.3/game/by-summoner/" + \
        ID + "/entry?api_key=" + APIKey

    print ("Requesting recent game data for summoner ID " + ID + " on region " + region + "...")
    r = requests.get(URL)
    print ("done.")

    return r.json()


def getItemData(region, APIKey):

    URL = "https://global.api.pvp.net/api/lol/static-data/" + region + "/v1.2/item?api_key=" + APIKey

    print ("Requesting item data from region" + region + "...")
    r = requests.get(URL)
    print ("done.")

    return r.json()


#getSummoner("na", "Cryrore", "689e58e2-23b2-415c-aca7-183ea7fe3535") # This is my API key btw.
#getRankedData("na", "31300153", "689e58e2-23b2-415c-aca7-183ea7fe3535") # The number is Cryrore's summ ID