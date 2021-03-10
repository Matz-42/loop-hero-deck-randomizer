##############################################
#                                            #
#   Loop Hero deck randomizer by Matz v1.0   #
#                                            #
##############################################

import json
import random

#Lists of things
characters = ["Warrior", "Rogue", "Necromancer"]
roadCards = ["Cemetery", "Village", "Grove", "Wheat Fields", "Swamp", "Ruins"]
roadSideCards = ["Spider Cocoon", "Vampire Mansion", "Battle Fields", "Blood Grove", "Bookery", "Road Lantern", "Smiths Forge", "Chrono Crystals", "Outpost"]
terrainCards = ["Rock", "Forest", "River", "Desert", "Meadow", "Suburbs"]
specialCards = ["Oblivion", "Beacon", "Storm Temple", "Temporal Beacon", "Treasury"]
goldCards = ["Ancestral Crypt", "Zero Milestone", "Maze Of Memories", "Arsenal"]

try:
	#Load config
	with open("config.json") as file:
		config = json.load(file)

	#Basic config weird options test
	if config["minCards"] < 7:
		raise Exception("Wrong config: You can't have less than 7 cards in a deck")
	if config["maxCards"] > 15:
		raise Exception("Wrong config: You can't have more than 15 cards in a deck")
	if config["minCards"] > config["maxCards"]:
		raise Exception("Wrong config: The minimum amount of cards can't be above the maximum amount")
	if config["goldCardChance"] < 0:
		raise Exception("Wrong config: You can't have less than 0% chance of having a gold card")
	if config["goldCardChance"] > 100:
		raise Exception("Wrong config: You can't have more than 100% chance of having a gold card")
	if len(config["whiteList"]) > config["maxCards"]:
		raise Exception("Wrong config: You have more whitelisted cards than max cards")
		
	#Extra removal for cards requiring other cards that might be blacklisted
	if "Village" in config["blackList"]:
		if "Wheat Fields" in config["whiteList"]:
			raise Exception("Wrong config: Wheat Fields is whitelisted but Village is blacklisted")
		roadCards.remove("Wheat Fields")
	
	if "Grove" in config["blackList"] and "Forest" in config["blackList"]:
		if "Blood Grove" in config["whiteList"]:
			raise Exception("Wrong config: Blood Grove is whitelisted but both Grove and Forest are blacklisted")
		roadSideCards.remove("Blood Grove")
		
	#Removing the blacklisted cards
	for c in config["blackList"]:
		if c in config["whiteList"]:
			raise Exception("Wrong config: A card can't be both whitelisted and blacklisted")
		
		if c in roadCards: roadCards.remove(c)
		elif c in roadSideCards: roadSideCards.remove(c)
		elif c in terrainCards: terrainCards.remove(c)
		elif c in specialCards: specialCards.remove(c)
		elif c in goldCards: goldCards.remove(c)
		
	#Variables to keep track of added cards
	roadAdded = []
	roadSideAdded = []
	terrainAdded = []
	specialAdded = []
	
	#Adding whitelisted normal cards
	for c in config["whiteList"]:
		if c in roadCards:
			roadCards.remove(c)
			roadAdded.append(c)
			
		elif c in roadSideCards:
			roadSideCards.remove(c)
			roadSideAdded.append(c)

		elif c in terrainCards:
			terrainCards.remove(c)
			terrainAdded.append(c)

		elif c in specialCards:
			specialCards.remove(c)
			specialAdded.append(c)
	
	#Adding necessary cards for possible whitelisted cards
	if "Wheat Fields" in roadAdded and "Village" not in roadAdded:
		if len(roadAdded + roadSideAdded + terrainAdded + specialAdded) >= config["maxCards"]:
			raise Exception("Wrong config: Wheat Fields require Village to be added, but all whitelisted cards take all possible slots already")
		roadCards.remove("Village")
		roadAdded.append("Village")
		
	if "Blood Grove" in roadSideAdded and "Grove" not in roadAdded and "Forest" not in terrainAdded:
		if len(roadAdded + roadSideAdded + terrainAdded + specialAdded) >= config["maxCards"]:
			raise Exception("Wrong config: Blood Grove require Grove or Forest to be added, but all whitelisted cards take all possible slots already")
		if random.randint(0,1) == 1:
			roadCards.remove("Grove")
			roadAdded.append("Grove")
		else:
			terrainCards.remove("Forest")
			terrainAdded.append("Forest")
			
	#Shuffling the remaining lists
	random.shuffle(roadCards)
	random.shuffle(roadSideCards)
	random.shuffle(terrainCards)
	random.shuffle(specialCards)
	
	#Adding the minimum amount of cards necessary
	while len(roadAdded) < 2:
		if len(roadCards) == 0:
			raise Exception("Wrong config: Not enough road cards left")
		roadAdded.append(roadCards.pop())
	while len(roadSideAdded) < 2:
		if len(roadSideCards) == 0:
			raise Exception("Wrong config: Not enough road-side cards left")
		roadSideAdded.append(roadSideCards.pop())
	while len(terrainAdded) < 2:
		if len(terrainCards) == 0:
			raise Exception("Wrong config: Not enough terrain cards left")
		terrainAdded.append(terrainCards.pop())
	while len(specialAdded) < 1:
		if len(specialCards) == 0:
			raise Exception("Wrong config: Not enough special cards left")
		specialAdded.append(specialCards.pop())
		
	#Check if the config isn't impossible
	if len(roadAdded + roadSideAdded + terrainAdded + specialAdded) > config["maxCards"]:
		raise Exception("Wrong config: The whitelisted cards require a minimum amount of cards above the set maximum")
	
	#Get the random number of cards to aim for
	targetAmount = random.randint(config["minCards"], config["maxCards"])
	
	#Shuffle the remaining cards together
	remainingCards = roadCards + roadSideCards + terrainCards + specialCards
	random.shuffle(remainingCards)
	
	#Add random cards until we get to the target amount
	while len(roadAdded + roadSideAdded + terrainAdded + specialAdded) < targetAmount:
		c = remainingCards.pop()
		if c in roadCards:
			roadCards.remove(c)
			roadAdded.append(c)
			
		elif c in roadSideCards:
			roadSideCards.remove(c)
			roadSideAdded.append(c)

		elif c in terrainCards:
			terrainCards.remove(c)
			terrainAdded.append(c)

		elif c in specialCards:
			specialCards.remove(c)
			specialAdded.append(c)
			
	#Adding necessary cards for possible added cards or removing them if impossible
	if "Wheat Fields" in roadAdded and "Village" not in roadAdded:
		if len(roadAdded + roadSideAdded + terrainAdded + specialAdded) >= config["maxCards"]:
			roadAdded.remove("Wheat Fields")
			if len(roadCards) == 0:
				raise Exception("Something went wrong... Not enough road cards left")
			roadAdded.append(roadCards.pop())
		else:
			roadCards.remove("Village")
			roadAdded.append("Village")
		
	if "Blood Grove" in roadSideAdded and "Grove" not in roadAdded and "Forest" not in terrainAdded:
		if len(roadAdded + roadSideAdded + terrainAdded + specialAdded) >= config["maxCards"]:
			roadSideAdded.remove("Blood Grove")
			if len(roadSideCards) == 0:
				raise Exception("Something went wrong.. Not enough road-side cards left")
			roadSideAdded.append(roadSideCards.pop())
		else:
			if random.randint(0,1) == 1:
				roadCards.remove("Grove")
				roadAdded.append("Grove")
			else:
				terrainCards.remove("Forest")
				terrainAdded.append("Forest")
	
	#Security checks
	if len(roadAdded + roadSideAdded + terrainAdded + specialAdded) > config["maxCards"]:
		raise Exception("Something went wrong... There are more cards in the deck than there should be")
		
	if len(roadAdded + roadSideAdded + terrainAdded + specialAdded) < config["minCards"]:
		raise Exception("Something went wrong... There are less cards in the deck than there should be")
				
	#Selecting a random gold card
	goldCard = None
	if config["goldCardChance"] > 0 and len(goldCards) == 0:
		raise Exception("Wrong config: No gold cards to select from")
		
	if random.randint(0,100) < config["goldCardChance"]:
		for c in goldCards:
			if c in config["whiteList"]:
				goldCard = c
				
		if goldCard == None:
			goldCard = random.choice(goldCards)
		
	#Selecting a random Hero
	hero = None
	if config["randomCharacter"]:
		hero = random.choice(characters)
	
	#Printing the results
	print("Loop Hero deck randomizer by Matz:\n")
	
	if hero != None:
		print("Play as: " + hero + "\n")
	
	print("Your deck is:")
	print("Road Cards:      ", end = "")
	print(roadAdded)
	print("Road-side Cards: ", end = "")
	print(roadSideAdded)
	print("Terrain Cards:   ", end = "")
	print(terrainAdded)
	print("Special Cards:   ", end = "")
	print(specialAdded)
	
	if goldCard == None:
		print("And no gold card")
	else:
		print("Gold Card:       ['" + goldCard + "']")

	
except Exception as e:
	print(e)
	
#Waiting for exit
wait = input("\nPress enter to exit...")