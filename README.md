# typegen Is a Typed Dict Generator

## What it works for?
- Basic dictionaries 
- Nested dictionaries
- Dictionaries with Lists if the items are of same type
- Any level of nesting as long as list items are of same type
- NoneType values default to `Optional[Any]`

## When it fails
Each generation gets tested by pytype. In the case it fails it will let you know and provide a link to [typegen Issues](https://github.com/pestosoftware/typegen/issues).
### In many cases of failure:

It created the type, but didn't import something needed like a datetime. 

I'm looking for a clever way to handle the importing, but this should be a quick fix for now.

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
        "items": [
            {"item_id": 1, "value":4, "name": "scales", "variations": ["weak", "strong"]},
            {"item_id": 2, "value":4, "name": "knife", "variations": ["weak", "strong"]},
            {"item_id": 1, "value":4, "name": "scales", "variations": ["weak", "strong"]}  
        ]
        
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

## Maintenance

I will work to patch big issues with generating TypedDicts but will not expand the scope of the project for now.