from __future__ import annotations
from typing import TYPE_CHECKING
from math import ceil

import rule_builder.rules
from Options import OptionError
from rule_builder.options import OptionFilter
from rule_builder.rules import True_, Has, HasAny, HasAll, HasGroupUnique, CanReachRegion

from .options import RandomizeCharacterUnlocks, Goal
from . import items

if TYPE_CHECKING:
    from .world import GnosiaWorld

def get_stat_rule(stat_name: str, stat_min: int) -> rule_builder.rules.Rule:
    #TODO: Implement this when levelsanity is a thing
    return True_() #For now...

def check_stats(arg1: list, arg2: list) -> bool:
    for i in range(min(len(arg1), len(arg2))):
        if arg1[i] < arg2[i]:
            return False
    return True

def raise_stats(starting_stats: list, current_stats: list, max_stats: list, total_notes: int):
    for i in range(min(len(starting_stats), len(current_stats), len(max_stats))):
        current_stats[i] += ((max_stats[i] - starting_stats[i]) / total_notes) / 2

def get_npc_skill_rule(npc_name: str, skill_name: str) -> rule_builder.rules.Rule:
    npc_starting_stats = {
        "Gina": [3.5, 4, 7.5, 10, 2, 9],
        "SQ": [5.5, 11, 15.5, 2.5, 14.5, 3],
        "Raqio": [3, 0.5, 2, 20.5, 11, 4.5],
        "Stella": [7.5, 5, 1.5, 13, 5, 7.5],
        "Shigemichi": [17, 3.5, 0.5, 2, 0.5, 16],
        "Chipie": [10, 17, 13.5, 7.5, 10.5, 15],
        "Remnan": [2, 21, 10, 15, 13, 22.5],
        "Comet": [5.5, 25.5, 11, 0.5, 4.5, 7.5],
        "Yuriko": [25.5, 20.5, 17.5, 22, 25, 12],
        "Jonas": [16.5, 9.5, 7, 12, 19.5, 15.5],
        "Setsu": [10, 8, 11, 12, 9.5, 3.5],
        "Otome": [7.5, 16.5, 20.5, 24, 11, 13.5],
        "Sha-Ming": [14.5, 5.5, 16.5, 6.5, 20.5, 25],
        "Kukrushka": [4.5, 16, 22.5, 0.5, 20.5, 17.5],
    }
    npc_final_stats = {
        "Gina": [17.5, 45.5, 24, 31.5, 13, 31.5],
        "SQ": [22, 21.5, 46, 12, 47.5, 38.5],
        "Raqio": [16.5, 0.5, 7.5, 49.5, 35.5, 20.5],
        "Stella": [27, 18, 27.5, 42, 30.5, 29],
        "Shigemichi": [45.5, 14.5, 17.5, 9.5, 6, 45],
        "Chipie": [25, 39, 31, 18.5, 26.5, 33.5],
        "Remnan": [2, 41, 29, 28, 33, 43.5],
        "Comet": [17, 49.5, 32.5, 0.5, 16.5, 22],
        "Yuriko": [49.5, 42, 37.5, 44, 49.5, 25],
        "Jonas": [38.5, 25, 21.5, 34, 43.5, 37],
        "Setsu": [35, 28.5, 36.5, 38.5, 31, 17.5],
        "Otome": [16, 32, 42, 46.5, 23, 26.5],
        "Sha-Ming": [29, 6.5, 34.5, 6.5, 40.5, 49.5],
        "Kukrushka": [14, 35.5, 49.5, 3.5, 45, 40.5],
    }
    skill_stat_requirements = {
        "Step Forward": [9.5, 0, 0, 0, 0, 0],
        "Definite Human/Enemy": [0, 0, 0, 19.5, 0, 0],
        "Definite AC Follower": [0, 0, 0, 24.5, 0, 0],
        "Definite Bug": [0, 0, 0, 29.5, 0, 0],
        "Say You're Human": [0, 19.5, 0, 0, 0, 0],
        "Vote": [0, 0, 0, 9.5, 0, 0],
        "Don't Vote": [0, 0, 0, 14.5, 0, 0],
        "Small Talk": [0, 0, 0, 0, 0, 9.5],
        "Freeze All": [0, 0, 0, 29.5, 0, 0],
        "Let's Collaborate": [0, 0, 14.5, 0, 0, 0],
        "Seek Agreement": [24.5, 0, 0, 0, 0, 0],
        "Block Argument": [39.5, 0, 0, 0, 0, 0],
        "Exaggerate": [0, 0, 0, 0, 14.5, 0],
        "Obfuscate": [0, 0, 0, 0, 0, 24.5],
        "Retaliate": [0, 0, 0, 24.5, 24.5, 0],
        "Regret": [0, 0, 24.5, 0, 0, 0],
        "Seek Help": [0, 0, 0, 0, 29.5, 0],
        "Don't Be Fooled": [0, 29.5, 0, 0, 0, 0],
        "Grovel": [0, 0, 0, 0, 0, 34.5],
    }
    thing_to_check = f"{npc_name} Notes"
    total_character_notes = len(items.get_groups().get(thing_to_check, []))
    number_of_notes_required = 0
    current_stats = npc_starting_stats[npc_name].copy()
    if check_stats(current_stats, skill_stat_requirements[skill_name]):
        return True_()
    else:
        for _ in range(total_character_notes):
            number_of_notes_required += 1
            raise_stats(npc_starting_stats[npc_name], current_stats, npc_final_stats[npc_name], total_character_notes)
            if check_stats(current_stats, skill_stat_requirements[skill_name]):
                break
    return HasGroupUnique(thing_to_check, number_of_notes_required)

def forbidden_role_rule(role_name: str) -> rule_builder.rules.Rule:
    #TODO: Implement this when player crew and player gnosia are randomized
    return True_() #For Now...

def get_min_crew_rule(minimum: int) -> rule_builder.rules.Rule:
    return HasGroupUnique("Characters", minimum - 1) | Has("Progressive Crew Max", minimum - 5)

def set_all_rules(world: GnosiaWorld) -> None:
    set_all_entrance_rules(world)
    set_all_location_rules(world)
    set_completion_condition(world)

def set_all_entrance_rules(world: GnosiaWorld) -> None:
    #Define Common Rules
    #Character Rules
    characters_randomized = OptionFilter(RandomizeCharacterUnlocks, True)
    characters_not_randomized = OptionFilter(RandomizeCharacterUnlocks, False)
    has_gina = Has("Gina") | characters_not_randomized
    has_sq = Has("SQ") | characters_not_randomized
    has_raqio = Has("Raqio") | characters_not_randomized
    has_stella = Has("Stella") | characters_not_randomized
    has_shigemichi = Has("Shigemichi") | characters_not_randomized
    has_chipie = Has("Chipie") | characters_not_randomized
    has_remnan = Has("Remnan") | characters_not_randomized
    has_comet = Has("Comet") | characters_not_randomized
    has_yuriko = Has("Yuriko") | characters_not_randomized
    has_jonas = Has("Jonas") | characters_not_randomized
    has_setsu = Has("Setsu") | characters_not_randomized
    has_otome = Has("Otome") | characters_not_randomized
    has_shaming = Has("Sha-Ming") | characters_not_randomized
    has_kukrushka = Has("Kukrushka") | characters_not_randomized
    #Role Rules
    has_player_engineer = Has("Engineer Role")
    has_player_doctor = Has("Doctor Role")
    has_player_ga = Has("Guardian Angel Role")
    has_player_gd = Has("Guard Duty Role")
    has_player_crew = True_()
    has_player_ac_follower = Has("AC Follower Role")
    has_player_gnosia = True_()
    has_player_bug = Has("Bug Role")
    has_player_crew_aligned = has_player_engineer | has_player_doctor | has_player_ga | has_player_gd | has_player_crew
    has_npc_engineer = Has("Engineer Role")
    has_npc_doctor = Has("Doctor Role")
    has_npc_ga = Has("Guardian Angel Role")
    has_npc_gd = Has("Guard Duty Role")
    has_npc_ac_follower = Has("AC Follower Role")
    has_npc_bug = Has("Bug Role")
    #Goal-Related Rule
    min_notes = ceil((world.options.required_note_percent / 100) * len(items.get_groups()["All Notes"]))
    filled_key = HasGroupUnique("All Notes", min_notes)
    #Other Rules
    has_event_search = Has("Setsu Note 2") & CanReachRegion("Bug Tutorial")
    #Define Logic for always present regions
    entrance_to_rule = {
        "Loop 6 to Step Forward Event":
            has_setsu & has_player_crew_aligned,
        "Setup to Let's Collaborate Event":
            has_player_gnosia & has_chipie & get_min_crew_rule(7) & (Has("Chipie Note 2") | get_stat_rule("Charm", 15)),
        "Setup to Chipie & Comet Note Event":
            has_chipie & has_comet,
        "Setup to Chipie Note 5 Event":
            has_chipie & has_setsu & HasAll("Chipie Note 2", "Setsu Note 2", "Let's Collaborate"),
        "Setup to Chipie & Shigemichi Note Event":
            has_chipie & has_shigemichi & has_setsu & Has("Setsu Note 5"),
        "Setup to Comet Note 4 Event":
            has_comet & has_raqio & (has_player_ac_follower | has_npc_ac_follower),
        "Setup to Say You're Human Event":
            has_comet & has_sq & get_npc_skill_rule("Comet", "Say You're Human"),
        "Setup to Gina Note 3 Event":
            has_gina & get_min_crew_rule(6) & forbidden_role_rule("Gnosia"),
        "Setup to Don't Be Fooled Event":
            has_comet & has_gina & has_setsu & HasGroupUnique("Gina Notes", 4),
        "Setup to Gina Note 6 Event":
            (characters_randomized | get_min_crew_rule(12)) & has_gina & has_setsu & has_raqio & has_shigemichi & has_shaming & has_stella & Has("Setsu Note 2"),
        "Setup to Jonas Note 3 Event":
            has_gina & has_jonas & has_sq,
        "Setup to Jonas The Wreck":
            has_jonas & has_stella & has_player_crew_aligned & Has("Jonas Note 3"),
        "Setup to Obfuscate Event":
            has_jonas & has_remnan & has_setsu & get_npc_skill_rule("Jonas", "Obfuscate") & Has("Jonas Note 4"),
        "Setup to Kukrushka & Otome Note Event":
            has_kukrushka & has_otome,
        "Setup to Regret Event":
            has_comet & has_kukrushka & Has("Kukrushka Note 2") & get_npc_skill_rule("Kukrushka", "Regret"),
        "Setup to Shower Room - Raqio":
            has_raqio & has_sq & has_setsu,
        "Setup to Raqio Quiz - Definite Human/Enemy":
            has_raqio & has_gina & (has_npc_engineer | has_player_engineer),
        "Setup to Exaggerate Event":
            has_sq & has_setsu & has_shigemichi & get_npc_skill_rule("SQ", "Exaggerate"),
        "Setup to Let's Play":
            has_setsu & has_shigemichi & has_otome & Has("Event Seen: AWWG"),
        "Setup to Otome & Sha-Ming Note Event":
            has_shaming & has_otome & has_remnan & Has("Setsu Note 2"),
        "Setup to Small Talk Event":
            has_shaming & get_npc_skill_rule("Sha-Ming", "Small Talk"),
        "Setup to Sha-Ming's Promise":
            has_shaming & has_otome & has_player_gnosia & get_min_crew_rule(7) & Has("Sha-Ming Note 2"),
        "Setup to Sha-Ming Gnosia Ally Intro":
            has_shaming & has_setsu & has_player_gnosia & get_min_crew_rule(7) & Has("Setsu Note 2"),
        "Setup to Seek Agreement Event":
            has_sq & has_raqio & has_shigemichi & has_remnan & get_npc_skill_rule("Shigemichi", "Seek Agreement"),
        "Setup to Shower Room - Shigemichi":
            has_shigemichi & Has("Shigemichi Note 2"),
        "Setup to Shigemichi Note 4 Event":
            has_raqio & has_shigemichi & has_shaming,
        "Setup to Shigemichi Note 6 Event":
            has_shigemichi & has_stella & Has("Stella Note 3"),
        "Setup to Retaliate Event":
            has_shigemichi & has_setsu & has_sq & Has("Exaggerate") & get_npc_skill_rule("Setsu", "Retaliate"),
        "Setup to SQ Note 2 - Gnosia Intro Ver.":
            has_sq & has_remnan & has_raqio & has_player_gnosia & get_min_crew_rule(7),
        "Setup to Flowers":
            has_stella,
        "Setup to Tears Go By":
            has_stella & has_raqio & (has_player_engineer | has_npc_engineer) & get_npc_skill_rule("Stella", "Vote"),
        "Setup to Stella Note 5 Event":
            has_stella & has_jonas & has_setsu & has_remnan & has_yuriko & HasAll("Stella Note 1", "Stella Note 2", "Stella Note 3", "Stella Note 4") & get_min_crew_rule(9),
        "Setup to Chipie Note 2 - Result Event Ver.":
            has_chipie & has_player_crew_aligned,
        "Setup to Chipie Crew Result Event":
            has_chipie & has_player_crew_aligned,
        "Setup to Comet Gnosia Result Event":
            has_comet & has_player_crew_aligned,
        "Setup to Comet Note 2 Event":
            has_comet & has_player_crew_aligned,
        "Setup to Gina Gnosia Result Event":
            has_gina & has_player_crew_aligned & HasGroupUnique("Gina Notes", 4),
        "Setup to Gina Note 2 Event":
            has_gina & has_player_crew_aligned,
        "Setup to Jonas & SQ Gnosia Result Event":
            has_jonas & has_sq & has_player_crew_aligned & get_min_crew_rule(7),
        "Setup to Jonas Note 2 - Result Event Ver.":
            has_jonas & has_remnan & has_player_crew_aligned,
        "Setup to Kukrushka's Song":
            has_kukrushka & has_jonas & has_player_crew_aligned,
        "Setup to Lovely Kukrushka":
            has_kukrushka & has_gina & has_player_crew_aligned,
        "Setup to Otome Gnosia Result Event":
            has_otome & has_player_crew_aligned,
        "Setup to Otome Note 2 Event":
            has_otome & has_player_crew_aligned,
        "Setup to Raqio Gnosia Result Event":
            has_raqio & has_player_crew_aligned,
        "Setup to Raqio Note 2 Event":
            has_raqio & has_player_crew_aligned,
        "Setup to Remnan Gnosia Result Event":
            has_remnan & has_player_crew_aligned,
        "Setup to Remnan & Raqio Crew Result Event":
            has_remnan & has_raqio & has_player_crew_aligned,
        "Setup to Setsu Gnosia Result Event":
            has_setsu & ((has_player_gnosia & get_min_crew_rule(7)) | has_player_ac_follower),
        "Setup to Setsu Crew Result Event":
            has_setsu & has_player_crew_aligned & Has("Setsu Note 2"),
        "Setup to Sha-Ming Gnosia Result Event":
            has_shaming & has_player_crew_aligned,
        "Setup to Shigemichi Gnosia Result Event":
            has_shigemichi & has_player_crew_aligned,
        "Setup to Shigemichi Crew Result Event":
            has_shigemichi & has_player_crew_aligned,
        "Setup to SQ Note 2 - Result Event Ver.":
            has_sq & has_remnan & has_player_crew_aligned & get_min_crew_rule(7),
        "Setup to Yuriko Gnosia Result Event":
            has_yuriko & has_player_crew_aligned,
        "Setup to Yuriko Crew Result Event":
            has_yuriko & has_player_crew_aligned,
        "Setup to Bug Tutorial":
            has_player_bug | has_npc_bug,
        "Setup to Bug Loop":
            has_setsu,
        "Setup to A World Without Gnosia - First Time Ver.":
            get_min_crew_rule(15) & Has("Can Set Gnosia to Zero") & (has_player_crew_aligned | has_player_ac_follower),
        "Bug Tutorial to Shower Room - Comet":
            has_comet,
        "Bug Tutorial to Citizen Slime":
            (characters_randomized | has_event_search) & has_comet & has_stella & has_shigemichi & has_remnan & has_jonas & has_setsu & has_shaming & HasAll("Setsu Note 2", "Sha-Ming Note 3", "Comet Note 5"),
        "Bug Tutorial to Adventure In A Frozen World":
            has_comet & has_player_gnosia & HasAll("Comet Note 4", "Comet Note 5") & get_min_crew_rule(8),
        "Bug Tutorial to Allacosia":
            has_gina & has_stella & get_min_crew_rule(7) & has_player_crew_aligned & Has("Gina Note 3"),
        "Bug Tutorial to Jonas & Kukrushka Note Event":
            has_jonas & has_setsu & has_kukrushka & Has("Kukrushka Note 5"),
        "Bug Tutorial to The Kukrushka Problem":
            (characters_randomized | has_event_search) & has_sq & has_remnan & has_yuriko & has_jonas & has_kukrushka & Has("Yuriko Note 2"),
        "Bug Tutorial to Kukrushka The Guard":
            has_kukrushka & has_remnan & has_otome & has_setsu & has_raqio & get_min_crew_rule(9) & has_npc_gd & HasAny("Kukrushka Note 3", "SQ Note 2") & Has("Setsu Note 2") & forbidden_role_rule("Guard Duty"),
        "Bug Tutorial to Return Of The Saint":
            has_jonas & has_setsu & has_kukrushka & has_player_crew_aligned & HasAll("Jonas Note 3", "Jonas Note 5","Kukrushka Note 4"),
        "Bug Tutorial to Don't Vote Event":
            has_otome & has_raqio & (has_npc_bug | has_player_bug),
        "Bug Tutorial to Otome's Resolution":
            has_otome & has_stella & has_kukrushka & has_shigemichi & has_npc_bug,
        "Bug Tutorial to Raqio Quiz - Guardian Angel":
            has_raqio & has_npc_bug & has_npc_engineer & has_npc_ga, #Simplified logic
        "Bug Tutorial to Inescapable Past":
            has_remnan & has_sq & has_raqio & get_min_crew_rule(7) & HasAll("Remnan Note 3", "Yuriko Note 4"),
        "Bug Tutorial to Remnan Note 2 Event":
            has_remnan & has_stella & has_comet & has_raqio & (has_npc_bug | has_player_bug),
        "Bug Tutorial to Hope For The Future":
            has_remnan & HasAll("Remnan Note 4", "Remnan Note 2") & has_player_crew_aligned,
        "Bug Tutorial to Setsu Note 2 Event":
            has_setsu & (has_player_crew_aligned | has_player_ac_follower | has_player_gnosia) & get_min_crew_rule(7), #Simplified Logic
        "Bug Tutorial to Setsu Note 3 Event":
            has_setsu & has_shaming & get_min_crew_rule(7),
        "Bug Tutorial to Ace In The Hole":
            has_shaming & get_npc_skill_rule("Sha-Ming", "Grovel"),
        "Bug Tutorial to Game Sermon":
            has_shigemichi & has_jonas & has_setsu & has_remnan & (has_npc_engineer | has_npc_doctor),
        "Bug Tutorial to Fool And Be Fooled":
            has_sq & has_player_crew_aligned & get_npc_skill_rule("SQ", "Let's Collaborate"),
        "Bug Tutorial to Shigemichi In Love":
            has_shigemichi & has_stella & Has("Shigemichi Note 6"),
        "Bug Tutorial to Chaos":
            has_yuriko & has_sq & get_npc_skill_rule("Yuriko", "Block Argument"),
        "Bug Tutorial to Starship Oracle":
            has_yuriko & has_remnan & has_gina & (get_min_crew_rule(7) | forbidden_role_rule("Gnosia")),
        "Bug Tutorial to Confrontation":
            has_yuriko & has_setsu & get_min_crew_rule(7) & HasAll("Yuriko Note 2", "Event Seen: Sha-Ming Gnosia Ally Intro") & (has_player_crew_aligned | has_player_bug),
        "Bug Tutorial to The Alien Gnos":
            has_yuriko & has_setsu & Has("Yuriko Note 4") & forbidden_role_rule("Bug"),
        "Bug Tutorial to Respec & Recollection Event":
            has_yuriko & has_player_bug,
        "Bug Tutorial to A Prayer To The Stars":
            has_sq & has_npc_bug & has_player_crew_aligned,
        "Raqio Note 6 Event to The Final Problem":
            get_min_crew_rule(9) & has_player_crew_aligned & has_npc_bug & has_raqio & has_yuriko,
        "Raqio Note 6 Event to Loop After - Raqio Note 6 Event":
            has_setsu,
        "Raqio Note 6 Event to Setsu's Origins":
            get_min_crew_rule(15) & has_player_crew_aligned & HasAll("Event Seen: AWWG", "Event Completed: Allacosia"),
        "Raqio Note 6 Event to Collaboration Hint Setsu Event":
            has_setsu & has_sq,
        "Raqio Quiz - Guardian Angel to Raqio Quiz - Note 4":
            has_raqio & has_sq & has_npc_bug & has_npc_ac_follower, #Simplified Logic
        "Raqio Quiz - Guardian Angel to Raqio Quiz - Freeze All":
            has_raqio & (has_npc_bug | has_player_bug) & get_npc_skill_rule("Raqio", "Freeze All"),
        "The Final Problem to Loop After - The Final Problem":
            has_setsu,
        "The Final Problem to After The Final Problem Result Event":
            has_setsu & has_yuriko & (has_player_crew_aligned | has_player_ac_follower | has_player_gnosia) & get_min_crew_rule(7), #Simplified Logic
        "The Alien Gnos to Loop After - The Alien Gnos":
            has_setsu,
        "The Alien Gnos to Tears Of SQ":
            has_sq & has_remnan & has_player_gnosia & get_min_crew_rule(9) & HasAll("SQ Note 1", "SQ Note 2", "SQ Note 3", "SQ Note 4", "Remnan Note 4"),
        "Raqio Quiz - Note 4 to Raqio Quiz - Note 5":
            has_raqio & (has_player_doctor | has_npc_doctor) & Has("Raqio Note 3") & get_min_crew_rule(15),
        "Raqio Quiz - Note 5 to Raqio Note 6 Event":
            has_raqio & has_setsu & has_player_crew_aligned & Has("Event Completed: The Alien Gnos"),
        "Return Of The Saint to To The Hangar":
            has_setsu & has_jonas & has_kukrushka & forbidden_role_rule("Gnosia"), #Possibly too restrictive but it's fine
        "Fool And Be Fooled to Collaboration Hint Setsu Event":
            has_setsu & has_sq,
        "After The Final Problem Result Event to World Without Gnosia Hint Result Event":
            has_yuriko & has_player_crew_aligned,
        "AWWG - Unfilled Key to In The Loop Again":
            filled_key,
    }
    #Apply Rules
    for entrance_name in entrance_to_rule:
        world.set_rule(world.get_entrance(entrance_name), entrance_to_rule[entrance_name])
    #Add optional region/location rules
    if world.options.allow_gender_specific_logic:
        optional = {
            "Respec to Shower Room - Gina":
                has_gina,
            "Respec to Gina In Love":
                has_gina & has_player_crew_aligned & HasAll("Gina Romance Chain Started", "Apologized to Gina in Shower Room", "Gina Note 1", "Gina Note 2", "Gina Note 3", "Gina Note 4", "Gina Note 5", "Let's Collaborate") & get_stat_rule("Charm", 15),
            "Respec to Hope For The Future":
                has_remnan & HasAll("Remnan Note 4", "Remnan Note 2"),
            "Respec to Plastic Flower":
                has_stella & get_min_crew_rule(11) & has_player_crew_aligned & Has("Stella Note 3"),
            "Respec to Stella Protected By Player Result Event":
                has_stella & has_player_ga,
        }
        for entrance_name in optional:
            world.set_rule(world.get_entrance(entrance_name), optional[entrance_name])

def set_all_location_rules(world: GnosiaWorld) -> None:
    #Nothing complex as there's only one rule for now...
    lets_collaborate = world.get_location("Learn About Let's Collaborate")
    world.set_rule(lets_collaborate, get_min_crew_rule(8))

def set_completion_condition(world: GnosiaWorld) -> None:
    match world.options.goal:
        case Goal.option_normal_ending:
            world.set_completion_rule(Has("Event Seen: Normal Ending"))
        case _:
            raise OptionError("Unknown or Undefined Goal")