from __future__ import annotations
from typing import TYPE_CHECKING, override
from math import ceil

from dataclasses import dataclass, replace, fields

from Options import OptionError
from rule_builder.options import OptionFilter
from rule_builder.rules import Rule, True_, And, Or, Has, HasAny, HasAll, HasGroupUnique, CanReachLocation

from .options import RandomizeCharacterUnlocks, Goal, RandomizeNotes, TutorialHandling
from .stats_data import CharacterStats, npc_starting_stats, npc_final_stats, skill_stat_requirements
from . import items, locations

from collections.abc import Iterable

if TYPE_CHECKING:
    from .world import GnosiaWorld

is_glitch_logic = Has(items.GLITCHES_ITEM_NAME)

@dataclass(init=False)
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

@dataclass(init=False)
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

@dataclass(init=False)
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

@dataclass(init=False)
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

@dataclass()
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
        current_stats = replace(npc_starting_stats[self.character_name])
        if self.check_stats(current_stats, self.required_stats):
            return True_().resolve(world)
        else:
            for _ in range(total_character_notes):
                number_of_notes_required += 1
                self.raise_stats(npc_starting_stats[self.character_name], current_stats, npc_final_stats[self.character_name], total_character_notes)
                if self.check_stats(current_stats, self.required_stats):
                    break
        return Or(
            HasGroupUnique(thing_to_check, number_of_notes_required),
            is_glitch_logic, #You can grind loops to get npc stats higher
        ).resolve(world)

    @staticmethod
    def check_stats(arg1: CharacterStats, arg2: CharacterStats) -> bool:
        for field in fields(CharacterStats):
            if getattr(arg1, field.name) < getattr(arg2, field.name):
                return False
        return True

    @staticmethod
    def raise_stats(starting_stats: CharacterStats, current_stats: CharacterStats, max_stats: CharacterStats, total_notes: int):
        for field in fields(CharacterStats):
            starting = getattr(starting_stats, field.name)
            current = getattr(current_stats, field.name)
            maximum = getattr(max_stats, field.name)
            increase = ((maximum - starting) / total_notes) / 2
            setattr(current_stats, field.name, current + increase)

@dataclass()
class CharacterHasSkill(Rule["GnosiaWorld"], game="Gnosia"):

    character_name: str
    skill_name: str

    @override
    def _instantiate(self, world: GnosiaWorld) -> Rule.Resolved:
        has_skill_rule = True_()
        if self.character_name == "Player":
            has_skill_rule &= Has(self.skill_name)
        #Exception for Sha-Ming Grovel with vanilla note placement (Only 3 notes are available)
        if not world.options.randomize_notes and self.character_name == "Sha-Ming" and self.skill_name == "Grovel":
            return HasGroupUnique("Sha-Ming Notes", 3).resolve(world)
        return And(
            has_skill_rule,
            CharacterHasStats(self.character_name, skill_stat_requirements[self.skill_name]),
        ).resolve(world)

@dataclass()
class HasMinCharacters(Rule["GnosiaWorld"], game="Gnosia"):

    minimum: int

    @override
    def _instantiate(self, world: GnosiaWorld) -> Rule.Resolved:
        starting_crew_count = world.options.starting_crew_count
        if world.options.randomize_character_unlocks:
            return HasGroupUnique("Characters", self.minimum - 1).resolve(world)
        return Has("Progressive Crew Max", self.minimum - starting_crew_count).resolve(world)

@dataclass()
class HasMinGnosia(Rule["GnosiaWorld"], game="Gnosia"):

    minimum: int

    @override
    def _instantiate(self, world: GnosiaWorld) -> Rule.Resolved:
        return HasMinCharacters(self.minimum * 2 + 3).resolve(world)

@dataclass()
class CanBeOnSameTeam(Rule["GnosiaWorld"], game="Gnosia"):

    character_1: str
    character_2: str

    @override
    def _instantiate(self, world: GnosiaWorld) -> Rule.Resolved:
        return Or(
                    And(
                        CharacterIsRole(self.character_1, *CREW_ALIGNED_ROLES),
                        CharacterIsRole(self.character_2, *CREW_ALIGNED_ROLES),
                    ), #Win as crew
                    And(
                        CharacterIsRole(self.character_1, "Gnosia"),
                        CharacterIsRole(self.character_2, "Gnosia"),
                        HasMinGnosia(2),
                    ), #Win as gnosia
                    And(
                        CharacterIsRole(self.character_1, "AC Follower"),
                        CharacterIsRole(self.character_2, "Gnosia"),
                    ), #Character 1 is AC & 2 is Gnosia
                    And(
                        CharacterIsRole(self.character_1, "Gnosia"),
                        CharacterIsRole(self.character_2, "AC Follower"),
                    ), #Character 1 is Gnosia & 2 is AC
                ).resolve(world)

@dataclass()
class CanBeOnOppositeTeams(Rule["GnosiaWorld"], game="Gnosia"):

    character_1: str
    character_2: str

    @override
    def _instantiate(self, world: GnosiaWorld) -> Rule.Resolved:
        return Or(
            And(
                CharacterIsRole(self.character_1, *CREW_ALIGNED_ROLES),
                CharacterIsNotRole(self.character_2, *CREW_ALIGNED_ROLES),
            ),
            And(
                CharacterIsNotRole(self.character_1, *CREW_ALIGNED_ROLES),
                CharacterIsRole(self.character_2, *CREW_ALIGNED_ROLES),
            ),
            And(
                CharacterIsRole(self.character_1, "Gnosia", "AC Follower"),
                CharacterIsNotRole(self.character_2, "Gnosia", "AC Follower"),
            ),
            And(
                CharacterIsNotRole(self.character_1, "Gnosia", "AC Follower"),
                CharacterIsRole(self.character_2, "Gnosia", "AC Follower"),
            ),
            And(
                CharacterIsRole(self.character_1, "Bug"),
                CharacterIsNotRole(self.character_2, "Bug"),
            ),
            And(
                CharacterIsNotRole(self.character_1, "Bug"),
                CharacterIsRole(self.character_2, "Bug"),
            ),
        ).resolve(world)

@dataclass()
class OtherThanCharacterIsRole(Rule["GnosiaWorld"], game="Gnosia"):

    other_than: str
    role: str

    @override
    def _instantiate(self, world: GnosiaWorld) -> Rule.Resolved:
        characters = items.get_groups()["Characters"]
        characters.add("Player")
        characters.remove(self.other_than)
        return Or(
            *(CharacterIsRole(character, self.role) for character in characters)
        ).resolve(world)

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
                CharacterIsRole("Setsu", *CREW_ALIGNED_ROLES),
            ),
        "Setup to Let's Collaborate Event":
            And(
                HasCharacters("Chipie"),
                CharacterIsRole("Player", "Gnosia"),
                CharacterIsRole("Chipie", "Gnosia"),
                HasMinGnosia(2),
            ),
        "Setup to Chipie & Comet Note Event":
            And(
                HasCharacters("Chipie", "Comet"),
                CharacterIsNotRole("Chipie", "Guard Duty"),
                CharacterIsNotRole("Comet", "Guard Duty"),
            ),
        "Setup to Chipie Note 5 Event":
            And(
                HasCharacters("Chipie", "Setsu"),
                HasAll("Chipie Note 2", "Setsu Note 2", "Let's Collaborate"),
                Or(
                    CharacterIsNotRole("Player", "Gnosia", "AC Follower"),
                    CharacterIsNotRole("Chipie", "Gnosia", "AC Follower"),
                ),
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
                CharacterIsRole("Comet", *CREW_ALIGNED_ROLES),
            ),
        "Setup to Say You're Human Event":
            And(
                HasCharacters("Comet", "SQ"),
                CharacterHasSkill("Comet", "Say You're Human"),
                CharacterIsNotRole("Comet", "Gnosia", "AC Follower"),
            ),
        "Setup to Gina Note 3 Event":
            And(
                HasCharacters("Gina"),
                CharacterIsRole("Gina", "Gnosia"),
                CharacterIsNotRole("Player", "Gnosia"),
                HasMinGnosia(2),
            ),
        "Setup to Don't Be Fooled Event":
            And(
                HasCharacters("Comet", "Gina", "Setsu"),
                CharacterIsRole("Gina", *CREW_ALIGNED_ROLES),
                HasGroupUnique("Gina Notes", 4),
            ),
        "Setup to Gina Note 6 Event":
            And(
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
                Or(
                    And(
                        CharacterIsRole("Jonas", "Engineer", "Doctor", "Guardian Angel", "Crew Member"),
                        CharacterIsRole("Stella", "Gnosia"),
                    ),
                    And(
                        CharacterIsRole("Stella", "Engineer", "Doctor", "Guardian Angel", "Crew Member"),
                        CharacterIsRole("Jonas", "Gnosia"),
                    ),
                ),
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
                CharacterIsRole("Comet", *CREW_ALIGNED_ROLES),
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
            HasCharacters("Setsu", "Shigemichi", "Otome"),
        "Setup to Otome & Sha-Ming Note Event":
            And(
                HasCharacters("Sha-Ming", "Otome", "Remnan"),
                Has("Setsu Note 2"),
            ),
        "Setup to Small Talk Event":
            And(
                HasCharacters("Sha-Ming"),
                CharacterIsRole("Sha-Ming", *CREW_ALIGNED_ROLES),
                CharacterHasSkill("Sha-Ming", "Small Talk"),
            ),
        "Setup to Sha-Ming's Promise":
            And(
                HasCharacters("Sha-Ming", "Otome"),
                CharacterIsRole("Player", "Gnosia"),
                CharacterIsRole("Sha-Ming", "Gnosia"),
                CharacterIsRole("Otome", *HUMAN_ROLES),
                HasMinGnosia(2),
                Has("Sha-Ming Note 2"),
            ),
        "Setup to Sha-Ming Gnosia Ally Intro":
            And(
                HasCharacters("Sha-Ming", "Setsu"),
                CharacterIsRole("Player", "Gnosia"),
                CharacterIsRole("Sha-Ming", "Gnosia"),
                HasMinGnosia(2),
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
            HasCharacters("Raqio", "Shigemichi", "Sha-Ming"), #Always requires loop 30+
        "Setup to Shigemichi Note 6 Event":
            And(
                HasCharacters("Shigemichi", "Stella"),
                CharacterIsRole("Shigemichi", *CREW_ALIGNED_ROLES),
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
                CharacterIsRole("SQ", "Gnosia"),
                CharacterIsNotRole("Remnan", "Gnosia", "Bug"),
                CharacterIsNotRole("Raqio", "Gnosia"),
                HasMinGnosia(2),
            ), #Always requires loop 25+
        "Setup to Flowers":
            HasCharacters("Stella"),
        "Setup to Tears Go By":
            And(
                HasCharacters("Stella", "Raqio"),
                HasRoles("Engineer") | HasRoles("Doctor"),
                CharacterHasSkill("Stella", "Vote"),
            ),
        "Setup to Stella Note 5 Event":
            And(
                HasCharacters("Stella", "Jonas", "Setsu", "Remnan", "Yuriko"),
                CharacterIsRole("Player", *CREW_ALIGNED_ROLES),
                CharacterIsRole("Setsu", *CREW_ALIGNED_ROLES),
                CharacterIsRole("Stella", "Crew Member", "Guardian Angel"),
                HasMinCharacters(9),
                HasAll("Stella Note 1", "Stella Note 2", "Stella Note 3", "Stella Note 4"),
            ),
        "Setup to Chipie Note 2 - Result Event Ver.":
            And(
                HasCharacters("Chipie"),
                CharacterIsRole("Player", *CREW_ALIGNED_ROLES),
                CharacterIsRole("Chipie", "Gnosia"),
            ),
        "Setup to Chipie Crew Result Event":
            And(
                HasCharacters("Chipie"),
                CharacterIsRole("Player", *CREW_ALIGNED_ROLES),
                CharacterIsRole("Chipie", *CREW_ALIGNED_ROLES),
            ),
        "Setup to Comet Gnosia Result Event":
            And(
                HasCharacters("Comet"),
                CharacterIsRole("Player", *CREW_ALIGNED_ROLES),
                CharacterIsRole("Comet", "Gnosia"),
            ),
        "Setup to Comet Note 2 Event":
            And(
                HasCharacters("Comet"),
                CharacterIsRole("Player", *CREW_ALIGNED_ROLES),
                CharacterIsRole("Comet", *CREW_ALIGNED_ROLES),
            ),
        "Setup to Gina Gnosia Result Event":
            And(
                HasCharacters("Gina"),
                CharacterIsRole("Player", *CREW_ALIGNED_ROLES),
                CharacterIsRole("Gina", "Gnosia"),
                HasGroupUnique("Gina Notes", 4),
            ),
        "Setup to Gina Note 2 Event":
            And(
                HasCharacters("Gina"),
                CharacterIsRole("Player", *CREW_ALIGNED_ROLES),
                CharacterIsRole("Gina", *CREW_ALIGNED_ROLES),
            ),
        "Setup to Jonas & SQ Gnosia Result Event":
            And(
                HasCharacters("Jonas", "SQ"),
                CharacterIsRole("Player", *CREW_ALIGNED_ROLES),
                CharacterIsRole("Jonas", "Gnosia"),
                CharacterIsRole("SQ", "Gnosia"),
                HasMinGnosia(2),
            ),
        "Setup to Jonas Note 2 - Result Event Ver.":
            And(
                HasCharacters("Jonas", "Remnan"),
                CharacterIsRole("Player", *CREW_ALIGNED_ROLES),
                CharacterIsRole("Jonas", *CREW_ALIGNED_ROLES),
                CharacterIsRole("Remnan", *CREW_ALIGNED_ROLES),
            ),
        "Setup to Kukrushka's Song":
            And(
                HasCharacters("Kukrushka", "Jonas"),
                CharacterIsRole("Player", *CREW_ALIGNED_ROLES),
                CharacterIsRole("Kukrushka", "Gnosia"),
                CharacterIsRole("Jonas", "Gnosia", "AC Follower"),
            ),
        "Setup to Lovely Kukrushka":
            And(
                HasCharacters("Kukrushka", "Gina"),
                CharacterIsRole("Player", *CREW_ALIGNED_ROLES),
                CharacterIsRole("Gina", *CREW_ALIGNED_ROLES),
                CharacterIsRole("Kukrushka", *CREW_ALIGNED_ROLES),
            ),
        "Setup to Otome Gnosia Result Event":
            And(
                HasCharacters("Otome"),
                CharacterIsRole("Player", *CREW_ALIGNED_ROLES),
                CharacterIsRole("Otome", "Gnosia"),
            ),
        "Setup to Otome Note 2 Event":
            And(
                HasCharacters("Otome"),
                CharacterIsRole("Player", *CREW_ALIGNED_ROLES),
                CharacterIsRole("Otome", *CREW_ALIGNED_ROLES),
            ),
        "Setup to Raqio Gnosia Result Event":
            And(
                HasCharacters("Raqio"),
                CharacterIsRole("Player", *CREW_ALIGNED_ROLES),
                CharacterIsRole("Raqio", "Gnosia"),
            ),
        "Setup to Raqio Note 2 Event":
            And(
                HasCharacters("Raqio"),
                CharacterIsRole("Player", *CREW_ALIGNED_ROLES),
                CharacterIsRole("Raqio", *CREW_ALIGNED_ROLES),
            ),
        "Setup to Remnan Gnosia Result Event":
            And(
                HasCharacters("Remnan"),
                CharacterIsRole("Player", *CREW_ALIGNED_ROLES),
                CharacterIsRole("Remnan", "Gnosia"),
            ),
        "Setup to Remnan & Raqio Crew Result Event":
            And(
                HasCharacters("Remnan", "Raqio"),
                CharacterIsRole("Player", *CREW_ALIGNED_ROLES),
                CharacterIsRole("Remnan", *CREW_ALIGNED_ROLES),
                CharacterIsRole("Raqio", *CREW_ALIGNED_ROLES),
            ),
        "Setup to Setsu Gnosia Result Event":
            And(
                HasCharacters("Setsu"),
                CharacterIsRole("Setsu", "Gnosia"),
                Or(
                    CharacterIsRole("Player", "Gnosia") & HasMinGnosia(2),
                    CharacterIsRole("Player", "AC Follower"),
                ),
            ), #Always requires loop 20+
        "Setup to Setsu Crew Result Event":
            And(
                HasCharacters("Setsu"),
                CharacterIsRole("Player", *CREW_ALIGNED_ROLES),
                CharacterIsRole("Setsu", *CREW_ALIGNED_ROLES),
                Has("Setsu Note 2"),
            ), #Always requires loop 40+
        "Setup to Sha-Ming Gnosia Result Event":
            And(
                HasCharacters("Sha-Ming"),
                CharacterIsRole("Player", *CREW_ALIGNED_ROLES),
                CharacterIsRole("Sha-Ming", "Gnosia"),
            ),
        "Setup to Shigemichi Gnosia Result Event":
            And(
                HasCharacters("Shigemichi"),
                CharacterIsRole("Player", *CREW_ALIGNED_ROLES),
                CharacterIsRole("Shigemichi", "Gnosia"),
            ),
        "Setup to Shigemichi Crew Result Event":
            And(
                HasCharacters("Shigemichi"),
                CharacterIsRole("Player", *CREW_ALIGNED_ROLES),
                CharacterIsRole("Shigemichi", *CREW_ALIGNED_ROLES),
            ),
        "Setup to SQ Note 2 - Result Event Ver.":
            And(
                HasCharacters("SQ", "Remnan"),
                CharacterIsRole("Player", *CREW_ALIGNED_ROLES),
                CharacterIsRole("Remnan", *CREW_ALIGNED_ROLES),
                CharacterIsRole("SQ", "Gnosia"),
                HasMinGnosia(2), #Required for 2 alive crew with Gnosia win
            ),
        "Setup to Yuriko Gnosia Result Event":
            And(
                HasCharacters("Yuriko"),
                CharacterIsRole("Player", *CREW_ALIGNED_ROLES),
                CharacterIsRole("Yuriko", "Gnosia"),
            ),
        "Setup to Yuriko Crew Result Event":
            And(
                HasCharacters("Yuriko"),
                CharacterIsRole("Player", *CREW_ALIGNED_ROLES),
                CharacterIsRole("Yuriko", *CREW_ALIGNED_ROLES),
            ),
        "Setup to Bug Tutorial":
            HasRoles("Bug"),
        "Setup to Bug Loop":
            HasCharacters("Setsu") | OptionFilter(TutorialHandling, TutorialHandling.option_vanilla, operator="ne"), #Always requires Loop 16+
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
                HasCharacters("Comet", "Stella", "Shigemichi", "Remnan", "Jonas", "Setsu", "Sha-Ming"),
                CharacterIsRole("Player", *CREW_ALIGNED_ROLES),
                CharacterIsRole("Sha-Ming", "Gnosia"),
                CharacterIsNotRole("Stella", "Gnosia"),
                CharacterIsRole("Jonas", *HUMAN_ROLES),
                HasAll("Setsu Note 2", "Sha-Ming Note 3", "Comet Note 5"),
            ),
        "Bug Tutorial to Adventure In A Frozen World":
            And(
                HasCharacters("Comet"),
                CharacterIsRole("Player", "Gnosia"),
                CharacterIsRole("Comet", "Gnosia"),
                HasMinCharacters(8), #Minimum characters for Gnosia Ratio <= 25% With 2/8 Gnosia
                HasAll("Comet Note 4", "Comet Note 5"),
            ), #Always requires loop 60+
        "Bug Tutorial to Allacosia":
            And(
                HasCharacters("Gina", "Stella"),
                CharacterIsRole("Player", *CREW_ALIGNED_ROLES),
                CharacterIsRole("Gina", "Gnosia"),
                HasMinGnosia(2),
                Has("Gina Note 3"),
            ),
        "Bug Tutorial to Jonas & Kukrushka Note Event":
            And(
                HasCharacters("Jonas", "Setsu", "Kukrushka"),
                Has("Kukrushka Note 5"),
            ),
        "Bug Tutorial to The Kukrushka Problem":
            And(
                HasCharacters("SQ", "Remnan", "Yuriko", "Jonas", "Kukrushka"),
                CharacterIsNotRole("Kukrushka", "Gnosia"),
                Or(
                    And(
                        CharacterIsRole("Yuriko", *CREW_ALIGNED_ROLES),
                        CharacterIsNotRole("Jonas", *CREW_ALIGNED_ROLES),
                    ),
                    And(
                        CharacterIsRole("Jonas", *CREW_ALIGNED_ROLES),
                        CharacterIsNotRole("Yuriko", *CREW_ALIGNED_ROLES),
                    ),
                ),
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
                CharacterIsRole("Setsu", *CREW_ALIGNED_ROLES),
                CharacterIsRole("Kukrushka", "Gnosia"),
                HasAll("Jonas Note 3", "Jonas Note 5", "Kukrushka Note 4"),
            ),
        "Bug Tutorial to Don't Vote Event":
            And(
                HasCharacters("Otome", "Raqio"),
                HasRoles("Bug"),
                Or(
                    CharacterHasSkill("Otome", "Don't Vote"),
                    CharacterIsNotRole("Otome", "Bug"),
                ),
            ),
        "Bug Tutorial to Otome's Resolution":
            And(
                HasCharacters("Otome", "Stella", "Kukrushka", "Shigemichi"),
                CharacterIsRole("Shigemichi", *CREW_ALIGNED_ROLES),
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
                CharacterIsRole("Remnan", *CREW_ALIGNED_ROLES),
                CharacterIsRole("SQ", "Gnosia"),
                HasMinGnosia(2),
                HasAll("Remnan Note 3", "Yuriko Note 4"),
            ),
        "Bug Tutorial to Remnan Note 2 Event":
            And(
                HasCharacters("Remnan", "Stella", "Comet", "Raqio"),
                HasRoles("Bug"),
            ), #Also requires having seen a double elimination or loop 80+
        "Bug Tutorial to Hope For The Future":
            And(
                HasCharacters("Remnan"),
                CharacterIsRole("Player", *CREW_ALIGNED_ROLES),
                CharacterIsRole("Remnan", "Engineer", "Doctor", "Guardian Angel", "Crew Member"),
                HasAll("Remnan Note 4", "Remnan Note 2"),
            ),
        "Bug Tutorial to Setsu Note 2 Event":
            And(
                HasCharacters("Setsu"),
                CanBeOnSameTeam("Player", "Setsu"),
            ),
        "Bug Tutorial to Setsu Note 3 Event":
            And(
                HasCharacters("Setsu", "Sha-Ming"),
                HasMinGnosia(2),
            ),
        "Bug Tutorial to Ace In The Hole":
            And(
                HasCharacters("Sha-Ming"),
                CharacterHasSkill("Sha-Ming", "Grovel"),
            ),
        "Bug Tutorial to Game Sermon":
            And(
                HasCharacters("Shigemichi", "Jonas", "Setsu", "Remnan"),
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
                CharacterIsNotRole("SQ", "Guard Duty", "AC Follower", "Bug"),
                CharacterHasSkill("SQ", "Let's Collaborate"),
            ),
        "Bug Tutorial to Shigemichi In Love":
            And(
                HasCharacters("Shigemichi", "Stella"),
                CharacterIsRole("Stella", *CREW_ALIGNED_ROLES),
                CharacterIsRole("Shigemichi", "Crew Member", "Guardian Angel", "Guard Duty"),
                Has("Shigemichi Note 6"),
            ),
        "Bug Tutorial to Chaos":
            And(
                HasCharacters("Yuriko", "SQ"),
                CharacterHasSkill("Yuriko", "Block Argument"),
            ), #Always requires loop 50+
        "Bug Tutorial to Starship Oracle":
            And(
                HasCharacters("Yuriko", "Remnan", "Gina"),
                CharacterIsNotRole("Player", "Gnosia"),
                CharacterIsRole("Remnan", "Gnosia"),
                CharacterIsRole("Gina", *CREW_ALIGNED_ROLES),
                HasAny("Gina Note 2", "Event Seen: AWWG"),
            ),
        "Bug Tutorial to Confrontation":
            And(
                HasCharacters("Yuriko", "Setsu"),
                CharacterIsRole("Player", *CREW_ALIGNED_ROLES, "Bug"),
                CharacterIsRole("Setsu", *CREW_ALIGNED_ROLES, "Bug"),
                CharacterIsRole("Yuriko", "Gnosia"),
                HasMinGnosia(2),
                HasAll("Yuriko Note 2", "Event Seen: Sha-Ming Gnosia Ally Intro"),
            ), #Always requires loop 40+
        "Bug Tutorial to The Alien Gnos":
            And(
                HasCharacters("Yuriko", "Setsu"),
                CharacterIsNotRole("Player", "Bug"),
                Or(
                    CharacterIsNotRole("Player", "Gnosia", "Bug"),
                    CharacterIsNotRole("Yuriko", *CREW_ALIGNED_ROLES),
                ),
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
                CharacterIsRole("Player", *CREW_ALIGNED_ROLES),
                CharacterIsRole("SQ", "Bug"),
            ),
        "Raqio Note 6 Event to The Final Problem":
            And(
                HasCharacters("Raqio", "Yuriko"),
                CharacterIsRole("Player", *CREW_ALIGNED_ROLES),
                CharacterIsRole("Raqio", "Bug"),
                HasMinCharacters(9),
            ),
        "Raqio Note 6 Event to Loop After - Raqio Note 6 Event":
            HasCharacters("Setsu"),
        "Raqio Note 6 Event to Setsu's Origins":
            And(
                HasMinCharacters(15),
                CharacterIsRole("Player", *CREW_ALIGNED_ROLES),
                CharacterIsRole("Setsu", "Guardian Angel", "Guard Duty", "Crew Member"),
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
                HasRoles("Bug", "Engineer"),
                CharacterIsNotRole("Raqio", "Engineer"),
                CharacterHasSkill("Raqio", "Freeze All"),
            ),
        "The Final Problem to Loop After - The Final Problem":
            HasCharacters("Setsu"),
        "The Final Problem to After The Final Problem Result Event":
            And(
                HasCharacters("Setsu", "Yuriko"),
                CanBeOnSameTeam("Player", "Setsu"),
            ),
        "The Alien Gnos to Loop After - The Alien Gnos":
            HasCharacters("Setsu"),
        "The Alien Gnos to Tears Of SQ":
            And(
                HasCharacters("SQ", "Remnan"),
                CharacterIsRole("Player", "Gnosia"),
                CharacterIsRole("SQ", *CREW_ALIGNED_ROLES),
                HasMinCharacters(9),
                HasAll("SQ Note 1", "SQ Note 2", "SQ Note 3", "SQ Note 4", "Remnan Note 4"),
            ),
        "Raqio Quiz - Note 4 to Raqio Quiz - Note 5":
            And(
                HasRoles("Doctor"),
                HasMinCharacters(15),
                Has("Raqio Note 3"),
            ),
        "Raqio Quiz - Note 5 to Raqio Note 6 Event":
            And(
                HasCharacters("Raqio", "Setsu"),
                CharacterIsRole("Player", *CREW_ALIGNED_ROLES),
                CharacterIsRole("Raqio", *CREW_ALIGNED_ROLES),
                Has("Event Completed: The Alien Gnos"),
            ),
        "Return Of The Saint to To The Hangar":
            And(
                HasCharacters("Setsu", "Jonas", "Kukrushka"),
                CharacterIsNotRole("Player", "Gnosia"),
                CharacterIsNotRole("Setsu", "Gnosia"),
            ),
        "Fool And Be Fooled to Collaboration Hint Setsu Event":
            HasCharacters("Setsu", "SQ"),
        "After The Final Problem Result Event to World Without Gnosia Hint Result Event":
            And(
                HasCharacters("Yuriko"),
                CharacterIsRole("Player", *CREW_ALIGNED_ROLES),
                CharacterIsRole("Yuriko", *CREW_ALIGNED_ROLES),
            ),
        "AWWG - Unfilled Key to In The Loop Again":
            filled_key,
    }
    #Define Soft Logic
    entrance_to_soft_rule = {
        "Setup to Let's Collaborate Event":
            Or(
                Has("Chipie Note 2"),
                CharacterHasStats("Player", CharacterStats(charm=15)),
            ), #You can get this event without these requirements on Loop 40+
        "Setup to Comet Note 4 Event":
            has_easy_lie_detect, #You can always detect lies, but it will be hard
        "Setup to Don't Be Fooled Event":
            has_easy_lie_detect, #You can always detect lies, but it will be hard
        "Setup to Gina Note 6 Event":
            Or(
                characters_randomized | Has("Event Search"),
                HasMinCharacters(12), #Required characters * 2
            ), #You can get the necessary characters by getting lucky
        "Setup to Jonas The Wreck":
            Has("Jonas Note 2"), #You can get this event without this requirement on loop 35+
        "Setup to Regret Event":
            CharacterHasStats("Player", CharacterStats(charm=20)), #Or loop 60+
        "Setup to Let's Play":
            Has("Event Seen: AWWG"), #You can get this event without this requirement on loop 65+
        "Setup to Tears Go By":
            HasRoles("Engineer"), #You can theoretically get a fake doctor Definite Enemy to trigger Vote
        "Bug Tutorial to Citizen Slime":
            Or(
                characters_randomized | Has("Event Search"),
                HasMinCharacters(14) #Required characters * 2
            ), #You can get the necessary characters by getting lucky
        "Bug Tutorial to The Kukrushka Problem":
            Or(
                characters_randomized | Has("Event Search"),
                HasMinCharacters(10), #Required characters * 2
            ), #You can get the necessary characters by getting lucky
        "Bug Tutorial to Game Sermon":
            CharacterHasSkill("Player", "Step Forward"), #Shigemichi or Jonas can reveal role on their own
        "Bug Tutorial to Fool And Be Fooled":
            CharacterIsRole("SQ", "Gnosia"), #10% the event activates on crew aligned (before Gnosia ver.)
        "Bug Tutorial to Starship Oracle":
            And(
                HasMinCharacters(7), #You can avoid eliminations with ga, bug and by abusing vote ties
                HasAll("Gina Note 2", "Gina Note 3", "Event Seen: AWWG",
                    options=[OptionFilter(RandomizeNotes, True)],
                    filtered_resolution=True,
                ), #Otherwise requires loop 40+ (Always true with vanilla note placements)
            ),
        "Raqio Quiz - Guardian Angel to Raqio Quiz - Freeze All":
            CharacterIsNotRole("Player", "Engineer"), #You can get this by risking logic errors
    }
    for entrance_name in entrance_to_soft_rule:
        entrance_to_soft_rule[entrance_name] |= is_glitch_logic
    #Apply Rules
    for entrance_name in {*entrance_to_rule, *entrance_to_soft_rule}:
        rule = entrance_to_rule.get(entrance_name, True_()) & entrance_to_soft_rule.get(entrance_name, True_())
        world.set_rule(world.get_entrance(entrance_name), rule)
    #Add optional entrance rules
    optional = {}
    optional_soft = {}
    if world.options.allow_gender_specific_logic:
        optional |= {
            "Respec to Shower Room - Gina":
                HasCharacters("Gina"),
            "Respec to Gina In Love":
                And(
                    HasCharacters("Gina"),
                    CharacterIsRole("Player", *CREW_ALIGNED_ROLES),
                    CharacterIsNotRole("Gina", "AC Follower"),
                    CharacterHasSkill("Player", "Let's Collaborate"),
                    HasAll(
                        "Gina Romance Chain Started", "Apologized to Gina in Shower Room",
                        "Gina Note 1", "Gina Note 2", "Gina Note 3", "Gina Note 4", "Gina Note 5",
                        "Event Completed: Allacosia",
                    ),
                ),
            "Respec to Hope For The Future":
                And(
                    HasCharacters("Remnan"),
                    CharacterIsNotRole("Remnan", "Guard Duty"),
                    Or(
                        CharacterIsNotRole("Player", "Gnosia"),
                        CharacterIsNotRole("Remnan", "Gnosia", "Guard Duty"),
                    ),
                    HasAll("Remnan Note 4", "Remnan Note 2"),
                ),
            "Respec to Plastic Flower":
                And(
                    HasCharacters("Stella"),
                    CharacterIsRole("Player", *CREW_ALIGNED_ROLES),
                    CharacterIsRole("Stella", "Gnosia"),
                    HasMinCharacters(11),
                    Has("Stella Note 3"),
                ),
            "Respec to Stella Protected By Player Result Event":
                And(
                    HasCharacters("Stella"),
                    CharacterIsRole("Player", "Guardian Angel"),
                    CharacterIsRole("Stella", *CREW_ALIGNED_ROLES),
                ),
        }
    for entrance_name in optional_soft:
        optional_soft[entrance_name] |= is_glitch_logic
    for entrance_name in {*optional, *optional_soft}:
        rule = optional.get(entrance_name, True_()) & optional_soft.get(entrance_name, True_())
        world.set_rule(world.get_entrance(entrance_name), rule)

def set_all_location_rules(world: GnosiaWorld) -> None:
    location_to_rule = {
        "Unlock Event Search":
            Has("Setsu Note 2"),
    }
    location_to_soft_rule = {
        "Learn About Let's Collaborate":
            HasMinCharacters(8), #You can use gd, bug and vote ties to get to Night 2 with 2 Gnosia alive
        "Learn About Jonas 7":
            HasMinCharacters(8), #You can use gd, bug and vote ties to get to Night 3 with you, Setsu and Jonas alive
        "Learn About Kukrushka 6":
            HasMinCharacters(8), #You can use gd, bug and vote ties to get to Night 3 with you, Setsu and Jonas alive
    }
    for location_name in location_to_soft_rule:
        location_to_soft_rule[location_name] |= is_glitch_logic
    for location_name in {*location_to_rule, *location_to_soft_rule}:
        rule = location_to_rule.get(location_name, True_()) & location_to_soft_rule.get(location_name, True_())
        world.set_rule(world.get_location(location_name), rule)
    #Add optional location rules
    optional = {}
    optional_soft = {}
    if world.options.add_role_achievement_locations:
        optional |= {
            "Intrepid Investigator Achievement":
                And(
                    CharacterIsRole("Player", "Engineer"),
                    HasMinGnosia(3),
                ),
            "Guardian Angel Achievement":
                CharacterIsRole("Player", "Guardian Angel"),
            "Hero Achievement":
                And(
                    CharacterIsRole("Player", *CREW_ALIGNED_ROLES),
                    HasMinGnosia(6),
                ),
            "Loyal Servant Achievement":
                And(
                    CharacterIsRole("Player", "AC Follower"),
                    Or(
                        OtherThanCharacterIsRole("Player", "Engineer"),
                        OtherThanCharacterIsRole("Player", "Doctor"),
                    ),
                ),
            "Lonely Battle Achievement":
                And(
                    CharacterIsRole("Player", "Gnosia"),
                    HasMinCharacters(15),
                ),
            "Destroyer of the Universe Achievement":
                And(
                    CharacterIsRole("Player", "Bug"),
                    Or(
                        OtherThanCharacterIsRole("Player", "Engineer"),
                        OtherThanCharacterIsRole("Player", "Doctor"),
                    ),
                ),
        }
    if world.options.add_win_with_character_locations:
        optional |= {
            "Win With Gina":
                And(
                    HasCharacters("Gina"),
                    CanBeOnSameTeam("Player", "Gina"),
                ),
            "Win With SQ":
                And(
                    HasCharacters("SQ"),
                    CanBeOnSameTeam("Player", "SQ"),
                ),
            "Win With Raqio":
                And(
                    HasCharacters("Raqio"),
                    CanBeOnSameTeam("Player", "Raqio"),
                ),
            "Win With Stella":
                And(
                    HasCharacters("Stella"),
                    CanBeOnSameTeam("Player", "Stella"),
                ),
            "Win With Shigemichi":
                And(
                    HasCharacters("Shigemichi"),
                    CanBeOnSameTeam("Player", "Shigemichi"),
                ),
            "Win With Chipie":
                And(
                    HasCharacters("Chipie"),
                    CanBeOnSameTeam("Player", "Chipie"),
                ),
            "Win With Remnan":
                And(
                    HasCharacters("Remnan"),
                    CanBeOnSameTeam("Player", "Remnan"),
                ),
            "Win With Comet":
                And(
                    HasCharacters("Comet"),
                    CanBeOnSameTeam("Player", "Comet"),
                ),
            "Win With Yuriko":
                And(
                    HasCharacters("Yuriko"),
                    CanBeOnSameTeam("Player", "Yuriko"),
                ),
            "Win With Jonas":
                And(
                    HasCharacters("Jonas"),
                    CanBeOnSameTeam("Player", "Jonas"),
                ),
            "Win With Setsu":
                And(
                    HasCharacters("Setsu"),
                    CanBeOnSameTeam("Player", "Setsu"),
                ),
            "Win With Otome":
                And(
                    HasCharacters("Otome"),
                    CanBeOnSameTeam("Player", "Otome"),
                ),
            "Win With Sha-Ming":
                And(
                    HasCharacters("Sha-Ming"),
                    CanBeOnSameTeam("Player", "Sha-Ming"),
                ),
            "Win With Kukrushka":
                And(
                    HasCharacters("Kukrushka"),
                    CanBeOnSameTeam("Player", "Kukrushka"),
                ),
        }
    if world.options.add_win_against_character_locations:
        optional |= {
            "Win Against Gina":
                And(
                    HasCharacters("Gina"),
                    CanBeOnOppositeTeams("Player", "Gina"),
                ),
            "Win Against SQ":
                And(
                    HasCharacters("SQ"),
                    CanBeOnOppositeTeams("Player", "SQ"),
                ),
            "Win Against Raqio":
                And(
                    HasCharacters("Raqio"),
                    CanBeOnOppositeTeams("Player", "Raqio"),
                ),
            "Win Against Stella":
                And(
                    HasCharacters("Stella"),
                    CanBeOnOppositeTeams("Player", "Stella"),
                ),
            "Win Against Shigemichi":
                And(
                    HasCharacters("Shigemichi"),
                    CanBeOnOppositeTeams("Player", "Shigemichi"),
                ),
            "Win Against Chipie":
                And(
                    HasCharacters("Chipie"),
                    CanBeOnOppositeTeams("Player", "Chipie"),
                ),
            "Win Against Remnan":
                And(
                    HasCharacters("Remnan"),
                    CanBeOnOppositeTeams("Player", "Remnan"),
                ),
            "Win Against Comet":
                And(
                    HasCharacters("Comet"),
                    CanBeOnOppositeTeams("Player", "Comet"),
                ),
            "Win Against Yuriko":
                And(
                    HasCharacters("Yuriko"),
                    CanBeOnOppositeTeams("Player", "Yuriko"),
                ),
            "Win Against Jonas":
                And(
                    HasCharacters("Jonas"),
                    CanBeOnOppositeTeams("Player", "Jonas"),
                ),
            "Win Against Setsu":
                And(
                    HasCharacters("Setsu"),
                    CanBeOnOppositeTeams("Player", "Setsu"),
                ),
            "Win Against Otome":
                And(
                    HasCharacters("Otome"),
                    CanBeOnOppositeTeams("Player", "Otome"),
                ),
            "Win Against Sha-Ming":
                And(
                    HasCharacters("Sha-Ming"),
                    CanBeOnOppositeTeams("Player", "Sha-Ming"),
                ),
            "Win Against Kukrushka":
                And(
                    HasCharacters("Kukrushka"),
                    CanBeOnOppositeTeams("Player", "Kukrushka"),
                ),
        }
    if world.options.add_win_as_role_locations:
        optional |= {
            "Win As Engineer":
                CharacterIsRole("Player", "Engineer"),
            "Win As Doctor":
                CharacterIsRole("Player", "Doctor"),
            "Win As Guardian Angel":
                CharacterIsRole("Player", "Guardian Angel"),
            "Win As Guard Duty":
                CharacterIsRole("Player", "Guard Duty"),
            "Win As Crew Member":
                CharacterIsRole("Player", "Crew Member"),
            "Win As AC Follower":
                CharacterIsRole("Player", "AC Follower"),
            "Win As Gnosia":
                CharacterIsRole("Player", "Gnosia"),
            "Win As Bug":
                CharacterIsRole("Player", "Bug"),
        }
    if world.options.add_win_against_role_locations:
        optional |= {
            "Win Against Engineer":
                OtherThanCharacterIsRole("Player", "Engineer"),
            "Win Against Doctor":
                OtherThanCharacterIsRole("Player", "Doctor"),
            "Win Against Guardian Angel":
                OtherThanCharacterIsRole("Player", "Guardian Angel"),
            "Win Against Guard Duty":
                OtherThanCharacterIsRole("Player", "Guard Duty"),
            "Win Against Crew Member":
                OtherThanCharacterIsRole("Player", "Crew Member"),
            "Win Against AC Follower":
                OtherThanCharacterIsRole("Player", "AC Follower"),
            "Win Against Gnosia":
                OtherThanCharacterIsRole("Player", "Gnosia"),
            "Win Against Bug":
                OtherThanCharacterIsRole("Player", "Bug"),
        }
    for location_name in optional_soft:
        optional_soft[location_name] |= is_glitch_logic
    for location_name in {*optional, *optional_soft}:
        rule = optional.get(location_name, True_()) & optional_soft.get(location_name, True_())
        world.set_rule(world.get_location(location_name), rule)

def set_completion_condition(world: GnosiaWorld) -> None:
    match world.options.goal:
        case Goal.option_normal_ending:
            world.set_completion_rule(Has("Event Seen: Normal Ending"))
        case Goal.option_role_achievements:
            achievements = locations.get_groups()["Achievements"]
            achievements.difference_update(world.options.excluded_achievements)
            achievements.difference_update(world.options.exclude_locations)
            world.set_completion_rule(
                And(
                    *(CanReachLocation(achievement) for achievement in achievements)
                ),
            )
        case _:
            raise OptionError("Unknown or Undefined Goal")