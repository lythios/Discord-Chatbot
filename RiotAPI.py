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

    return r.json()


#getSummoner("na", "Cryrore", "689e58e2-23b2-415c-aca7-183ea7fe3535") # This is my API key btw.
#getRankedData("na", "31300153", "689e58e2-23b2-415c-aca7-183ea7fe3535") # The number is Cryrore's summ ID