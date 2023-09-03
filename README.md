# typegen Is a Typed Dict Generator
Auto generate typed dicts.

## What it works for?
- Basic dictionaries 
- Nested dictionaries
- Dictionaries with Lists if the items are of same type
- Any level of nesting as long as list items are of same type
- None values default to `Optional[Any]`

## Usage:
```
usage: typegen [-h] -f FILE -v VAR -t TYPE_NAME [-o OUTPUT]

Import a variable from a file.

options:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Path to the python file (without .py extension)
  -v VAR, --var VAR     Variable name in the file
  -t TYPE_NAME, --type-name TYPE_NAME
                        Name for the type
  -o OUTPUT, --output OUTPUT
                        Path to the output file (default: out/<name of variable>.py)
```
## Example:

```
File: tests/fish_obj.py
```
``` 
fish = {
    'fish': {
        "health":3,
        "location":{
            "city": "belo",
            "state": "kansas"
        },
        "items": [{"item_id": 1, "value":4, "name": "scales", "variations": ["weak", "strong"]}, {"item_id": 2, "value":4, "name": "knife", "variations": ["weak", "strong"]}, {"item_id": 1, "value":4, "name": "scales", "variations": ["weak", "strong"]}   ]
        
    }
}
```


Run
```
typegen -f tests/fish_obj -v fish -t FishType
```


Output:

```
File: out/FishType.py
```
```
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
```

