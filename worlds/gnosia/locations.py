from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Location
from . import items

from copy import deepcopy

if TYPE_CHECKING:
    from .world import GnosiaWorld



LOCATION_NAME_TO_ID = {
    #Skill Locations
    "Learn About Step Forward": 1,
    "Learn About Definite Human/Enemy": 2,
    "Learn About Say You're Human": 5,
    "Learn About Vote": 6,
    "Learn About Don't Vote": 7,
    "Learn About Small Talk": 8,
    "Learn About Freeze All": 9,
    "Learn About Let's Collaborate": 10,
    "Learn About Seek Agreement": 11,
    "Learn About Block Argument": 12,
    "Learn About Exaggerate": 13,
    "Learn About Obfuscate": 14,
    "Learn About Retaliate": 15,
    "Learn About Regret": 16,
    "Learn About Seek Help": 17,
    "Learn About Don't Be Fooled": 18,
    "Learn About Grovel": 19,
    #Note & Meet Locations
    #Gina
    "Meet Gina": 100,
    "Learn About Gina 1": 101,
    "Learn About Gina 2": 102,
    "Learn About Gina 3": 103,
    "Learn About Gina 4": 104,
    "Learn About Gina 5": 105,
    "Learn About Gina 6": 106,
    #SQ
    "Meet SQ": 200,
    "Learn About SQ 1": 201,
    "Learn About SQ 2": 202,
    "Learn About SQ 3": 203,
    "Learn About SQ 4": 204,
    "Learn About SQ 5": 205,
    #Raqio
    "Meet Raqio": 300,
    "Learn About Raqio 1": 301,
    "Learn About Raqio 2": 302,
    "Learn About Raqio 3": 303,
    "Learn About Raqio 4": 304,
    "Learn About Raqio 5": 305,
    "Learn About Raqio 6": 306,
    #Stella
    "Meet Stella": 400,
    "Learn About Stella 1": 401,
    "Learn About Stella 2": 402,
    "Learn About Stella 3": 403,
    "Learn About Stella 4": 404,
    "Learn About Stella 5": 405,
    #Shigemichi
    "Meet Shigemichi": 500,
    "Learn About Shigemichi 1": 501,
    "Learn About Shigemichi 2": 502,
    "Learn About Shigemichi 3": 503,
    "Learn About Shigemichi 4": 504,
    "Learn About Shigemichi 5": 505,
    "Learn About Shigemichi 6": 506,
    "Learn About Shigemichi 7": 507,
    #Chipie
    "Meet Chipie": 600,
    "Learn About Chipie 1": 601,
    "Learn About Chipie 2": 602,
    "Learn About Chipie 3": 603,
    "Learn About Chipie 4": 604,
    "Learn About Chipie 5": 605,
    "Learn About Chipie 6": 606,
    #Remnan
    "Meet Remnan": 700,
    "Learn About Remnan 1": 701,
    "Learn About Remnan 2": 702,
    "Learn About Remnan 3": 703,
    "Learn About Remnan 4": 704,
    "Learn About Remnan 5": 705,
    #Comet
    "Meet Comet": 800,
    "Learn About Comet 1": 801,
    "Learn About Comet 2": 802,
    "Learn About Comet 3": 803,
    "Learn About Comet 4": 804,
    "Learn About Comet 5": 805,
    "Learn About Comet 6": 806,
    "Learn About Comet 7": 807,
    #Yuriko
    "Meet Yuriko": 900,
    "Learn About Yuriko 1": 901,
    "Learn About Yuriko 2": 902,
    "Learn About Yuriko 3": 903,
    "Learn About Yuriko 4": 904,
    "Learn About Yuriko 5": 905,
    "Learn About Yuriko 6": 906,
    #Jonas
    "Meet Jonas": 1000,
    "Learn About Jonas 1": 1001,
    "Learn About Jonas 2": 1002,
    "Learn About Jonas 3": 1003,
    "Learn About Jonas 4": 1004,
    "Learn About Jonas 5": 1005,
    "Learn About Jonas 6": 1006,
    "Learn About Jonas 7": 1007,
    #Setsu
    "Meet Setsu": 1100,
    "Learn About Setsu 1": 1101,
    "Learn About Setsu 2": 1102,
    "Learn About Setsu 3": 1103,
    "Learn About Setsu 4": 1104,
    "Learn About Setsu 5": 1105,
    "Learn About Setsu 6": 1106,
    #Otome
    "Meet Otome": 1200,
    "Learn About Otome 1": 1201,
    "Learn About Otome 2": 1202,
    "Learn About Otome 3": 1203,
    "Learn About Otome 4": 1204,
    "Learn About Otome 5": 1205,
    "Learn About Otome 6": 1206,
    #Sha-Ming
    "Meet Sha-Ming": 1300,
    "Learn About Sha-Ming 1": 1301,
    "Learn About Sha-Ming 2": 1302,
    "Learn About Sha-Ming 3": 1303,
    "Learn About Sha-Ming 4": 1304,
    #Kukrushka
    "Meet Kukrushka": 1400,
    "Learn About Kukrushka 1": 1401,
    "Learn About Kukrushka 2": 1402,
    "Learn About Kukrushka 3": 1403,
    "Learn About Kukrushka 4": 1404,
    "Learn About Kukrushka 5": 1405,
    "Learn About Kukrushka 6": 1406,
    #Role Locations
    "Learn About Engineer Role": 1501,
    "Learn About Doctor Role": 1502,
    "Learn About Guardian Angel Role": 1503,
    "Learn About Guard Duty Role": 1504,
    "Learn About AC Follower Role": 1506,
    "Beat The Bug Loop": 1508,
    #Role Achievement Locations
    "Intrepid Investigator Achievement": 1601,
    "Guardian Angel Achievement": 1603,
    "Hero Achievement": 1605,
    "Loyal Servant Achievement": 1606,
    "Lonely Battle Achievement": 1607,
    "Destroyer of the Universe Achievement": 1608,
    #Win As Role Locations
    "Win As Engineer": 1701,
    "Win As Doctor": 1702,
    "Win As Guardian Angel": 1703,
    "Win As Guard Duty": 1704,
    "Win As Crew Member": 1705,
    "Win As AC Follower": 1706,
    "Win As Gnosia": 1707,
    "Win As Bug": 1708,
    #Win Against Role Locations
    "Win Against Engineer": 1801,
    "Win Against Doctor": 1802,
    "Win Against Guardian Angel": 1803,
    "Win Against Guard Duty": 1804,
    "Win Against Crew Member": 1805,
    "Win Against AC Follower": 1806,
    "Win Against Gnosia": 1807,
    "Win Against Bug": 1808,
    #Win With Character Locations
    "Win With Gina": 1901,
    "Win With SQ": 1902,
    "Win With Raqio": 1903,
    "Win With Stella": 1904,
    "Win With Shigemichi": 1905,
    "Win With Chipie": 1906,
    "Win With Remnan": 1907,
    "Win With Comet": 1908,
    "Win With Yuriko": 1909,
    "Win With Jonas": 1910,
    "Win With Setsu": 1911,
    "Win With Otome": 1912,
    "Win With Sha-Ming": 1913,
    "Win With Kukrushka": 1914,
    #Win Against Character Locations
    "Win Against Gina": 2001,
    "Win Against SQ": 2002,
    "Win Against Raqio": 2003,
    "Win Against Stella": 2004,
    "Win Against Shigemichi": 2005,
    "Win Against Chipie": 2006,
    "Win Against Remnan": 2007,
    "Win Against Comet": 2008,
    "Win Against Yuriko": 2009,
    "Win Against Jonas": 2010,
    "Win Against Setsu": 2011,
    "Win Against Otome": 2012,
    "Win Against Sha-Ming": 2013,
    "Win Against Kukrushka": 2014,
}

TUTORIAL_LOOP_CHARACTER_LOCATIONS = {
    "Loop 1": {
        "Meet Setsu",
        "Meet Gina",
        "Meet SQ",
        "Meet Raqio",
    },
    "Loop 3": {
        "Meet Stella",
        "Meet Shigemichi",
    },
    "Loop 5": {
        "Meet Yuriko",
    },
    "Loop 7": {
        "Meet Chipie",
        "Meet Comet",
    },
    "Loop 10": {
        "Meet Jonas",
        "Meet Kukrushka",
    },
    "Loop 12": {
        "Meet Otome",
        "Meet Sha-Ming",
    },
    "Loop 13": {
        "Meet Remnan",
    },
}

TUTORIAL_LOOP_ROLE_LOCATIONS = {
    "Loop 2": {
        "Learn About Engineer Role",
    },
    "Loop 4": {
        "Learn About Guardian Angel Role",
    },
    "Loop 9": {
        "Learn About AC Follower Role",
    },
    "Loop 10": {
        "Learn About Doctor Role",
    },
    "Loop 13": {
        "Learn About Guard Duty Role",
    },
    "Bug Loop": {
        "Beat The Bug Loop",
    },
}

TUTORIAL_LOOP_NOTE_LOCATIONS = {
    "Loop 11": {
        "Learn About Gina 1",
        "Learn About SQ 1",
        "Learn About Raqio 1",
        "Learn About Stella 1",
        "Learn About Shigemichi 1",
        "Learn About Chipie 1",
        "Learn About Comet 1",
        "Learn About Jonas 1",
        "Learn About Setsu 1",
        "Learn About Kukrushka 1",
    },
    "Loop 12": {
        "Learn About Sha-Ming 1",
    },
    "Loop 13": {
        "Learn About Remnan 1",
        "Learn About Otome 1",
        "Learn About Yuriko 1",
    },
}

SKILL_LOCATIONS = {
    "Step Forward Event": {"Learn About Step Forward"},
    "Raqio Quiz - Definite Human/Enemy": {"Learn About Definite Human/Enemy"},
    "Say You're Human Event": {"Learn About Say You're Human"},
    "Tears Go By": {"Learn About Vote"},
    "Don't Vote Event": {"Learn About Don't Vote"},
    "Small Talk Event": {"Learn About Small Talk"},
    "Raqio Quiz - Freeze All": {"Learn About Freeze All"},
    "Let's Collaborate Event": {"Learn About Let's Collaborate"},
    "Seek Agreement Event": {"Learn About Seek Agreement"},
    "Chaos": {"Learn About Block Argument"},
    "Exaggerate Event": {"Learn About Exaggerate"},
    "Obfuscate Event": {"Learn About Obfuscate"},
    "Retaliate Event": {"Learn About Retaliate"},
    "Regret Event": {"Learn About Regret"},
    "Fool And Be Fooled": {"Learn About Seek Help"},
    "Don't Be Fooled Event": {"Learn About Don't Be Fooled"},
    "Ace In The Hole": {"Learn About Grovel"},
}

NON_TUTORIAL_NOTE_LOCATIONS = {
    "Setsu Note 2 Event": {"Learn About Setsu 2"},
    "Setsu Note 3 Event": {"Learn About Setsu 3"},
    "Setsu Note 4 Region": {"Learn About Setsu 4"},
    "To The Hangar": {"Learn About Kukrushka 5"},
    "Setsu's Origins": {"Learn About Setsu 6"},
    "Let's Play": {"Learn About Setsu 5"},
    "Gina Note 2 Event": {"Learn About Gina 2"},
    "Gina Note 3 Event": {"Learn About Gina 3"},
    "Don't Be Fooled Event": {"Learn About Gina 4"},
    "Allacosia": {"Learn About Gina 5"},
    "Gina Note 6 Event": {"Learn About Gina 6"},
    "SQ Note 2 Region": {"Learn About SQ 2", "Learn About Remnan 3"},
    "Inescapable Past": {"Learn About SQ 3", "Learn About Remnan 4"},
    "Fool And Be Fooled": {"Learn About SQ 4"},
    "Tears Of SQ": {"Learn About SQ 5"},
    "Raqio Note 2 Event": {"Learn About Raqio 2"},
    "Shower Room - Raqio": {"Learn About Raqio 3"},
    "Raqio Quiz - Note 4": {"Learn About Raqio 4"},
    "Raqio Quiz - Note 5": {"Learn About Raqio 5"},
    "Raqio Note 6 Event": {"Learn About Raqio 6"},
    "Shigemichi In Love": {"Learn About Stella 2", "Learn About Shigemichi 7"},
    "Flowers": {"Learn About Stella 3"},
    "Jonas The Wreck": {"Learn About Stella 4", "Learn About Jonas 4"},
    "Stella Note 5 Event": {"Learn About Stella 5"},
    "Chipie & Shigemichi Note Event": {"Learn About Shigemichi 2", "Learn About Chipie 6"},
    "Shower Room - Shigemichi": {"Learn About Shigemichi 3"},
    "Shigemichi Note 4 Event": {"Learn About Shigemichi 4"},
    "Game Sermon": {"Learn About Shigemichi 5", "Learn About Jonas 6"},
    "Shigemichi Note 6 Event": {"Learn About Shigemichi 6"},
    "Let's Collaborate Event": {"Learn About Chipie 3"},
    "Chipie Note 2 Region": {"Learn About Chipie 2"},
    "Chipie & Comet Note Event": {"Learn About Chipie 4", "Learn About Comet 3"},
    "Chipie Note 5 Event": {"Learn About Chipie 5"},
    "Comet Note 2 Event": {"Learn About Comet 2"},
    "Comet Note 4 Event": {"Learn About Comet 4"},
    "Shower Room - Comet": {"Learn About Comet 5"},
    "Citizen Slime": {"Learn About Comet 6"},
    "Adventure In A Frozen World": {"Learn About Comet 7"},
    "Jonas Note 2 Region": {"Learn About Jonas 2"},
    "Jonas Note 3 Event": {"Learn About Jonas 3"},
    "The Kukrushka Problem": {"Learn About Jonas 5", "Learn About Kukrushka 3"},
    "Jonas & Kukrushka Note Event": {"Learn About Jonas 7", "Learn About Kukrushka 6"},
    "Kukrushka & Otome Note Event": {"Learn About Kukrushka 2", "Learn About Otome 5"},
    "Kukrushka The Guard": {"Learn About Kukrushka 4"},
    "Otome Note 2 Event": {"Learn About Otome 2"},
    "Otome & Sha-Ming Note Event": {"Learn About Otome 3", "Learn About Sha-Ming 2"},
    "Don't Vote Event": {"Learn About Otome 4"},
    "Otome's Resolution": {"Learn About Otome 6"},
    "Sha-Ming's Promise": {"Learn About Sha-Ming 3"},
    "Ace In The Hole": {"Learn About Sha-Ming 4"},
    "Remnan Note 2 Event": {"Learn About Remnan 2"},
    "Hope For The Future": {"Learn About Remnan 5"},
    "Starship Oracle": {"Learn About Yuriko 2", "Learn About Yuriko 3"},
    "Confrontation": {"Learn About Yuriko 4"},
    "The Alien Gnos": {"Learn About Yuriko 5"},
    "The Final Problem": {"Learn About Yuriko 6"},
}

class GnosiaLocation(Location):
    game = "Gnosia"

def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {location_name: LOCATION_NAME_TO_ID[location_name] for location_name in location_names}

def get_groups() -> dict[str, set[str]]:
    #Create Groups
    skills = set()
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
    characters = {f"Meet {character}" for character in notes}
    roles = set()
    achievements = set()
    win_with_characters = set()
    win_against_characters = set()
    win_as_roles = set()
    win_against_roles = set()
    #Populate Groups
    for location_name in LOCATION_NAME_TO_ID:
        #Skip Characters
        if location_name in characters:
            continue
        was_note = False
        for character_name in notes:
            if location_name.startswith(f"Learn About {character_name}"):
                notes[character_name].add(location_name)
                was_note = True
                break
        if was_note:
            continue
        if location_name.endswith(" Role"):
            roles.add(location_name)
        elif location_name.endswith(" Achievement"):
            achievements.add(location_name)
        elif location_name.startswith("Win With "):
            win_with_characters.add(location_name)
        elif location_name.startswith("Win Against "):
            if any(character in location_name for character in notes):
                win_against_characters.add(location_name)
            else:
                win_against_roles.add(location_name)
        elif location_name.startswith("Win As "):
            win_as_roles.add(location_name)
        else:
            skills.add(location_name)
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
        "Achievements": achievements,
        "Win With Characters": win_with_characters,
        "Win Against Characters": win_against_characters,
        "Win As Roles": win_as_roles,
        "Win Against Roles": win_against_roles,
    }

def create_all_locations(world: GnosiaWorld) -> None:
    create_regular_locations(world)
    create_events(world)

def create_regular_locations(world: GnosiaWorld) -> None:
    from .options import TutorialHandling
    region_to_locations: dict[str, set[str]] = {}
    #Add Tutorial Loop Locations
    if world.options.tutorial_handling != TutorialHandling.option_skip_and_remove_locations:
        region_to_locations |= deepcopy(TUTORIAL_LOOP_CHARACTER_LOCATIONS)
        if world.options.randomize_notes:
            for region, locations in TUTORIAL_LOOP_NOTE_LOCATIONS.items():
                region_to_locations.setdefault(region, set()).update(locations)
        if world.options.randomize_role_unlocks:
            for region, locations in TUTORIAL_LOOP_ROLE_LOCATIONS.items():
                region_to_locations.setdefault(region, set()).update(locations)
    #Add Skill Locations
    if world.options.randomize_skills:
        for region, locations in SKILL_LOCATIONS.items():
            region_to_locations.setdefault(region, set()).update(locations)
    #Add Note Locations
    if world.options.randomize_notes:
        for region, locations in NON_TUTORIAL_NOTE_LOCATIONS.items():
            region_to_locations.setdefault(region, set()).update(locations)
    #Add Extra Locations
    region_to_locations["Setup"] = set()
    groups = get_groups()
    if world.options.add_role_achievement_locations:
        region_to_locations["Setup"].update(groups["Achievements"])
    if world.options.add_win_with_character_locations:
        region_to_locations["Setup"].update(groups["Win With Characters"])
    if world.options.add_win_against_character_locations:
        region_to_locations["Setup"].update(groups["Win Against Characters"])
    if world.options.add_win_as_role_locations:
        region_to_locations["Setup"].update(groups["Win As Roles"])
    if world.options.add_win_against_role_locations:
        region_to_locations["Setup"].update(groups["Win Against Roles"])
    for region_name in region_to_locations:
        locations = get_location_names_with_ids(sorted(region_to_locations[region_name]))
        world.get_region(region_name).add_locations(locations, GnosiaLocation)


def create_events(world: GnosiaWorld) -> None:
    from .options import Goal
    #Add Always Events
    events = {
        "Gina Gnosia Result Event": ("Select: \"I love you\"", "Gina Romance Chain Started"),
        "Raqio Quiz - Definite Human/Enemy": ("Watch RQ - DH/E", "Event Seen: RQ - DH/E"),
        "The Alien Gnos": ("Complete The Alien Gnos", "Event Completed: The Alien Gnos"),
        "A World Without Gnosia - First Time Ver.": ("Watch AWWG", "Event Seen: AWWG"),
        "Allacosia": ("Complete Allacosia", "Event Completed: Allacosia"),
        "Sha-Ming Gnosia Ally Intro": ("Watch Sha-Ming Gnosia Ally Intro", "Event Seen: Sha-Ming Gnosia Ally Intro"),
        "A World Without Gnosia - Normal Ending Ver.": ("Get Normal Ending", "Event Seen: Normal Ending"),
        "After The Final Problem Result Event": ("Watch ATFPRE", "Can Set Gnosia to Zero"),
        "Bug Tutorial": ("Unlock Event Search", "Event Search"),
    }
    for region_name, (location, item) in events.items():
        world.get_region(region_name).add_event(location, item, location_type = GnosiaLocation, item_type = items.GnosiaItem)
    #Add optional events
    optional: dict[str, set[tuple[str, str]]] = {}
    if world.options.allow_gender_specific_logic:
        optional.setdefault("Shower Room - Gina", set()).add(('Select: "Apologize"', "Apologized to Gina in Shower Room"))
    if not world.options.randomize_notes:
        for region_name, locations in (TUTORIAL_LOOP_NOTE_LOCATIONS | NON_TUTORIAL_NOTE_LOCATIONS).items():
            for location_name in locations:
                words = location_name.split()
                item_name = f"{words[2]} Note {words[3]}"
                optional.setdefault(region_name, set()).add((location_name, item_name))
    if not world.options.randomize_role_unlocks:
        for region_name, locations in TUTORIAL_LOOP_ROLE_LOCATIONS.items():
            for location_name in locations:
                item_name = "Bug Role"
                if location_name != "Beat The Bug Loop":
                    item_name = location_name.removeprefix("Learn About ")
                optional.setdefault(region_name, set()).add((location_name, item_name))
    if not world.options.randomize_skills:
        for region_name, locations in SKILL_LOCATIONS.items():
            for location_name in locations:
                item_name = location_name.removeprefix("Learn About ")
                optional.setdefault(region_name, set()).add((location_name, item_name))
    if not world.options.add_role_achievement_locations and world.options.goal == Goal.option_role_achievements:
        #Add Achievement Events
        locations = get_groups()["Achievements"]
        for location_name in locations:
            optional.setdefault("Setup", set()).add((location_name, "Nothing"))
    for region_name in optional:
        for location, item in sorted(optional[region_name]):
            world.get_region(region_name).add_event(location, item, location_type = GnosiaLocation, item_type = items.GnosiaItem)