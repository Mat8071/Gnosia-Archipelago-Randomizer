from BaseClasses import ItemClassification, Location
from . import items

LOCATION_NAME_TO_ID = {

}

class GnosiaLocation(Location):
    game = "Gnosia"

def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {location_name: LOCATION_NAME_TO_ID[location_name] for location_name in location_names}

def create_all_locations(world: GnosiaWorld) -> None:
    create_regular_locations(world)
    create_events(world)

def create_regular_locations(world: GnosiaWorld) -> None:
    #TODO: Make this
    pass

def create_events(world: GnosiaWorld) -> None:
    #TODO: Make this
    pass
