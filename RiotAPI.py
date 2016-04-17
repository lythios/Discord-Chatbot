import requests
import json

def getSummoner(region, summonerName, APIKey):

    URL = "https://" + region + ".api.pvp.net/api/lol/" + region + "/v1.4/summoner/by-name/" + \
    	summonerName + "?api_key=" + APIKey

    print ("Requesting summoner data for " + summonerName + " on region " + region + "...")
    r = requests.get(URL)
    if r.status_code == 200:
        print("success!")
    else:
        print("failed!")
        return r.status_code

    parsed = r.json()
    print (parsed[summonerName.lower()]["id"])
    print (parsed[summonerName.lower()]["name"])
    print (parsed[summonerName.lower()]["summonerLevel"])
    
    return parsed


def getRankedData(region, ID, APIKey):

    URL = "https://" + region + ".api.pvp.net/api/lol/" + region + "/v2.5/league/by-summoner/" + \
    	ID + "/entry?api_key=" + APIKey

    print ("Requesting ranked data for summoner ID " + ID + " on region " + region + "...")
    r = requests.get(URL)
    if r.status_code == 200:
        print("success!")
    else:
        print("failed!")
        return r.status_code

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
    if r.status_code == 200:
        print("success!")
    else:
        print("failed!")
        return r.status_code

    return r.json()


def getItemData(region, APIKey):

    URL = "https://global.api.pvp.net/api/lol/static-data/" + region + "/v1.2/item?api_key=" + APIKey

    print ("Requesting item data from region " + region + "...")
    r = requests.get(URL)
    if r.status_code == 200:
        print("success!")
    else:
        print("failed!")
        return r.status_code

    return r.json()


def getFreeChamps(region, APIKey):

    URL = "https://" + region + ".api.pvp.net/api/lol/" + region + "/v1.2/champion?freeToPlay=true&api_key=" + APIKey

    print ("Requesting free to play data from region " + region + "...")
    r = requests.get(URL)
    if r.status_code == 200:
        print("success!")
    else:
        print("failed!")
        return r.status_code

    return r.json()


def getChampByID(region, champID, APIKey):
    URL = "https://global.api.pvp.net/api/lol/static-data/" + region + "/v1.2/champion/" + str(champID) + \
        "?champData=info,recommended&api_key=" + APIKey

    print ("Requesting champ by ID from region " + region + "...")
    r = requests.get(URL)
    if r.status_code == 200:
        print("success!")
    else:
        print("failed!")
        return r.status_code

    r = str(r.json()["name"])

    return r