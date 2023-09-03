from typing import TypedDict, List, Optional, Any

class ItemsList(TypedDict):
    item_id: int
    value: int
    name: str
    variations: List[str]

class Location(TypedDict):
    city: str
    state: str

class Fish(TypedDict):
    health: int
    location: Location
    items: List[ItemsList]

class FishType(TypedDict):
    fish: Fish

