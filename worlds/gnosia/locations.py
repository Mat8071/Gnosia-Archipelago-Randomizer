from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Location
from . import items

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
}

class GnosiaLocation(Location):
    game = "Gnosia"

def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {location_name: LOCATION_NAME_TO_ID[location_name] for location_name in location_names}

def get_groups() -> dict[str, set[str]]:
    # Create Groups
    skills = set()
    notes = set()
    characters = set()
    roles = set()
    # Populate Groups
    for location_name in LOCATION_NAME_TO_ID:
        current_id = LOCATION_NAME_TO_ID[location_name]
        if current_id < 100:
            skills.add(location_name)
        elif 100 <= current_id < 1500:
            if current_id % 100 == 0:
                characters.add(location_name)
            else:
                notes.add(location_name)
        elif 1500 <= current_id < 1600:
            roles.add(location_name)
    # Return Groups
    return {
        "Skills": skills,
        "Notes": notes,
        "Characters": characters,
        "Roles": roles,
    }

def create_all_locations(world: GnosiaWorld) -> None:
    create_regular_locations(world)
    create_events(world)

def create_regular_locations(world: GnosiaWorld) -> None:
    #Get Tutorial Loops Regions
    tutorial_loops = []
    for i in range(13):
        tutorial_loops.append(world.get_region(f"Loop {i + 1}"))
    #Add Tutorial Loop Locations
    tutorial_loop_locations = {
        tutorial_loops[0]: ["Meet Setsu", "Meet Gina", "Meet SQ", "Meet Raqio"],
        tutorial_loops[1]: ["Learn About Engineer Role"],
        tutorial_loops[2]: ["Meet Stella", "Meet Shigemichi"],
        tutorial_loops[3]: ["Learn About Guardian Angel Role"],
        tutorial_loops[4]: ["Meet Yuriko"],
        tutorial_loops[5]: [],
        tutorial_loops[6]: ["Meet Chipie", "Meet Comet"],
        tutorial_loops[7]: [],
        tutorial_loops[8]: ["Learn About AC Follower Role"],
        tutorial_loops[9]: ["Learn About Doctor Role", "Meet Jonas", "Meet Kukrushka"],
        tutorial_loops[10]: [
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
        ],
        tutorial_loops[11]: ["Meet Otome", "Meet Sha-Ming", "Learn About Sha-Ming 1"],
        tutorial_loops[12]: [
            "Meet Remnan", 
            "Learn About Guard Duty Role", 
            "Learn About Remnan 1", 
            "Learn About Otome 1",
            "Learn About Yuriko 1",
        ],
    }
    for loop in tutorial_loops:
        if tutorial_loop_locations[loop]:
            locations = get_location_names_with_ids(tutorial_loop_locations[loop])
            loop.add_locations(locations, GnosiaLocation)
    #Add Bug Loop Locations
    bug_loop_locations = get_location_names_with_ids(["Beat The Bug Loop"])
    world.get_region("Bug Loop").add_locations(bug_loop_locations, GnosiaLocation)
    #Add Skill Locations
    skill_locations = {
        "Step Forward Event": ["Learn About Step Forward"],
        "Raqio Quiz - Definite Human/Enemy": ["Learn About Definite Human/Enemy"],
        "Say You're Human Event": ["Learn About Say You're Human"],
        "Tears Go By": ["Learn About Vote"],
        "Don't Vote Event": ["Learn About Don't Vote"],
        "Small Talk Event": ["Learn About Small Talk"],
        "Raqio Quiz - Freeze All": ["Learn About Freeze All"],
        "Let's Collaborate Event": ["Learn About Let's Collaborate"],
        "Seek Agreement Event": ["Learn About Seek Agreement"],
        "Chaos": ["Learn About Block Argument"],
        "Exaggerate Event": ["Learn About Exaggerate"],
        "Obfuscate Event": ["Learn About Obfuscate"],
        "Retaliate Event": ["Learn About Retaliate"],
        "Regret Event": ["Learn About Regret"],
        "Fool And Be Fooled": ["Learn About Seek Help"],
        "Don't Be Fooled Event": ["Learn About Don't Be Fooled"],
        "Ace In The Hole": ["Learn About Grovel"],
    }
    for region_name in skill_locations:
        locations = get_location_names_with_ids(skill_locations[region_name])
        world.get_region(region_name).add_locations(locations, GnosiaLocation)
    #Add Note Locations
    note_locations = {
        "Setsu Note 2 Event": ["Learn About Setsu 2"],
        "Setsu Note 3 Event": ["Learn About Setsu 3"],
        "Setsu Note 4 Region": ["Learn About Setsu 4"],
        "To The Hangar": ["Learn About Kukrushka 5"],
        "Setsu's Origins": ["Learn About Setsu 6"],
        "Let's Play": ["Learn About Setsu 5"],
        "Gina Note 2 Event": ["Learn About Gina 2"],
        "Gina Note 3 Event": ["Learn About Gina 3"],
        "Don't Be Fooled Event": ["Learn About Gina 4"],
        "Allacosia": ["Learn About Gina 5"],
        "Gina Note 6 Event": ["Learn About Gina 6"],
        "SQ Note 2 Region": ["Learn About SQ 2", "Learn About Remnan 3"],
        "Inescapable Past": ["Learn About SQ 3", "Learn About Remnan 4"],
        "Fool And Be Fooled": ["Learn About SQ 4"],
        "Tears Of SQ": ["Learn About SQ 5"],
        "Raqio Note 2 Event": ["Learn About Raqio 2"],
        "Shower Room - Raqio": ["Learn About Raqio 3"],
        "Raqio Quiz - Note 4": ["Learn About Raqio 4"],
        "Raqio Quiz - Note 5": ["Learn About Raqio 5"],
        "Raqio Note 6 Event": ["Learn About Raqio 6"],
        "Shigemichi In Love": ["Learn About Stella 2", "Learn About Shigemichi 7"],
        "Flowers": ["Learn About Stella 3"],
        "Jonas The Wreck": ["Learn About Stella 4", "Learn About Jonas 4"],
        "Stella Note 5 Event": ["Learn About Stella 5"],
        "Chipie & Shigemichi Note Event": ["Learn About Shigemichi 2", "Learn About Chipie 6"],
        "Shower Room - Shigemichi": ["Learn About Shigemichi 3"],
        "Shigemichi Note 4 Event": ["Learn About Shigemichi 4"],
        "Game Sermon": ["Learn About Shigemichi 5", "Learn About Jonas 6"],
        "Shigemichi Note 6 Event": ["Learn About Shigemichi 6"],
        "Let's Collaborate Event": ["Learn About Chipie 3"],
        "Chipie Note 2 Region": ["Learn About Chipie 2"],
        "Chipie & Comet Note Event": ["Learn About Chipie 4", "Learn About Comet 3"],
        "Chipie Note 5 Event": ["Learn About Chipie 5"],
        "Comet Note 2 Event": ["Learn About Comet 2"],
        "Comet Note 4 Event": ["Learn About Comet 4"],
        "Shower Room - Comet": ["Learn About Comet 5"],
        "Citizen Slime": ["Learn About Comet 6"],
        "Adventure In A Frozen World": ["Learn About Comet 7"],
        "Jonas Note 2 Region": ["Learn About Jonas 2"],
        "Jonas Note 3 Event": ["Learn About Jonas 3"],
        "The Kukrushka Problem": ["Learn About Jonas 5", "Learn About Kukrushka 3"],
        "Jonas & Kukrushka Note Event": ["Learn About Jonas 7", "Learn About Kukrushka 6"],
        "Kukrushka & Otome Note Event": ["Learn About Kukrushka 2", "Learn About Otome 5"],
        "Kukrushka The Guard": ["Learn About Kukrushka 4"],
        "Otome Note 2 Event": ["Learn About Otome 2"],
        "Otome & Sha-Ming Note Event": ["Learn About Otome 3", "Learn About Sha-Ming 2"],
        "Don't Vote Event": ["Learn About Otome 4"],
        "Otome's Resolution": ["Learn About Otome 6"],
        "Sha-Ming's Promise": ["Learn About Sha-Ming 3"],
        "Ace In The Hole": ["Learn About Sha-Ming 4"],
        "Remnan Note 2 Event": ["Learn About Remnan 2"],
        "Hope For The Future": ["Learn About Remnan 5"],
        "Starship Oracle": ["Learn About Yuriko 2", "Learn About Yuriko 3"],
        "Confrontation": ["Learn About Yuriko 4"],
        "The Alien Gnos": ["Learn About Yuriko 5"],
        "The Final Problem": ["Learn About Yuriko 6"],
    }
    for region_name in note_locations:
        locations = get_location_names_with_ids(note_locations[region_name])
        world.get_region(region_name).add_locations(locations, GnosiaLocation)


def create_events(world: GnosiaWorld) -> None:
    events = {
        "Gina Gnosia Result Event": ["Select: \"I love you\"", "Gina Romance Chain Started"],
        "Raqio Quiz - Definite Human/Enemy": ["Watch RQ - DH/E", "Event Seen: RQ - DH/E"],
        "The Alien Gnos": ["Complete The Alien Gnos", "Event Completed: The Alien Gnos"],
        "A World Without Gnosia - First Time Ver.": ["Watch AWWG", "Event Seen: AWWG"],
        "Allacosia": ["Complete Allacosia", "Event Completed: Allacosia"],
        "Sha-Ming Gnosia Ally Intro": ["Watch Sha-Ming Gnosia Ally Intro", "Event Seen: Sha-Ming Gnosia Ally Intro"],
        "A World Without Gnosia - Normal Ending Ver.": ["Get Normal Ending", "Event Seen: Normal Ending"],
        "After The Final Problem Result Event": ["Watch ATFPRE", "Can Set Gnosia to Zero"],
    }
    for region_name in events:
        world.get_region(region_name).add_event(events[region_name][0], events[region_name][1], location_type = GnosiaLocation, item_type = items.GnosiaItem)
    #Add optional events
    if world.options.allow_gender_specific_logic:
        world.get_region("Shower Room - Gina").add_event("Select: \"Apologize\"", "Apologized to Gina in Shower Room")