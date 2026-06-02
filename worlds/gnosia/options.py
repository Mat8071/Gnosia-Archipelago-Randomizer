from dataclasses import dataclass

from Options import DeathLink, StartInventoryPool, OptionGroup, PerGameCommonOptions, Range, Toggle, DefaultOnToggle, Choice

class Goal(Choice):
    """
    The goal you need to reach to beat the randomizer for this world.

    Normal Ending: Get the required note percent defined in the other options
    and enter A World Without Gnosia, ending the loop there.

    (Other goals will be added here in the future)
    """

    display_name = "Goal"

    option_normal_ending = 0

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

class RandomizeCharacterUnlocks(DefaultOnToggle):
    """
    Characters will no longer appear outside of tutorial loops unless unlocked.
    You will start with 4 random ones.
    (This option replaces progressive crew max items with specific character unlocks)
    """

    display_name = "Randomize Character Unlocks"

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
    start_inventory_from_pool: StartInventoryPool
    death_link: DeathLink
    goal: Goal
    required_note_percent: RequiredNotePercent
    randomize_character_unlocks: RandomizeCharacterUnlocks
    allow_gender_specific_logic: AllowGenderSpecificLogic

option_groups = [
    OptionGroup(
        "Goal Settings",
        [
            Goal,
            RequiredNotePercent,
        ],
    ),
    OptionGroup(
        "Items & Locations Randomization Settings",
        [
            RandomizeCharacterUnlocks,
        ],
    ),
    #OptionGroup(
    #    "Other Randomization Settings",
    #    [
    #
    #    ],
    #),
    OptionGroup(
        "Other Settings",
        [
            AllowGenderSpecificLogic,
        ],
    )
]

option_presets = {
    
}
