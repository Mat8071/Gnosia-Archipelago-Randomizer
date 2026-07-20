from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification

if TYPE_CHECKING:
    from .world import GnosiaWorld

ITEM_NAME_TO_ID = {
    #Skills
    "Step Forward": 1,
    "Definite Human/Enemy": 2,
    "Say You're Human": 5,
    "Vote": 6,
    "Don't Vote": 7,
    "Small Talk": 8,
    "Freeze All": 9,
    "Let's Collaborate": 10,
    "Seek Agreement": 11,
    "Block Argument": 12,
    "Exaggerate": 13,
    "Obfuscate": 14,
    "Retaliate": 15,
    "Regret": 16,
    "Seek Help": 17,
    "Don't Be Fooled": 18,
    "Grovel": 19,
    #Notes & Characters
    #Gina
    "Gina": 100,
    "Gina Note 1": 101,
    "Gina Note 2": 102,
    "Gina Note 3": 103,
    "Gina Note 4": 104,
    "Gina Note 5": 105,
    "Gina Note 6": 106,
    #SQ
    "SQ": 200,
    "SQ Note 1": 201,
    "SQ Note 2": 202,
    "SQ Note 3": 203,
    "SQ Note 4": 204,
    "SQ Note 5": 205,
    #Raqio
    "Raqio": 300,
    "Raqio Note 1": 301,
    "Raqio Note 2": 302,
    "Raqio Note 3": 303,
    "Raqio Note 4": 304,
    "Raqio Note 5": 305,
    "Raqio Note 6": 306,
    #Stella
    "Stella": 400,
    "Stella Note 1": 401,
    "Stella Note 2": 402,
    "Stella Note 3": 403,
    "Stella Note 4": 404,
    "Stella Note 5": 405,
    #Shigemichi
    "Shigemichi": 500,
    "Shigemichi Note 1": 501,
    "Shigemichi Note 2": 502,
    "Shigemichi Note 3": 503,
    "Shigemichi Note 4": 504,
    "Shigemichi Note 5": 505,
    "Shigemichi Note 6": 506,
    "Shigemichi Note 7": 507,
    #Chipie
    "Chipie": 600,
    "Chipie Note 1": 601,
    "Chipie Note 2": 602,
    "Chipie Note 3": 603,
    "Chipie Note 4": 604,
    "Chipie Note 5": 605,
    "Chipie Note 6": 606,
    #Remnan
    "Remnan": 700,
    "Remnan Note 1": 701,
    "Remnan Note 2": 702,
    "Remnan Note 3": 703,
    "Remnan Note 4": 704,
    "Remnan Note 5": 705,
    #Comet
    "Comet": 800,
    "Comet Note 1": 801,
    "Comet Note 2": 802,
    "Comet Note 3": 803,
    "Comet Note 4": 804,
    "Comet Note 5": 805,
    "Comet Note 6": 806,
    "Comet Note 7": 807,
    #Yuriko
    "Yuriko": 900,
    "Yuriko Note 1": 901,
    "Yuriko Note 2": 902,
    "Yuriko Note 3": 903,
    "Yuriko Note 4": 904,
    "Yuriko Note 5": 905,
    "Yuriko Note 6": 906,
    #Jonas
    "Jonas": 1000,
    "Jonas Note 1": 1001,
    "Jonas Note 2": 1002,
    "Jonas Note 3": 1003,
    "Jonas Note 4": 1004,
    "Jonas Note 5": 1005,
    "Jonas Note 6": 1006,
    "Jonas Note 7": 1007,
    #Setsu
    "Setsu": 1100,
    "Setsu Note 1": 1101,
    "Setsu Note 2": 1102,
    "Setsu Note 3": 1103,
    "Setsu Note 4": 1104,
    "Setsu Note 5": 1105,
    "Setsu Note 6": 1106,
    #Otome
    "Otome": 1200,
    "Otome Note 1": 1201,
    "Otome Note 2": 1202,
    "Otome Note 3": 1203,
    "Otome Note 4": 1204,
    "Otome Note 5": 1205,
    "Otome Note 6": 1206,
    #Sha-Ming
    "Sha-Ming": 1300,
    "Sha-Ming Note 1": 1301,
    "Sha-Ming Note 2": 1302,
    "Sha-Ming Note 3": 1303,
    "Sha-Ming Note 4": 1304,
    #Kukrushka
    "Kukrushka": 1400,
    "Kukrushka Note 1": 1401,
    "Kukrushka Note 2": 1402,
    "Kukrushka Note 3": 1403,
    "Kukrushka Note 4": 1404,
    "Kukrushka Note 5": 1405,
    "Kukrushka Note 6": 1406,
    #Roles
    "Engineer Role": 1501,
    "Doctor Role": 1502,
    "Guardian Angel Role": 1503,
    "Guard Duty Role": 1504,
    "AC Follower Role": 1506,
    "Bug Role": 1508,
    #Progressive Items
    "Progressive Crew Max": 10000,
    #Filler Items
    "End Of Loop Exp Bonus": 11000,
    #Traps
}

DEFAULT_ITEM_CLASSIFICATIONS = {
    #Skills
    "Step Forward": ItemClassification.progression | ItemClassification.useful,
    "Definite Human/Enemy": ItemClassification.useful,
    "Say You're Human": ItemClassification.progression | ItemClassification.useful,
    "Vote": ItemClassification.useful,
    "Don't Vote": ItemClassification.useful,
    "Small Talk": ItemClassification.useful,
    "Freeze All": ItemClassification.useful,
    "Let's Collaborate": ItemClassification.progression | ItemClassification.useful,
    "Seek Agreement": ItemClassification.useful,
    "Block Argument": ItemClassification.useful,
    "Exaggerate": ItemClassification.progression | ItemClassification.useful,
    "Obfuscate": ItemClassification.useful,
    "Retaliate": ItemClassification.useful,
    "Regret": ItemClassification.useful,
    "Seek Help": ItemClassification.useful,
    "Don't Be Fooled": ItemClassification.useful,
    "Grovel": ItemClassification.useful,
    #Notes & Characters
    #Gina
    "Gina": ItemClassification.progression | ItemClassification.useful,
    "Gina Note 1": ItemClassification.progression_deprioritized_skip_balancing,
    "Gina Note 2": ItemClassification.progression_deprioritized_skip_balancing,
    "Gina Note 3": ItemClassification.progression_deprioritized_skip_balancing,
    "Gina Note 4": ItemClassification.progression_deprioritized_skip_balancing,
    "Gina Note 5": ItemClassification.progression_deprioritized_skip_balancing,
    "Gina Note 6": ItemClassification.progression_deprioritized_skip_balancing,
    #SQ
    "SQ": ItemClassification.progression | ItemClassification.useful,
    "SQ Note 1": ItemClassification.progression_deprioritized_skip_balancing,
    "SQ Note 2": ItemClassification.progression_deprioritized_skip_balancing,
    "SQ Note 3": ItemClassification.progression_deprioritized_skip_balancing,
    "SQ Note 4": ItemClassification.progression_deprioritized_skip_balancing,
    "SQ Note 5": ItemClassification.progression_deprioritized_skip_balancing,
    #Raqio
    "Raqio": ItemClassification.progression | ItemClassification.useful,
    "Raqio Note 1": ItemClassification.progression_deprioritized_skip_balancing,
    "Raqio Note 2": ItemClassification.progression_deprioritized_skip_balancing,
    "Raqio Note 3": ItemClassification.progression_deprioritized_skip_balancing,
    "Raqio Note 4": ItemClassification.progression_deprioritized_skip_balancing,
    "Raqio Note 5": ItemClassification.progression_deprioritized_skip_balancing,
    "Raqio Note 6": ItemClassification.progression_deprioritized_skip_balancing,
    #Stella
    "Stella": ItemClassification.progression | ItemClassification.useful,
    "Stella Note 1": ItemClassification.progression_deprioritized_skip_balancing,
    "Stella Note 2": ItemClassification.progression_deprioritized_skip_balancing,
    "Stella Note 3": ItemClassification.progression_deprioritized_skip_balancing,
    "Stella Note 4": ItemClassification.progression_deprioritized_skip_balancing,
    "Stella Note 5": ItemClassification.progression_deprioritized_skip_balancing,
    #Shigemichi
    "Shigemichi": ItemClassification.progression | ItemClassification.useful,
    "Shigemichi Note 1": ItemClassification.progression_deprioritized_skip_balancing,
    "Shigemichi Note 2": ItemClassification.progression_deprioritized_skip_balancing,
    "Shigemichi Note 3": ItemClassification.progression_deprioritized_skip_balancing,
    "Shigemichi Note 4": ItemClassification.progression_deprioritized_skip_balancing,
    "Shigemichi Note 5": ItemClassification.progression_deprioritized_skip_balancing,
    "Shigemichi Note 6": ItemClassification.progression_deprioritized_skip_balancing,
    "Shigemichi Note 7": ItemClassification.progression_deprioritized_skip_balancing,
    #Chipie
    "Chipie": ItemClassification.progression | ItemClassification.useful,
    "Chipie Note 1": ItemClassification.progression_deprioritized_skip_balancing,
    "Chipie Note 2": ItemClassification.progression_deprioritized_skip_balancing,
    "Chipie Note 3": ItemClassification.progression_deprioritized_skip_balancing,
    "Chipie Note 4": ItemClassification.progression_deprioritized_skip_balancing,
    "Chipie Note 5": ItemClassification.progression_deprioritized_skip_balancing,
    "Chipie Note 6": ItemClassification.progression_deprioritized_skip_balancing,
    #Remnan
    "Remnan": ItemClassification.progression | ItemClassification.useful,
    "Remnan Note 1": ItemClassification.progression_deprioritized_skip_balancing,
    "Remnan Note 2": ItemClassification.progression_deprioritized_skip_balancing,
    "Remnan Note 3": ItemClassification.progression_deprioritized_skip_balancing,
    "Remnan Note 4": ItemClassification.progression_deprioritized_skip_balancing,
    "Remnan Note 5": ItemClassification.progression_deprioritized_skip_balancing,
    #Comet
    "Comet": ItemClassification.progression | ItemClassification.useful,
    "Comet Note 1": ItemClassification.progression_deprioritized_skip_balancing,
    "Comet Note 2": ItemClassification.progression_deprioritized_skip_balancing,
    "Comet Note 3": ItemClassification.progression_deprioritized_skip_balancing,
    "Comet Note 4": ItemClassification.progression_deprioritized_skip_balancing,
    "Comet Note 5": ItemClassification.progression_deprioritized_skip_balancing,
    "Comet Note 6": ItemClassification.progression_deprioritized_skip_balancing,
    "Comet Note 7": ItemClassification.progression_deprioritized_skip_balancing,
    #Yuriko
    "Yuriko": ItemClassification.progression | ItemClassification.useful,
    "Yuriko Note 1": ItemClassification.progression_deprioritized_skip_balancing,
    "Yuriko Note 2": ItemClassification.progression_deprioritized_skip_balancing,
    "Yuriko Note 3": ItemClassification.progression_deprioritized_skip_balancing,
    "Yuriko Note 4": ItemClassification.progression_deprioritized_skip_balancing,
    "Yuriko Note 5": ItemClassification.progression_deprioritized_skip_balancing,
    "Yuriko Note 6": ItemClassification.progression_deprioritized_skip_balancing,
    #Jonas
    "Jonas": ItemClassification.progression | ItemClassification.useful,
    "Jonas Note 1": ItemClassification.progression_deprioritized_skip_balancing,
    "Jonas Note 2": ItemClassification.progression_deprioritized_skip_balancing,
    "Jonas Note 3": ItemClassification.progression_deprioritized_skip_balancing,
    "Jonas Note 4": ItemClassification.progression_deprioritized_skip_balancing,
    "Jonas Note 5": ItemClassification.progression_deprioritized_skip_balancing,
    "Jonas Note 6": ItemClassification.progression_deprioritized_skip_balancing,
    "Jonas Note 7": ItemClassification.progression_deprioritized_skip_balancing,
    #Setsu
    "Setsu": ItemClassification.progression | ItemClassification.useful,
    "Setsu Note 1": ItemClassification.progression_deprioritized_skip_balancing,
    "Setsu Note 2": ItemClassification.progression_deprioritized_skip_balancing | ItemClassification.useful,
    "Setsu Note 3": ItemClassification.progression_deprioritized_skip_balancing,
    "Setsu Note 4": ItemClassification.progression_deprioritized_skip_balancing,
    "Setsu Note 5": ItemClassification.progression_deprioritized_skip_balancing,
    "Setsu Note 6": ItemClassification.progression_deprioritized_skip_balancing,
    #Otome
    "Otome": ItemClassification.progression | ItemClassification.useful,
    "Otome Note 1": ItemClassification.progression_deprioritized_skip_balancing,
    "Otome Note 2": ItemClassification.progression_deprioritized_skip_balancing,
    "Otome Note 3": ItemClassification.progression_deprioritized_skip_balancing,
    "Otome Note 4": ItemClassification.progression_deprioritized_skip_balancing,
    "Otome Note 5": ItemClassification.progression_deprioritized_skip_balancing,
    "Otome Note 6": ItemClassification.progression_deprioritized_skip_balancing,
    #Sha-Ming
    "Sha-Ming": ItemClassification.progression | ItemClassification.useful,
    "Sha-Ming Note 1": ItemClassification.progression_deprioritized_skip_balancing,
    "Sha-Ming Note 2": ItemClassification.progression_deprioritized_skip_balancing,
    "Sha-Ming Note 3": ItemClassification.progression_deprioritized_skip_balancing,
    "Sha-Ming Note 4": ItemClassification.progression_deprioritized_skip_balancing,
    #Kukrushka
    "Kukrushka": ItemClassification.progression | ItemClassification.useful,
    "Kukrushka Note 1": ItemClassification.progression_deprioritized_skip_balancing,
    "Kukrushka Note 2": ItemClassification.progression_deprioritized_skip_balancing,
    "Kukrushka Note 3": ItemClassification.progression_deprioritized_skip_balancing,
    "Kukrushka Note 4": ItemClassification.progression_deprioritized_skip_balancing,
    "Kukrushka Note 5": ItemClassification.progression_deprioritized_skip_balancing,
    "Kukrushka Note 6": ItemClassification.progression_deprioritized_skip_balancing,
    #Roles
    "Engineer Role": ItemClassification.progression | ItemClassification.useful,
    "Doctor Role": ItemClassification.progression | ItemClassification.useful,
    "Guardian Angel Role": ItemClassification.progression | ItemClassification.useful,
    "Guard Duty Role": ItemClassification.progression | ItemClassification.useful,
    "AC Follower Role": ItemClassification.progression | ItemClassification.useful,
    "Bug Role": ItemClassification.progression | ItemClassification.useful,
    #Progressive Items
    "Progressive Crew Max": ItemClassification.progression | ItemClassification.useful,
    #Filler Items
    "End Of Loop Exp Bonus": ItemClassification.filler,
    #Traps
}

class GnosiaItem(Item):
    game = "Gnosia"

def get_random_filler_item_name(world: GnosiaWorld) -> str:
    return "End Of Loop Exp Bonus"

def get_groups() -> dict[str, set[str]]:
    #Create Groups
    skills = {
        "Step Forward",
        "Definite Human/Enemy",
        "Say You're Human",
        "Vote",
        "Don't Vote",
        "Small Talk",
        "Freeze All",
        "Let's Collaborate",
        "Seek Agreement",
        "Block Argument",
        "Exaggerate",
        "Obfuscate",
        "Retaliate",
        "Regret",
        "Seek Help",
        "Don't Be Fooled",
        "Grovel",
    }
    notes = {
        "Gina": set(),
        "SQ": set(),
        "Raqio": set(),
        "Stella": set(),
        "Shigemichi": set(),
        "Chipie": set(),
        "Remnan": set(),
        "Comet": set(),
        "Yuriko": set(),
        "Jonas": set(),
        "Setsu": set(),
        "Otome": set(),
        "Sha-Ming": set(),
        "Kukrushka": set(),
    }
    characters = set(notes.keys())
    roles = {
        "Engineer Role",
        "Doctor Role",
        "Guardian Angel Role",
        "Guard Duty Role",
        "AC Follower Role",
        "Bug Role",
    }
    #Populate Groups
    for item_name in ITEM_NAME_TO_ID:
        for character_name in notes:
            if item_name.startswith(f"{character_name} Note"):
                notes[character_name].add(item_name)
    #Return Groups
    return {
        "Skills": skills,
        "All Notes": set().union(*notes.values()),
        "Gina Notes": notes["Gina"],
        "SQ Notes": notes["SQ"],
        "Raqio Notes": notes["Raqio"],
        "Stella Notes": notes["Stella"],
        "Shigemichi Notes": notes["Shigemichi"],
        "Chipie Notes": notes["Chipie"],
        "Remnan Notes": notes["Remnan"],
        "Comet Notes": notes["Comet"],
        "Yuriko Notes": notes["Yuriko"],
        "Jonas Notes": notes["Jonas"],
        "Setsu Notes": notes["Setsu"],
        "Otome Notes": notes["Otome"],
        "Sha-Ming Notes": notes["Sha-Ming"],
        "Kukrushka Notes": notes["Kukrushka"],
        "Characters": characters,
        "Roles": roles,
    }

def create_item_with_correct_classification(world: GnosiaWorld, name: str) -> GnosiaItem:
    classification = DEFAULT_ITEM_CLASSIFICATIONS[name]
    return GnosiaItem(name, classification, ITEM_NAME_TO_ID[name], world.player)

def create_all_items(world: GnosiaWorld) -> None:
    itempool: list[Item] = [
        #Skills
        world.create_item("Step Forward"),
        world.create_item("Definite Human/Enemy"),
        world.create_item("Say You're Human"),
        world.create_item("Vote"),
        world.create_item("Don't Vote"),
        world.create_item("Small Talk"),
        world.create_item("Freeze All"),
        world.create_item("Let's Collaborate"),
        world.create_item("Seek Agreement"),
        world.create_item("Block Argument"),
        world.create_item("Exaggerate"),
        world.create_item("Obfuscate"),
        world.create_item("Retaliate"),
        world.create_item("Regret"),
        world.create_item("Seek Help"),
        world.create_item("Don't Be Fooled"),
        world.create_item("Grovel"),
        #Notes & Characters
        #Gina
        world.create_item("Gina Note 1"),
        world.create_item("Gina Note 2"),
        world.create_item("Gina Note 3"),
        world.create_item("Gina Note 4"),
        world.create_item("Gina Note 5"),
        world.create_item("Gina Note 6"),
        #SQ
        world.create_item("SQ Note 1"),
        world.create_item("SQ Note 2"),
        world.create_item("SQ Note 3"),
        world.create_item("SQ Note 4"),
        world.create_item("SQ Note 5"),
        #Raqio
        world.create_item("Raqio Note 1"),
        world.create_item("Raqio Note 2"),
        world.create_item("Raqio Note 3"),
        world.create_item("Raqio Note 4"),
        world.create_item("Raqio Note 5"),
        world.create_item("Raqio Note 6"),
        #Stella
        world.create_item("Stella Note 1"),
        world.create_item("Stella Note 2"),
        world.create_item("Stella Note 3"),
        world.create_item("Stella Note 4"),
        world.create_item("Stella Note 5"),
        #Shigemichi
        world.create_item("Shigemichi Note 1"),
        world.create_item("Shigemichi Note 2"),
        world.create_item("Shigemichi Note 3"),
        world.create_item("Shigemichi Note 4"),
        world.create_item("Shigemichi Note 5"),
        world.create_item("Shigemichi Note 6"),
        world.create_item("Shigemichi Note 7"),
        #Chipie
        world.create_item("Chipie Note 1"),
        world.create_item("Chipie Note 2"),
        world.create_item("Chipie Note 3"),
        world.create_item("Chipie Note 4"),
        world.create_item("Chipie Note 5"),
        world.create_item("Chipie Note 6"),
        #Remnan
        world.create_item("Remnan Note 1"),
        world.create_item("Remnan Note 2"),
        world.create_item("Remnan Note 3"),
        world.create_item("Remnan Note 4"),
        world.create_item("Remnan Note 5"),
        #Comet
        world.create_item("Comet Note 1"),
        world.create_item("Comet Note 2"),
        world.create_item("Comet Note 3"),
        world.create_item("Comet Note 4"),
        world.create_item("Comet Note 5"),
        world.create_item("Comet Note 6"),
        world.create_item("Comet Note 7"),
        #Yuriko
        world.create_item("Yuriko Note 1"),
        world.create_item("Yuriko Note 2"),
        world.create_item("Yuriko Note 3"),
        world.create_item("Yuriko Note 4"),
        world.create_item("Yuriko Note 5"),
        world.create_item("Yuriko Note 6"),
        #Jonas
        world.create_item("Jonas Note 1"),
        world.create_item("Jonas Note 2"),
        world.create_item("Jonas Note 3"),
        world.create_item("Jonas Note 4"),
        world.create_item("Jonas Note 5"),
        world.create_item("Jonas Note 6"),
        world.create_item("Jonas Note 7"),
        #Setsu
        world.create_item("Setsu Note 1"),
        world.create_item("Setsu Note 2"),
        world.create_item("Setsu Note 3"),
        world.create_item("Setsu Note 4"),
        world.create_item("Setsu Note 5"),
        world.create_item("Setsu Note 6"),
        #Otome
        world.create_item("Otome Note 1"),
        world.create_item("Otome Note 2"),
        world.create_item("Otome Note 3"),
        world.create_item("Otome Note 4"),
        world.create_item("Otome Note 5"),
        world.create_item("Otome Note 6"),
        #Sha-Ming
        world.create_item("Sha-Ming Note 1"),
        world.create_item("Sha-Ming Note 2"),
        world.create_item("Sha-Ming Note 3"),
        world.create_item("Sha-Ming Note 4"),
        #Kukrushka
        world.create_item("Kukrushka Note 1"),
        world.create_item("Kukrushka Note 2"),
        world.create_item("Kukrushka Note 3"),
        world.create_item("Kukrushka Note 4"),
        world.create_item("Kukrushka Note 5"),
        world.create_item("Kukrushka Note 6"),
        #Roles
        world.create_item("Engineer Role"),
        world.create_item("Doctor Role"),
        world.create_item("Guardian Angel Role"),
        world.create_item("Guard Duty Role"),
        world.create_item("AC Follower Role"),
        world.create_item("Bug Role"),
    ]

    #Check Options
    if world.options.randomize_character_unlocks:
        # Guarantee at least 4 Starting Characters
        all_characters = {
            "Gina",
            "SQ",
            "Raqio",
            "Stella",
            "Shigemichi",
            "Chipie",
            "Remnan",
            "Comet",
            "Yuriko",
            "Jonas",
            "Setsu",
            "Otome",
            "Sha-Ming",
            "Kukrushka",
        }
        # Pick random characters until you have 4 Starting Characters
        remaining_characters = all_characters.copy()
        start_inventory_from_pool = world.options.start_inventory_from_pool
        guaranteed_starting_characters = set()
        for item_name in start_inventory_from_pool:
            if item_name in all_characters:
                guaranteed_starting_characters.add(item_name)
                remaining_characters.remove(item_name)
        random_starting_characters = set()
        while len(random_starting_characters) + len(guaranteed_starting_characters) < 4:
            random_character = world.random.choice(tuple(remaining_characters))
            random_starting_characters.add(random_character)
            remaining_characters.remove(random_character)
        # Pre-Collect the chosen characters
        for character in random_starting_characters:
            world.push_precollected(world.create_item(character))
        characters = []
        # Put all non-randomly chosen characters in the pool
        # Guaranteed starting characters should get removed by AP automatically
        for character_name in all_characters - random_starting_characters:
            characters.append(world.create_item(character_name))
        itempool += characters
    else:
        for _ in range(10):
            itempool.append(world.create_item("Progressive Crew Max"))
    
    #Match number of items to number of locations
    number_of_items = len(itempool)
    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))
    needed_number_of_filler_items = number_of_unfilled_locations - number_of_items

    itempool += [world.create_filler() for _ in range(needed_number_of_filler_items)]

    world.multiworld.itempool += itempool