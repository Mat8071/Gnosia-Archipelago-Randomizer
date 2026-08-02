from __future__ import annotations
from typing import TYPE_CHECKING, override
from math import ceil

from Options import OptionError
from rule_builder.options import OptionFilter
from rule_builder.rules import Rule, True_, And, Or, Has, HasAny, HasAll, HasGroupUnique, CanReachRegion

from .options import RandomizeCharacterUnlocks, Goal
from .stats_data import CharacterStats, npc_starting_stats, npc_final_stats, skill_stat_requirements
from . import items

from _collections_abc import Iterable

import dataclasses

if TYPE_CHECKING:
    from .world import GnosiaWorld

@dataclasses.dataclass(init=False)
class HasCharacters(Rule["GnosiaWorld"], game="Gnosia"):

    character_names: tuple[str, ...]

    def __init__(
            self,
            *character_names: str,
            options: Iterable[OptionFilter] = (),
            filtered_resolution: bool = False,
    ) -> None:
        super().__init__(options=options, filtered_resolution=filtered_resolution)
        self.character_names = tuple(sorted(set(character_names)))

    @override
    def _instantiate(self, world: GnosiaWorld) -> Rule.Resolved:
        return (HasAll(*self.character_names) | OptionFilter(RandomizeCharacterUnlocks, False)).resolve(world)

@dataclasses.dataclass(init=False)
class HasRoles(Rule["GnosiaWorld"], game="Gnosia"):

    role_names: tuple[str, ...]

    def __init__(
        self,
        *role_names: str,
        options: Iterable[OptionFilter] = (),
        filtered_resolution: bool = False,
    ) -> None:
        super().__init__(options=options, filtered_resolution=filtered_resolution)
        self.role_names = tuple(sorted(set(role_names)))

    @override
    def _instantiate(self, world: GnosiaWorld) -> Rule.Resolved:
        return HasAll(*(f"{role} Role" for role in self.role_names)).resolve(world)

@dataclasses.dataclass(init=False)
class CharacterIsRole(Rule["GnosiaWorld"], game="Gnosia"):

    character_name: str
    role_names: tuple[str, ...]

    def __init__(
        self,
        character_name: str,
        *role_names: str,
        options: Iterable[OptionFilter] = (),
        filtered_resolution: bool = False,
    ) -> None:
        super().__init__(options=options, filtered_resolution=filtered_resolution)
        self.character_name = character_name
        self.role_names = tuple(sorted(set(role_names)))

    @override
    def _instantiate(self, world: GnosiaWorld) -> Rule.Resolved:
        if "Gnosia" in self.role_names or "Crew Member" in self.role_names:
            return True_().resolve(world)
        return HasAny(*(f"{role} Role" for role in self.role_names)).resolve(world)

@dataclasses.dataclass()
class CharacterIsNotRole(Rule["GnosiaWorld"], game="Gnosia"):

    character_name: str
    role_names: tuple[str, ...]

    def __init__(
        self,
        character_name: str,
        *role_names: str,
        options: Iterable[OptionFilter] = (),
        filtered_resolution: bool = False,
    ) -> None:
        super().__init__(options=options, filtered_resolution=filtered_resolution)
        self.character_name = character_name
        self.role_names = tuple(sorted(set(role_names)))

    @override
    def _instantiate(self, world: GnosiaWorld) -> Rule.Resolved:
        roles = ALL_ROLES.copy()
        roles.difference_update(self.role_names)
        return CharacterIsRole(self.character_name, *roles).resolve(world)

@dataclasses.dataclass()
class CharacterHasStats(Rule["GnosiaWorld"], game="Gnosia"):

    character_name: str
    required_stats: CharacterStats

    @override
    def _instantiate(self, world: GnosiaWorld) -> Rule.Resolved:
        if self.character_name == "Player":
            return True_().resolve(world)
        thing_to_check = f"{self.character_name} Notes"
        total_character_notes = len(items.get_groups().get(thing_to_check, []))
        number_of_notes_required = 0
        current_stats = dataclasses.replace(npc_starting_stats[self.character_name])
        if self.check_stats(current_stats, self.required_stats):
            return True_().resolve(world)
        else:
            for _ in range(total_character_notes):
                number_of_notes_required += 1
                self.raise_stats(npc_starting_stats[self.character_name], current_stats, npc_final_stats[self.character_name], total_character_notes)
                if self.check_stats(current_stats, self.required_stats):
                    break
        return HasGroupUnique(thing_to_check, number_of_notes_required).resolve(world)

    @staticmethod
    def check_stats(arg1: CharacterStats, arg2: CharacterStats) -> bool:
        for field in dataclasses.fields(CharacterStats):
            if getattr(arg1, field.name) < getattr(arg2, field.name):
                return False
        return True

    @staticmethod
    def raise_stats(starting_stats: CharacterStats, current_stats: CharacterStats, max_stats: CharacterStats, total_notes: int):
        for field in dataclasses.fields(CharacterStats):
            starting = getattr(starting_stats, field.name)
            current = getattr(current_stats, field.name)
            maximum = getattr(max_stats, field.name)
            increase = ((maximum - starting) / total_notes) / 2
            setattr(current_stats, field.name, current + increase)

@dataclasses.dataclass()
class CharacterHasSkill(Rule["GnosiaWorld"], game="Gnosia"):

    character_name: str
    skill_name: str

    @override
    def _instantiate(self, world: GnosiaWorld) -> Rule.Resolved:
        has_skill_rule = True_()
        if self.character_name == "Player":
            has_skill_rule &= Has(self.skill_name)
        return And(
            has_skill_rule,
            CharacterHasStats(self.character_name, skill_stat_requirements[self.skill_name]),
        ).resolve(world)

@dataclasses.dataclass()
class HasMinCharacters(Rule["GnosiaWorld"], game="Gnosia"):

    minimum: int

    @override
    def _instantiate(self, world: GnosiaWorld) -> Rule.Resolved:
        if world.options.randomize_character_unlocks:
            return HasGroupUnique("Characters", self.minimum - 1).resolve(world)
        return Has("Progressive Crew Max", self.minimum - 5).resolve(world)

CREW_ALIGNED_ROLES: set = {
    "Engineer",
    "Doctor",
    "Guardian Angel",
    "Guard Duty",
    "Crew Member",
}

HUMAN_ROLES: set = CREW_ALIGNED_ROLES | {
    "AC Follower",
}

ALL_ROLES: set = HUMAN_ROLES | {
    "Gnosia",
    "Bug",
}

#Common Rules Definitions
#Option Filters
characters_randomized = OptionFilter(RandomizeCharacterUnlocks, True)
characters_not_randomized = OptionFilter(RandomizeCharacterUnlocks, False)
#Other Rules
has_event_search = Has("Setsu Note 2") & CanReachRegion("Bug Tutorial")
has_easy_lie_detect = HasAny("Engineer Role", "Doctor Role", "Say You're Human")

def set_all_rules(world: GnosiaWorld) -> None:
    set_all_entrance_rules(world)
    set_all_location_rules(world)
    set_completion_condition(world)

def set_all_entrance_rules(world: GnosiaWorld) -> None:
    #Goal-Related Rules
    min_notes = ceil((world.options.required_note_percent / 100) * len(items.get_groups()["All Notes"]))
    filled_key = HasGroupUnique("All Notes", min_notes)
    #Define Logic for always present regions
    entrance_to_rule = {
        "Loop 6 to Step Forward Event":
            And(
                HasCharacters("Setsu"),
                CharacterIsRole("Player", *CREW_ALIGNED_ROLES),
            ),
        "Setup to Let's Collaborate Event":
            And(
                HasCharacters("Chipie"),
                CharacterIsRole("Player", "Gnosia"),
                HasMinCharacters(7),
                Has("Chipie Note 2") | CharacterHasStats("Player", CharacterStats(charm=15)),
            ),
        "Setup to Chipie & Comet Note Event":
            HasCharacters("Chipie", "Comet"),
        "Setup to Chipie Note 5 Event":
            And(
                HasCharacters("Chipie", "Setsu"),
                HasAll("Chipie Note 2", "Setsu Note 2", "Let's Collaborate"),
            ),
        "Setup to Chipie & Shigemichi Note Event":
            And(
                HasCharacters("Chipie", "Shigemichi", "Setsu"),
                Has("Setsu Note 5"),
            ),
        "Setup to Comet Note 4 Event":
            And(
                HasCharacters("Comet", "Raqio"),
                HasRoles("AC Follower"),
                has_easy_lie_detect,
            ),
        "Setup to Say You're Human Event":
            And(
                HasCharacters("Comet", "SQ"),
                CharacterHasSkill("Comet", "Say You're Human"),
            ),
        "Setup to Gina Note 3 Event":
            And(
                HasCharacters("Gina"),
                HasMinCharacters(6),
                CharacterIsNotRole("Player", "Gnosia"),
            ),
        "Setup to Don't Be Fooled Event":
            And(
                HasCharacters("Comet", "Gina", "Setsu"),
                HasGroupUnique("Gina Notes", 4),
                has_easy_lie_detect,
            ),
        "Setup to Gina Note 6 Event":
            And(
                characters_randomized | HasMinCharacters(12),
                HasCharacters(
                    "Gina", "Setsu", "Raqio", "Shigemichi", "Sha-Ming", "Stella"
                ),
                Has("Setsu Note 2"),
            ),
        "Setup to Jonas Note 3 Event":
            HasCharacters("Gina", "Jonas", "SQ"),
        "Setup to Jonas The Wreck":
            And(
                HasCharacters("Jonas", "Stella"),
                CharacterIsRole("Player", *CREW_ALIGNED_ROLES),
                Has("Jonas Note 3"),
            ),
        "Setup to Obfuscate Event":
            And(
                HasCharacters("Jonas", "Remnan", "Setsu"),
                CharacterHasSkill("Jonas", "Obfuscate"),
                Has("Jonas Note 4"),
            ),
        "Setup to Kukrushka & Otome Note Event":
            HasCharacters("Kukrushka", "Otome"),
        "Setup to Regret Event":
            And(
                HasCharacters("Comet", "Kukrushka"),
                CharacterHasSkill("Kukrushka", "Regret"),
                Has("Kukrushka Note 2"),
            ),
        "Setup to Shower Room - Raqio":
            HasCharacters("Raqio", "SQ", "Setsu"),
        "Setup to Raqio Quiz - Definite Human/Enemy":
            And(
                HasCharacters("Raqio", "Gina"),
                HasRoles("Engineer"),
            ),
        "Setup to Exaggerate Event":
            And(
                HasCharacters("SQ", "Setsu", "Shigemichi"),
                CharacterHasSkill("SQ", "Exaggerate"),
            ),
        "Setup to Let's Play":
            And(
                HasCharacters("Setsu", "Shigemichi", "Otome"),
                Has("Event Seen: AWWG"),
            ),
        "Setup to Otome & Sha-Ming Note Event":
            And(
                HasCharacters("Sha-Ming", "Otome", "Remnan"),
                Has("Setsu Note 2"),
            ),
        "Setup to Small Talk Event":
            And(
                HasCharacters("Sha-Ming"),
                CharacterHasSkill("Sha-Ming", "Small Talk"),
            ),
        "Setup to Sha-Ming's Promise":
            And(
                HasCharacters("Sha-Ming", "Otome"),
                CharacterIsRole("Player", "Gnosia"),
                HasMinCharacters(7),
                Has("Sha-Ming Note 2"),
            ),
        "Setup to Sha-Ming Gnosia Ally Intro":
            And(
                HasCharacters("Sha-Ming", "Setsu"),
                CharacterIsRole("Player", "Gnosia"),
                HasMinCharacters(7),
                Has("Setsu Note 2"),
            ),
        "Setup to Seek Agreement Event":
            And(
                HasCharacters("SQ", "Raqio", "Shigemichi", "Remnan"),
                CharacterHasSkill("Shigemichi", "Seek Agreement"),
            ),
        "Setup to Shower Room - Shigemichi":
            And(
                HasCharacters("Shigemichi"),
                Has("Shigemichi Note 2"),
            ),
        "Setup to Shigemichi Note 4 Event":
            HasCharacters("Raqio", "Shigemichi", "Sha-Ming"),
        "Setup to Shigemichi Note 6 Event":
            And(
                HasCharacters("Shigemichi", "Stella"),
                Has("Stella Note 3"),
            ),
        "Setup to Retaliate Event":
            And(
                HasCharacters("Shigemichi", "Setsu", "SQ"),
                CharacterHasSkill("Setsu", "Retaliate"),
                Has("Exaggerate"),
            ),
        "Setup to SQ Note 2 - Gnosia Intro Ver.":
            And(
                HasCharacters("SQ", "Remnan", "Raqio"),
                CharacterIsRole("Player", "Gnosia"),
                HasMinCharacters(7),
            ),
        "Setup to Flowers":
            HasCharacters("Stella"),
        "Setup to Tears Go By":
            And(
                HasCharacters("Stella", "Raqio"),
                HasRoles("Engineer"),
                CharacterHasSkill("Stella", "Vote"),
            ),
        "Setup to Stella Note 5 Event":
            And(
                HasCharacters("Stella", "Jonas", "Setsu", "Remnan", "Yuriko"),
                HasAll("Stella Note 1", "Stella Note 2", "Stella Note 3", "Stella Note 4"),
                HasMinCharacters(9),
            ),
        "Setup to Chipie Note 2 - Result Event Ver.":
            And(
                HasCharacters("Chipie"),
                CharacterIsRole("Player", *CREW_ALIGNED_ROLES),
            ),
        "Setup to Chipie Crew Result Event":
            And(
                HasCharacters("Chipie"),
                CharacterIsRole("Player", *CREW_ALIGNED_ROLES),
            ),
        "Setup to Comet Gnosia Result Event":
            And(
                HasCharacters("Comet"),
                CharacterIsRole("Player", *CREW_ALIGNED_ROLES),
            ),
        "Setup to Comet Note 2 Event":
            And(
                HasCharacters("Comet"),
                CharacterIsRole("Player", *CREW_ALIGNED_ROLES),
            ),
        "Setup to Gina Gnosia Result Event":
            And(
                HasCharacters("Gina"),
                CharacterIsRole("Player", *CREW_ALIGNED_ROLES),
                HasGroupUnique("Gina Notes", 4),
            ),
        "Setup to Gina Note 2 Event":
            And(
                HasCharacters("Gina"),
                CharacterIsRole("Player", *CREW_ALIGNED_ROLES),
            ),
        "Setup to Jonas & SQ Gnosia Result Event":
            And(
                HasCharacters("Jonas", "SQ"),
                CharacterIsRole("Player", *CREW_ALIGNED_ROLES),
                HasMinCharacters(7),
            ),
        "Setup to Jonas Note 2 - Result Event Ver.":
            And(
                HasCharacters("Jonas", "Remnan"),
                CharacterIsRole("Player", *CREW_ALIGNED_ROLES),
            ),
        "Setup to Kukrushka's Song":
            And(
                HasCharacters("Kukrushka", "Jonas"),
                CharacterIsRole("Player", *CREW_ALIGNED_ROLES),
            ),
        "Setup to Lovely Kukrushka":
            And(
                HasCharacters("Kukrushka", "Gina"),
                CharacterIsRole("Player", *CREW_ALIGNED_ROLES),
            ),
        "Setup to Otome Gnosia Result Event":
            And(
                HasCharacters("Otome"),
                CharacterIsRole("Player", *CREW_ALIGNED_ROLES),
            ),
        "Setup to Otome Note 2 Event":
            And(
                HasCharacters("Otome"),
                CharacterIsRole("Player", *CREW_ALIGNED_ROLES),
            ),
        "Setup to Raqio Gnosia Result Event":
            And(
                HasCharacters("Raqio"),
                CharacterIsRole("Player", *CREW_ALIGNED_ROLES),
            ),
        "Setup to Raqio Note 2 Event":
            And(
                HasCharacters("Raqio"),
                CharacterIsRole("Player", *CREW_ALIGNED_ROLES),
            ),
        "Setup to Remnan Gnosia Result Event":
            And(
                HasCharacters("Remnan"),
                CharacterIsRole("Player", *CREW_ALIGNED_ROLES),
            ),
        "Setup to Remnan & Raqio Crew Result Event":
            And(
                HasCharacters("Remnan", "Raqio"),
                CharacterIsRole("Player", *CREW_ALIGNED_ROLES),
            ),
        "Setup to Setsu Gnosia Result Event":
            And(
                HasCharacters("Setsu"),
                Or(
                    CharacterIsRole("Player", "Gnosia") & HasMinCharacters(7),
                    CharacterIsRole("Player", "AC Follower"),
                ),
            ),
        "Setup to Setsu Crew Result Event":
            And(
                HasCharacters("Setsu"),
                CharacterIsRole("Player", *CREW_ALIGNED_ROLES),
                Has("Setsu Note 2"),
            ),
        "Setup to Sha-Ming Gnosia Result Event":
            And(
                HasCharacters("Sha-Ming"),
                CharacterIsRole("Player", *CREW_ALIGNED_ROLES),
            ),
        "Setup to Shigemichi Gnosia Result Event":
            And(
                HasCharacters("Shigemichi"),
                CharacterIsRole("Player", *CREW_ALIGNED_ROLES),
            ),
        "Setup to Shigemichi Crew Result Event":
            And(
                HasCharacters("Shigemichi"),
                CharacterIsRole("Player", *CREW_ALIGNED_ROLES),
            ),
        "Setup to SQ Note 2 - Result Event Ver.":
            And(
                HasCharacters("SQ", "Remnan"),
                CharacterIsRole("Player", *CREW_ALIGNED_ROLES),
                HasMinCharacters(7),
            ),
        "Setup to Yuriko Gnosia Result Event":
            And(
                HasCharacters("Yuriko"),
                CharacterIsRole("Player", *CREW_ALIGNED_ROLES),
            ),
        "Setup to Yuriko Crew Result Event":
            And(
                HasCharacters("Yuriko"),
                CharacterIsRole("Player", *CREW_ALIGNED_ROLES),
            ),
        "Setup to Bug Tutorial":
            HasRoles("Bug"),
        "Setup to Bug Loop":
            HasCharacters("Setsu"),
        "Setup to A World Without Gnosia - First Time Ver.":
            And(
                HasMinCharacters(15),
                Has("Can Set Gnosia to Zero"),
                CharacterIsRole("Player", *HUMAN_ROLES),
            ),
        "Bug Tutorial to Shower Room - Comet":
            HasCharacters("Comet"),
        "Bug Tutorial to Citizen Slime":
            And(
                characters_randomized | has_event_search,
                HasCharacters("Comet", "Stella", "Shigemichi", "Remnan", "Jonas", "Setsu", "Sha-Ming"),
                HasAll("Setsu Note 2", "Sha-Ming Note 3", "Comet Note 5"),
            ),
        "Bug Tutorial to Adventure In A Frozen World":
            And(
                HasCharacters("Comet"),
                CharacterIsRole("Player", "Gnosia"),
                HasMinCharacters(8),
                HasAll("Comet Note 4", "Comet Note 5"),
            ),
        "Bug Tutorial to Allacosia":
            And(
                HasCharacters("Gina", "Stella"),
                CharacterIsRole("Player", *CREW_ALIGNED_ROLES),
                HasMinCharacters(7),
                Has("Gina Note 3"),
            ),
        "Bug Tutorial to Jonas & Kukrushka Note Event":
            And(
                HasCharacters("Jonas", "Setsu", "Kukrushka"),
                Has("Kukrushka Note 5"),
            ),
        "Bug Tutorial to The Kukrushka Problem":
            And(
                characters_randomized | has_event_search,
                HasCharacters("SQ", "Remnan", "Yuriko", "Jonas", "Kukrushka"),
                Has("Yuriko Note 2"),
            ),
        "Bug Tutorial to Kukrushka The Guard":
            And(
                HasCharacters("Kukrushka", "Remnan", "Otome", "Setsu", "Raqio"),
                CharacterIsRole("Kukrushka", "Guard Duty"),
                CharacterIsRole("Remnan", "Guard Duty"),
                CharacterIsNotRole("Player", "Guard Duty"),
                HasMinCharacters(9),
                HasAny("Kukrushka Note 3", "SQ Note 2"),
                Has("Setsu Note 2"),
            ),
        "Bug Tutorial to Return Of The Saint":
            And(
                HasCharacters("Jonas", "Setsu", "Kukrushka"),
                CharacterIsRole("Player", *CREW_ALIGNED_ROLES),
                HasAll("Jonas Note 3", "Jonas Note 5","Kukrushka Note 4"),
            ),
        "Bug Tutorial to Don't Vote Event":
            And(
                HasCharacters("Otome", "Raqio"),
                HasRoles("Bug"),
            ),
        "Bug Tutorial to Otome's Resolution":
            And(
                HasCharacters("Otome", "Stella", "Kukrushka", "Shigemichi"),
                CharacterIsRole("Otome", "Bug"),
            ),
        "Bug Tutorial to Raqio Quiz - Guardian Angel":
            And(
                HasCharacters("Raqio"),
                HasRoles("Bug", "Engineer", "Guardian Angel"), #Simplified logic
            ),
        "Bug Tutorial to Inescapable Past":
            And(
                HasCharacters("Remnan", "SQ", "Raqio"),
                HasMinCharacters(7),
                HasAll("Remnan Note 3", "Yuriko Note 4"),
            ),
        "Bug Tutorial to Remnan Note 2 Event":
            And(
                HasCharacters("Remnan", "Stella", "Comet", "Raqio"),
                HasRoles("Bug"),
            ),
        "Bug Tutorial to Hope For The Future":
            And(
                HasCharacters("Remnan"),
                CharacterIsRole("Player", *CREW_ALIGNED_ROLES),
                HasAll("Remnan Note 4", "Remnan Note 2"),
            ),
        "Bug Tutorial to Setsu Note 2 Event":
            And(
                HasCharacters("Setsu"),
                Or(
                    CharacterIsRole("Player", *HUMAN_ROLES),
                    And(
                        CharacterIsRole("Player", "Gnosia"),
                        HasMinCharacters(7),
                    ),
                ),
            ),
        "Bug Tutorial to Setsu Note 3 Event":
            And(
                HasCharacters("Setsu", "Sha-Ming"),
                HasMinCharacters(7),
            ),
        "Bug Tutorial to Ace In The Hole":
            And(
                HasCharacters("Sha-Ming"),
                CharacterHasSkill("Sha-Ming", "Grovel"),
            ),
        "Bug Tutorial to Game Sermon":
            And(
                HasCharacters("Shigemichi", "Jonas", "Setsu", "Remnan"),
                CharacterHasSkill("Player", "Step Forward"),
                Or(
                    And(
                        CharacterIsRole("Shigemichi", "Engineer", "Doctor"),
                        CharacterIsRole("Jonas", "Gnosia"),
                    ),
                    And(
                        CharacterIsRole("Shigemichi", "Gnosia"),
                        CharacterIsRole("Jonas", "Engineer", "Doctor"),
                    ),
                ),
            ),
        "Bug Tutorial to Fool And Be Fooled":
            And(
                HasCharacters("SQ"),
                CharacterIsRole("Player", *CREW_ALIGNED_ROLES),
                CharacterHasSkill("SQ", "Let's Collaborate"),
            ),
        "Bug Tutorial to Shigemichi In Love":
            And(
                HasCharacters("Shigemichi", "Stella"),
                Has("Shigemichi Note 6"),
            ),
        "Bug Tutorial to Chaos":
            And(
                HasCharacters("Yuriko", "SQ"),
                CharacterHasSkill("Yuriko", "Block Argument"),
            ),
        "Bug Tutorial to Starship Oracle":
            And(
                HasCharacters("Yuriko", "Remnan", "Gina"),
                CharacterIsNotRole("Player", "Gnosia"),
                HasMinCharacters(7),
            ),
        "Bug Tutorial to Confrontation":
            And(
                HasCharacters("Yuriko", "Setsu"),
                CharacterIsRole("Player", *CREW_ALIGNED_ROLES, "Bug"),
                HasMinCharacters(7),
                HasAll("Yuriko Note 2", "Event Seen: Sha-Ming Gnosia Ally Intro"),
            ),
        "Bug Tutorial to The Alien Gnos":
            And(
                HasCharacters("Yuriko", "Setsu"),
                CharacterIsNotRole("Player", "Bug"),
                Has("Yuriko Note 4"),
            ),
        "Bug Tutorial to Respec & Recollection Event":
            And(
                HasCharacters("Yuriko"),
                CharacterIsRole("Player", "Bug"),
            ),
        "Bug Tutorial to A Prayer To The Stars":
            And(
                HasCharacters("SQ"),
                CharacterIsRole("SQ", "Bug"),
                CharacterIsRole("Player", *CREW_ALIGNED_ROLES),
            ),
        "Raqio Note 6 Event to The Final Problem":
            And(
                HasCharacters("Raqio", "Yuriko"),
                CharacterIsRole("Raqio", "Bug"),
                CharacterIsRole("Player", *CREW_ALIGNED_ROLES),
                HasMinCharacters(9),
            ),
        "Raqio Note 6 Event to Loop After - Raqio Note 6 Event":
            HasCharacters("Setsu"),
        "Raqio Note 6 Event to Setsu's Origins":
            And(
                HasMinCharacters(15),
                CharacterIsRole("Player", *CREW_ALIGNED_ROLES),
                HasAll("Event Seen: AWWG", "Event Completed: Allacosia"),
            ),
        "Raqio Note 6 Event to Collaboration Hint Setsu Event":
            HasCharacters("Setsu", "SQ"),
        "Raqio Quiz - Guardian Angel to Raqio Quiz - Note 4":
            And(
                HasCharacters("Raqio", "SQ"),
                HasRoles("Bug", "AC Follower"), #Simplified Logic
            ),
        "Raqio Quiz - Guardian Angel to Raqio Quiz - Freeze All":
            And(
                HasCharacters("Raqio"),
                HasRoles("Bug"),
                CharacterHasSkill("Raqio", "Freeze All"),
            ),
        "The Final Problem to Loop After - The Final Problem":
            HasCharacters("Setsu"),
        "The Final Problem to After The Final Problem Result Event":
            And(
                HasCharacters("Setsu", "Yuriko"),
                Or(
                    CharacterIsRole("Player", *HUMAN_ROLES),
                    And(
                        CharacterIsRole("Player", "Gnosia"),
                        HasMinCharacters(7),
                    ),
                ),
            ),
        "The Alien Gnos to Loop After - The Alien Gnos":
            HasCharacters("Setsu"),
        "The Alien Gnos to Tears Of SQ":
            And(
                HasCharacters("SQ", "Remnan"),
                CharacterIsRole("Player", "Gnosia"),
                HasMinCharacters(9),
                HasAll("SQ Note 1", "SQ Note 2", "SQ Note 3", "SQ Note 4", "Remnan Note 4"),
            ),
        "Raqio Quiz - Note 4 to Raqio Quiz - Note 5":
            And(
                HasCharacters("Raqio"),
                HasRoles("Doctor"),
                HasMinCharacters(15),
                Has("Raqio Note 3"),
            ),
        "Raqio Quiz - Note 5 to Raqio Note 6 Event":
            And(
                HasCharacters("Raqio", "Setsu"),
                CharacterIsRole("Player", *CREW_ALIGNED_ROLES),
                Has("Event Completed: The Alien Gnos"),
            ),
        "Return Of The Saint to To The Hangar":
            And(
                HasCharacters("Setsu", "Jonas", "Kukrushka"),
                CharacterIsNotRole("Player", "Gnosia"),
            ),
        "Fool And Be Fooled to Collaboration Hint Setsu Event":
            HasCharacters("Setsu", "SQ"),
        "After The Final Problem Result Event to World Without Gnosia Hint Result Event":
            And(
                HasCharacters("Yuriko"),
                CharacterIsRole("Player", *CREW_ALIGNED_ROLES),
            ),
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
                HasCharacters("Gina"),
            "Respec to Gina In Love":
                And(
                    HasCharacters("Gina"),
                    CharacterIsRole("Player", *CREW_ALIGNED_ROLES),
                    CharacterHasSkill("Player", "Let's Collaborate"),
                    HasAll(
                        "Gina Romance Chain Started", "Apologized to Gina in Shower Room",
                        "Gina Note 1", "Gina Note 2", "Gina Note 3", "Gina Note 4", "Gina Note 5"),
                ),
            "Respec to Hope For The Future":
                And(
                    HasCharacters("Remnan"),
                    HasAll("Remnan Note 4", "Remnan Note 2"),
                ),
            "Respec to Plastic Flower":
                And(
                    HasCharacters("Stella"),
                    CharacterIsRole("Player", *CREW_ALIGNED_ROLES),
                    HasMinCharacters(11),
                    Has("Stella Note 3"),
                ),
            "Respec to Stella Protected By Player Result Event":
                And(
                    HasCharacters("Stella"),
                    CharacterIsRole("Player", "Guardian Angel"),
                ),
        }
        for entrance_name in optional:
            world.set_rule(world.get_entrance(entrance_name), optional[entrance_name])

def set_all_location_rules(world: GnosiaWorld) -> None:
    location_to_rule = {
        "Learn About Let's Collaborate":
            HasMinCharacters(8), #Requires two gnosia to be alive on Night 2
        "Learn About Jonas 7":
            HasMinCharacters(8), #Requires getting to Night 3 with Jonas & Setsu Alive
        "Learn About Kukrushka 6":
            HasMinCharacters(8), #Same as Jonas 7
    }
    for location_name in location_to_rule:
        world.set_rule(world.get_location(location_name), location_to_rule[location_name])

def set_completion_condition(world: GnosiaWorld) -> None:
    match world.options.goal:
        case Goal.option_normal_ending:
            world.set_completion_rule(Has("Event Seen: Normal Ending"))
        case _:
            raise OptionError("Unknown or Undefined Goal")