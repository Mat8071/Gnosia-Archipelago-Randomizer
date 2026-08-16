from collections.abc import Mapping
from typing import Any, Optional

from BaseClasses import ItemClassification
from worlds.AutoWorld import World
from Options import Option, OptionError

from . import items, locations, regions, rules, web_world
from . import options as gnosia_options

import worlds

class GnosiaWorld(World):
    """
    Gnosia is a SinglePlayer social deduction game
    """

    game = "Gnosia"
    version = "0.2.0"

    web = web_world.GnosiaWebWorld()

    options_dataclass = gnosia_options.GnosiaOptions
    options: gnosia_options.GnosiaOptions

    location_name_to_id = locations.LOCATION_NAME_TO_ID
    item_name_to_id = items.ITEM_NAME_TO_ID
    item_name_groups = items.get_groups()
    location_name_groups = locations.get_groups()

    origin_region_name = "Title Screen"

    #UT Stuff
    glitches_item_name = items.GLITCHES_ITEM_NAME
    ut_can_gen_without_yaml = True

    def generate_early(self) -> None:
        #UT Stuff
        re_gen_passthrough = getattr(self.multiworld, "re_gen_passthrough", {})
        if re_gen_passthrough and self.game in re_gen_passthrough:
            #Get the passed through slot data from the real generation
            slot_data: dict[str, Any] = re_gen_passthrough[self.game]

            generation_version = slot_data.get("version")
            if generation_version != self.version:
                raise worlds.tracker.TrackerException(
                    message=
                    "The multiworld you're trying to track was generated with a different "
                    "version of this AP world than the currently installed one."
                    f"\nGeneration Version: {generation_version or "Unknown"}"
                    f"\nInstalled AP World Version: {self.version}"
                )

            slot_options: dict[str, Any] = slot_data.get("options", {})
            for key, value in slot_options.items():
                opt: Optional[Option] = getattr(self.options, key, None)
                if opt is not None:
                    setattr(self.options, key, opt.from_any(value))
        #Validate options (first pass)
        if self.options.goal == gnosia_options.Goal.option_role_achievements:
            all_achievements = locations.get_groups()["Achievements"]
            needed_achievements = all_achievements.copy()
            needed_achievements.difference_update(self.options.excluded_achievements.value)
            needed_achievements.difference_update(self.options.exclude_locations.value)
            if not needed_achievements:
                raise OptionError(
                    "All achievements were excluded.\n"
                    "This would result in instant goaling."
                )
        if self.options.tutorial_handling == gnosia_options.TutorialHandling.option_skip_and_remove_locations:
            extra_locations_needed = 14
            characters_in_sifp = 0
            if self.options.randomize_notes:
                extra_locations_needed += 14
            if self.options.randomize_role_unlocks:
                extra_locations_needed += 8
            for item, quantity in self.options.start_inventory_from_pool.items():
                if ItemClassification.progression in items.DEFAULT_ITEM_CLASSIFICATIONS[item]:
                    if item in items.get_groups()["Characters"]:
                        characters_in_sifp += 1
                    if items.ITEM_NAME_TO_ID[item] >= 10000: #Start item ids with >1 quantity
                        extra_locations_needed -= quantity
                    else:
                        extra_locations_needed -= 1
            extra_locations = max(0, self.options.starting_crew_count - (characters_in_sifp + 1)) #Player
            if self.options.add_role_achievement_locations:
                extra_locations += 6
            if self.options.add_win_with_character_locations:
                extra_locations += 14
            if self.options.add_win_against_character_locations:
                extra_locations += 14
            if self.options.add_win_as_role_locations:
                extra_locations += 8
            if self.options.add_win_against_role_locations:
                extra_locations += 8
            if extra_locations_needed > extra_locations:
                raise OptionError(
                    "Not enough extra locations were added in order to be able to"
                    "remove the tutorial locations"
                )

    def create_regions(self) -> None:
        regions.create_and_connect_regions(self)
        locations.create_all_locations(self)

    def set_rules(self) -> None:
        rules.set_all_rules(self)

    def create_items(self) -> None:
        items.create_all_items(self)

    def create_item(self, name: str) -> items.GnosiaItem:
        return items.create_item_with_correct_classification(self, name)

    def get_filler_item_name(self) -> str:
        return items.get_random_filler_item_name(self)

    def fill_slot_data(self) -> Mapping[str, Any]:
        #Fill slot data
        slot_data: dict[str, Any] = {
            "version": self.version,
            "options": self.options.as_dict(
                *gnosia_options.SLOT_DATA_OPTIONS,
                toggles_as_bools=True,
            ),
        }
        #Return slot data
        return slot_data

    @staticmethod
    def interpret_slot_data(slot_data: dict[str, Any]) -> dict[str, Any]:
        #Trigger a regen in UT
        return slot_data
