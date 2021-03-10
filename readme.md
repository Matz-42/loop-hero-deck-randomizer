A small python deck generator and randomizer made for Loop Hero by Matz.
Was made with python 3.8 but should probably work with any Python 3 version.

Just launch the script, you can reproduce the deck generated in-game.

Also includes a small .json config file if you want to change a bit the type of decks you get:
	
	"randomCharacter": (true/false)
	If the generator should also give you a random character.

	"minCards": (7-15)
	The minimum amount of cards that the deck can be made of.
	
	"maxCards": (7-15)
	The maximum amount of cards that the deck can be made of.
	
	"goldCardChance": (0-100)
	The chance in % that you will be given a gold card, can be useful if you want the occasional gold card-less run.
	
	"whiteList": [List]
	A list of cards that will always be included into the decks, can be useful if you have cards you always want in.
	eg: "whiteList": ["Oblivion", "Village"]
	
	"blackList": [List]
	A list of cards that will never be included into the decks, can be useful if you have cards you hate or haven't unlocked.
	eg: "blackList": ["Beacon", "Maze Of Memories"]
	
	(The whiteList and blackList are case sensitive, here is the complete list of cards and their case sensitive spelling:
	"Cemetery", "Village", "Grove", "Wheat Fields", "Swamp", "Ruins", "Spider Cocoon", "Vampire Mansion", "Battle Fields",
	"Blood Grove", "Bookery", "Road Lantern", "Smiths Forge", "Chrono Crystals", "Outpost", "Rock", "Forest", "River",
	"Desert", "Meadow", "Suburbs", "Oblivion", "Beacon", "Storm Temple", "Temporal Beacon", "Treasury", "Ancestral Crypt",
	"Zero Milestone", "Maze Of Memories", "Arsenal")