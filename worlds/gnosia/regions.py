from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Region

if TYPE_CHECKING:
    from .world import GnosiaWorld



def create_and_connect_regions(world: GnosiaWorld) -> None:
    create_all_regions(world)
    connect_all_regions(world)

def create_all_regions(world: GnosiaWorld) -> None:
    #Add always present regions
    region_names = [
        #Non-Event Regions
        "Title Screen",
        "Setup",
        "Setsu Note 4 Region",
        "SQ Note 2 Region",
        "Chipie Note 2 Region",
        "Jonas Note 2 Region",
        #Tutorial Loops
        "Loop 1",
        "Loop 2",
        "Loop 3",
        "Loop 4",
        "Loop 5",
        "Loop 6",
        "Loop 7",
        "Loop 8",
        "Loop 9",
        "Loop 10",
        "Loop 11",
        "Loop 12",
        "Loop 13",
        "Bug Loop",
        "Bug Tutorial",
        #Character Events
        #Chipie
        "Let's Collaborate Event",
        "Chipie & Comet Note Event",
        "Chipie Note 5 Event",
        "Chipie & Shigemichi Note Event",
        #Comet
        "Comet Note 4 Event",
        "Shower Room - Comet",
        "Citizen Slime",
        "Say You're Human Event",
        "Adventure In A Frozen World",
        #Gina
        "Gina Note 3 Event",
        "Don't Be Fooled Event",
        "Allacosia",
        "Gina Note 6 Event",
        #Jonas
        "Jonas Note 3 Event",
        "Jonas The Wreck",
        "Obfuscate Event",
        "Jonas & Kukrushka Note Event",
        #Kukrushka
        "Kukrushka & Otome Note Event",
        "The Kukrushka Problem",
        "Kukrushka The Guard",
        "Return Of The Saint",
        "To The Hangar",
        "Regret Event",
        #Otome
        "Don't Vote Event",
        "Otome's Resolution",
        #Raqio
        "Shower Room - Raqio",
        "Raqio Quiz - Definite Human/Enemy",
        "Raqio Quiz - Guardian Angel",
        "Raqio Quiz - Note 4",
        "Raqio Quiz - Note 5",
        "Raqio Quiz - Freeze All",
        "Raqio Note 6 Event",
        "The Final Problem",
        #Remnan
        "Inescapable Past",
        "Remnan Note 2 Event",
        "Hope For The Future",
        #Setsu
        "Exaggerate Event",
        "Setsu Note 2 Event",
        "Loop After - The Alien Gnos",
        "Loop After - Raqio Note 6 Event",
        "Let's Play",
        "Loop After - The Final Problem",
        "After The Final Problem Result Event",
        "Setsu's Origins",
        "Setsu Note 3 Event",
        "Collaboration Hint Setsu Event",
        #Sha-Ming
        "Ace In The Hole",
        "Otome & Sha-Ming Note Event",
        "Small Talk Event",
        "Sha-Ming's Promise",
        "Sha-Ming Gnosia Ally Intro",
        #Shigemichi
        "Seek Agreement Event",
        "Game Sermon",
        "Shower Room - Shigemichi",
        "Shigemichi Note 4 Event",
        "Shigemichi Note 6 Event",
        #SQ
        "Fool And Be Fooled",
        "Retaliate Event",
        "Tears Of SQ",
        "SQ Note 2 - Gnosia Intro Ver.",
        #Stella
        "Shigemichi In Love",
        "Flowers",
        "Tears Go By",
        "Stella Note 5 Event",
        #Yuriko
        "Chaos",
        "Starship Oracle",
        "Confrontation",
        "The Alien Gnos",
        "World Without Gnosia Hint Result Event",
        "Respec & Recollection Event",
        #Result Events
        #Chipie
        "Chipie Note 2 - Result Event Ver.",
        "Chipie Crew Result Event",
        #Comet
        "Comet Gnosia Result Event",
        "Comet Note 2 Event",
        #Gina
        "Gina Gnosia Result Event",
        "Gina Note 2 Event",
        #Jonas
        "Jonas & SQ Gnosia Result Event",
        "Jonas Note 2 - Result Event Ver.",
        #Kukrushka
        "Kukrushka's Song",
        "Lovely Kukrushka",
        #Otome
        "Otome Gnosia Result Event",
        "Otome Note 2 Event",
        #Raqio
        "Raqio Gnosia Result Event",
        "Raqio Note 2 Event",
        #Remnan
        "Remnan Gnosia Result Event",
        "Remnan & Raqio Crew Result Event",
        #Setsu
        "Setsu Gnosia Result Event",
        "Setsu Crew Result Event",
        #Sha-Ming
        "Sha-Ming Gnosia Result Event",
        #Shigemichi
        "Shigemichi Gnosia Result Event",
        "Shigemichi Crew Result Event",
        #SQ
        "SQ Note 2 - Result Event Ver.",
        "A Prayer To The Stars",
        #Stella
        #None: All stella result events are gender-locked to male main characters
        #Yuriko
        "Yuriko Gnosia Result Event",
        "Yuriko Crew Result Event",
        #Other Events
        "Step Forward Event",
        #A World Without Gnosia
        "A World Without Gnosia - First Time Ver.",
        "In The Loop",
        "A World Without Gnosia - Unfilled Key Ver.",
        "In The Loop Again",
        "A World Without Gnosia - Normal Ending Ver.",
    ]
    regions = []
    for region_name in region_names:
        regions.append(Region(region_name, world.player, world.multiworld))
    #Add optional regions
    if world.options.allow_gender_specific_logic:
        gender_specific_events = [
            "Shower Room - Gina",
            "Gina In Love",
            "Plastic Flower",
            "Stella Protected By Player Result Event",
        ]
        for region_name in gender_specific_events:
            regions.append(Region(region_name, world.player, world.multiworld))
    world.multiworld.regions += regions

def connect_all_regions(world: GnosiaWorld) -> None:
    #Connect Tutorial Loops
    tutorial_loops = []
    for i in range(13):
        tutorial_loops.append(world.get_region(f"Loop {i + 1}"))
        if i > 0:
            tutorial_loops[i - 1].connect(tutorial_loops[i], f"Loop {i} to Loop {i + 1}")
    #Connect Title Screen To Loop 1 and Loop 13 to Setup
    world.get_region("Title Screen").connect(tutorial_loops[0], "Title Screen to Loop 1")
    setup = world.get_region("Setup")
    tutorial_loops[-1].connect(setup, "Loop 13 to Setup")
    #Connect Step Forward Event to Loop 6
    step_forward_event = world.get_region("Step Forward Event")
    tutorial_loops[5].connect(step_forward_event, "Loop 6 to Step Forward Event")
    #Connect all "Can Change Setup Settings" Requirements to Setup
    directly_connected_to_setup = [
        "Let's Collaborate Event",
        "Chipie & Comet Note Event",
        "Chipie Note 5 Event",
        "Chipie & Shigemichi Note Event",
        "Comet Note 4 Event",
        "Say You're Human Event",
        "Gina Note 3 Event",
        "Don't Be Fooled Event",
        "Gina Note 6 Event",
        "Jonas Note 3 Event",
        "Jonas The Wreck",
        "Obfuscate Event",
        "Kukrushka & Otome Note Event",
        "Regret Event",
        "Shower Room - Raqio",
        "Raqio Quiz - Definite Human/Enemy",
        "Exaggerate Event",
        "Let's Play",
        "Otome & Sha-Ming Note Event",
        "Small Talk Event",
        "Sha-Ming's Promise",
        "Sha-Ming Gnosia Ally Intro",
        "Seek Agreement Event",
        "Shower Room - Shigemichi",
        "Shigemichi Note 4 Event",
        "Shigemichi Note 6 Event",
        "Retaliate Event",
        "SQ Note 2 - Gnosia Intro Ver.",
        "Flowers",
        "Tears Go By",
        "Stella Note 5 Event",
        "Chipie Note 2 - Result Event Ver.",
        "Chipie Crew Result Event",
        "Comet Gnosia Result Event",
        "Comet Note 2 Event",
        "Gina Gnosia Result Event",
        "Gina Note 2 Event",
        "Jonas & SQ Gnosia Result Event",
        "Jonas Note 2 - Result Event Ver.",
        "Kukrushka's Song",
        "Lovely Kukrushka",
        "Otome Gnosia Result Event",
        "Otome Note 2 Event",
        "Raqio Gnosia Result Event",
        "Raqio Note 2 Event",
        "Remnan Gnosia Result Event",
        "Remnan & Raqio Crew Result Event",
        "Setsu Gnosia Result Event",
        "Setsu Crew Result Event",
        "Sha-Ming Gnosia Result Event",
        "Shigemichi Gnosia Result Event",
        "Shigemichi Crew Result Event",
        "SQ Note 2 - Result Event Ver.",
        "Yuriko Gnosia Result Event",
        "Yuriko Crew Result Event",
        "Bug Tutorial",
        "Bug Loop",
        "A World Without Gnosia - First Time Ver.",
    ]
    for region_name in directly_connected_to_setup:
        setup.connect(world.get_region(region_name), f"Setup to {region_name}")
    #Connect all Events connected to TutorialAfterBugScenario to Bug Tutorial Region
    after_bug_scenario = world.get_region("Bug Tutorial")
    connected_to_tutorial_after_bug_scenario = [
        "Shower Room - Comet",
        "Citizen Slime",
        "Adventure In A Frozen World",
        "Allacosia",
        "Jonas & Kukrushka Note Event",
        "The Kukrushka Problem",
        "Kukrushka The Guard",
        "Return Of The Saint",
        "Don't Vote Event",
        "Otome's Resolution",
        "Raqio Quiz - Guardian Angel",
        "Inescapable Past",
        "Remnan Note 2 Event",
        "Hope For The Future",
        "Setsu Note 2 Event",
        "Setsu Note 3 Event",
        "Ace In The Hole",
        "Game Sermon",
        "Fool And Be Fooled",
        "Shigemichi In Love",
        "Chaos",
        "Starship Oracle",
        "Confrontation",
        "The Alien Gnos",
        "Respec & Recollection Event",
        "A Prayer To The Stars",
    ]
    for region_name in connected_to_tutorial_after_bug_scenario:
        after_bug_scenario.connect(world.get_region(region_name), f"Bug Tutorial to {region_name}")
    if world.options.allow_gender_specific_logic:
        #Connect Gender-specific events to Yuriko Respec
        respec_event = world.get_region("Respec & Recollection Event")
        gender_specific_events = [
            "Shower Room - Gina",
            "Gina In Love",
            "Hope For The Future",
            "Plastic Flower",
            "Stella Protected By Player Result Event",
        ]
        for region_name in gender_specific_events:
            respec_event.connect(world.get_region(region_name), f"Respec to {region_name}")
    #Connect Other (Still Unconnected) Event Chains
    connection_dict = {
        "Raqio Note 6 Event": [
            "The Final Problem", 
            "Loop After - Raqio Note 6 Event", 
            "Setsu's Origins", 
            "Collaboration Hint Setsu Event",
        ],
        "Raqio Quiz - Guardian Angel": [
            "Raqio Quiz - Note 4",
            "Raqio Quiz - Freeze All",
        ],
        "The Final Problem": [
            "Loop After - The Final Problem",
            "After The Final Problem Result Event",
        ],
        "The Alien Gnos": [
            "Loop After - The Alien Gnos",
            "Tears Of SQ",
        ],
        "Raqio Quiz - Note 4": ["Raqio Quiz - Note 5"],
        "Raqio Quiz - Note 5": ["Raqio Note 6 Event"],
        "Return Of The Saint": ["To The Hangar"],
        "Fool And Be Fooled": ["Collaboration Hint Setsu Event"],
        "After The Final Problem Result Event": ["World Without Gnosia Hint Result Event"],
    }
    for start_event_name in connection_dict:
        for end_event_name in connection_dict[start_event_name]:
            world.get_region(start_event_name).connect(world.get_region(end_event_name), f"{start_event_name} to {end_event_name}")
    #Connect Fake Regions
    fake_region_dict = {
        "To The Hangar": ["Setsu Note 4 Region"],
        "Setsu's Origins": ["Setsu Note 4 Region"],
        "SQ Note 2 - Gnosia Intro Ver.": ["SQ Note 2 Region"],
        "SQ Note 2 - Result Event Ver.": ["SQ Note 2 Region"],
        "Let's Collaborate Event": ["Chipie Note 2 Region"],
        "Chipie Note 2 - Result Event Ver.": ["Chipie Note 2 Region"],
        "Jonas The Wreck": ["Jonas Note 2 Region"],
        "Jonas Note 2 - Result Event Ver.": ["Jonas Note 2 Region"],
    }
    for start_event_name in fake_region_dict:
        for end_event_name in fake_region_dict[start_event_name]:
            world.get_region(start_event_name).connect(world.get_region(end_event_name), f"{start_event_name} to {end_event_name}")
    #Connect A World Without Gnosia Event Chain
    awwg_first = world.get_region("A World Without Gnosia - First Time Ver.")
    in_the_loop = world.get_region("In The Loop")
    awwg_unfilled_key = world.get_region("A World Without Gnosia - Unfilled Key Ver.")
    itl_again = world.get_region("In The Loop Again")
    awwg_normal_ending = world.get_region("A World Without Gnosia - Normal Ending Ver.")
    awwg_first.connect(in_the_loop, "AWWG - First Ver. to In The Loop")
    awwg_first.connect(awwg_unfilled_key, "AWWG - First Ver. to Unfilled Key Ver.")
    awwg_unfilled_key.connect(itl_again, "AWWG - Unfilled Key to In The Loop Again")
    itl_again.connect(awwg_normal_ending, "In The Loop Again to Normal Ending")
