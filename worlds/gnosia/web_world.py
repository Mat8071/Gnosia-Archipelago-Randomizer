from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld

from .options import option_groups, option_presets

class GnosiaWebWorld(WebWorld):
    game = "Gnosia"

    theme = "ocean"

    setup_en = Tutorial(
        "MultiWorld Setup Guide",
        "A guide to setting up Gnosia for MultiWorld",
        "English",
        "setup_en.md",
        "setup/en",
        ["Mat8071"],
    )

    tutorials = [setup_en]

    option_groups = option_groups
    options_presets = option_presets