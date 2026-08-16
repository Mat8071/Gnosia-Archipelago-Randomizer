from dataclasses import dataclass

from Options import DeathLink, StartInventoryPool, OptionGroup, PerGameCommonOptions, Range, Toggle, DefaultOnToggle, Choice, OptionSet
from . import items, locations



SLOT_DATA_OPTIONS = {
    "death_link",
    "exclude_locations",
    "goal",
    "required_note_percent",
    "excluded_achievements",
    "randomize_character_unlocks",
    "starting_crew_count",
    "randomize_role_unlocks",
    "randomize_notes",
    "randomize_skills",
    "add_role_achievement_locations",
    "add_win_with_character_locations",
    "add_win_against_character_locations",
    "add_win_as_role_locations",
    "add_win_against_role_locations",
    "tutorial_handling",
    "exp_multiplier",
    "allow_gender_specific_logic",
}

class Goal(Choice):
    """
    The goal you need to reach to beat the randomizer for this world.

    Normal Ending: Get the required note percent defined in the other options
        and enter A World Without Gnosia, ending the loop there.
    Role Achievements: Get all role-related achievements (Including "Hero")
        Achievements can be excluded by putting them in Excluded Achievements or Excluded Locations.
        You can add role achievements as locations as well, but it's not necessary for this goal to work.
    """

    display_name = "Goal"

    option_normal_ending = 0
    #Reserved spot for potential true ending-related goal
    option_role_achievements = 2

    default = option_normal_ending

class RequiredNotePercent(Range):
    """
    The % of Note Items you'll need in order to see the Normal Ending.
    Min: 0%, Max: 100%, Default: 80%, Vanilla Game: 100%
    """

    display_name = "Required Note Percent"

    range_start = 0
    range_end = 100
    default = 80

class ExcludedAchievements(OptionSet):
    """
    Achievements that are put in this list won't be needed for the Role Achievements Goal

    Does nothing if the goal is not Role Achievements
    """

    display_name = "Excluded Achievements"

    valid_keys = locations.get_groups()["Achievements"]

class RandomizeCharacterUnlocks(DefaultOnToggle):
    """
    Characters will no longer appear outside of tutorial loops unless unlocked.
    You will start with at least 4 random ones.
    (This option replaces progressive crew max items with specific character unlocks)
    """

    display_name = "Randomize Character Unlocks"

class StartingCrewCount(Range):
    """
    The maximum number of characters, including the player, per loop
    before any item is received to increase this.
    Min: 5, Max: 15
    """

    display_name = "Starting Crew Count"

    range_start = 5
    range_end = 15
    default = 5

class PriorityStartingCharacters(OptionSet):
    """
    When picking starting characters, characters from this list will be prioritized

    Does nothing if character unlocks are not randomized
    or if characters in Start Inventory From Pool already fill the crew count
    """

    display_name = "Priority Starting Characters"

    valid_keys = items.get_groups()["Characters"]

class RandomizeRoleUnlocks(DefaultOnToggle):
    """
    Roles will need to be found as items before being included in a loop
    Also adds 8 locations, one for each time a role is explained during tutorials
    or otherwise unlocked (in the case of the Bug Role)
    """

    display_name = "Randomize Role Unlocks"

class RandomizeNotes(DefaultOnToggle):
    """
    Notes will be shuffled into the item pool
    This also adds 82 Locations (one for each note)
    """

    display_name = "Randomize Notes"

class RandomizeSkills(DefaultOnToggle):
    """
    Skills will be shuffled into the item pool
    This also adds 17 Locations (one for each skill)

    Definite Human and Definite Enemy count as a single skill
    """

    display_name = "Randomize Skills"

class AddRoleAchievementLocations(Toggle):
    """
    Adds a location for each role-related achievement (Plus the Hero Achievement)

    Adds 6 locations in total
    """

    display_name = "Add Role Achievement Locations"

class AddWinWithCharacterLocations(Toggle):
    """
    Adds a location for the first time you win with each character
    (They must be on the same team you're on)

    Adds 14 locations in total
    """

    display_name = "Add Win With Character Locations"

class AddWinAgainstCharacterLocations(Toggle):
    """
    Adds a location for the first time you win against each character
    (They must be on any team except the team you're on)

    Adds 14 locations in total
    """

    display_name = "Add Win Against Character Locations"

class AddWinAsRoleLocations(Toggle):
    """
    Adds a location for the first time you win as each role

    Adds 8 locations in total
    """

    display_name = "Add Win As Role Locations"

class AddWinAgainstRoleLocations(Toggle):
    """
    Adds a location for the first time you win against each role
    (They must be on any team except the team you're on)

    Adds 8 locations in total
    """

    display_name = "Add Win Against Role Locations"

class TutorialHandling(Choice):
    """
    How to handle tutorial loops:

    Vanilla: Tutorials are not skipped at all.
    Skip: The game will start on loop 14, and you will receive all tutorial
        loop locations immediately. The Bug-related Tutorial loops will also be skipped
    Skip And Remove Locations: Same as Skip but without receiving any locations.
        Requires adding at least 14 Locations from "Extra Locations"
        Plus an additional 14 locations if randomizing notes
        Plus an additional 8 locations if randomizing roles
        These requirements can be lowered by having a higher starting crew count
        or by using any feature that removes items from the pool (such as Start Inventory From Pool)
    """

    display_name = "Tutorial Handling"

    option_vanilla = 0
    option_skip = 1
    option_skip_and_remove_locations = 2

    default = option_vanilla

class ExpMultiplier(Range):
    """
    When ending a loop, the experience gained will be multiplied by this number
    """

    display_name = "Exp Multiplier"

    range_start = 1
    range_end = 5
    default = 1

class AllowGenderSpecificLogic(Toggle):
    """
    By default, logic will assume you could have chosen any of the game's three gender options.
    As such, events will only be in logic if *all* genders can access the event with the current items.

    By activating this option, a patch will be applied to the game that allows you to instead
    change the main character's gender mid-game (by talking to Yuriko as the Bug at night)

    This allows any gender-specific event or logical path to be accessed in any save file
    and logic will account for that (so you may be required to make use of this feature if you enable it)
    """

    display_name = "Allow Gender-Specific Logic"

@dataclass
class GnosiaOptions(PerGameCommonOptions):
    #Base Archipelago Options
    start_inventory_from_pool: StartInventoryPool
    death_link: DeathLink
    #Goal
    goal: Goal
    required_note_percent: RequiredNotePercent
    excluded_achievements: ExcludedAchievements
    #Character Unlock Randomization
    randomize_character_unlocks: RandomizeCharacterUnlocks
    starting_crew_count: StartingCrewCount
    priority_starting_characters: PriorityStartingCharacters
    #Role Unlock Randomization
    randomize_role_unlocks: RandomizeRoleUnlocks
    #Other Items & Locations
    randomize_notes: RandomizeNotes
    randomize_skills: RandomizeSkills
    #Extra Locations
    add_role_achievement_locations: AddRoleAchievementLocations
    add_win_with_character_locations: AddWinWithCharacterLocations
    add_win_against_character_locations: AddWinAgainstCharacterLocations
    add_win_as_role_locations: AddWinAsRoleLocations
    add_win_against_role_locations: AddWinAgainstRoleLocations
    #Other Randomization
    #QOL & Other
    tutorial_handling: TutorialHandling
    exp_multiplier: ExpMultiplier
    allow_gender_specific_logic: AllowGenderSpecificLogic

option_groups = [
    OptionGroup(
        "Goal",
        [
            Goal,
            RequiredNotePercent,
            ExcludedAchievements,
        ],
    ),
    OptionGroup(
        "Character Unlock Randomization",
        [
            RandomizeCharacterUnlocks,
            StartingCrewCount,
            PriorityStartingCharacters,
        ],
    ),
    OptionGroup(
        "Role Unlock Randomization",
        [
            RandomizeRoleUnlocks,
        ],
    ),
    OptionGroup(
        "Other Items & Locations",
        [
            RandomizeNotes,
            RandomizeSkills,
        ],
    ),
    OptionGroup(
        "Extra Locations",
        [
            AddRoleAchievementLocations,
            AddWinWithCharacterLocations,
            AddWinAgainstCharacterLocations,
            AddWinAsRoleLocations,
            AddWinAgainstRoleLocations,
        ],
    ),
    #OptionGroup(
    #    "Other Randomization",
    #    [
    #
    #    ],
    #),
    OptionGroup(
        "QOL & Other",
        [
            TutorialHandling,
            ExpMultiplier,
            AllowGenderSpecificLogic,
        ],
    )
]

option_presets = {
    
}
