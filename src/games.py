from enum import Enum, nonmember
from abc import ABC, abstractmethod
from typing import Self

class Game(Enum):
    """An enum representing the games on Hypixel.
    The names here are uppercased versions of the database name, which is the one given by the API.
    Some games have different database names than their actual names. See the list of names at https://api.hypixel.net/#section/Introduction/GameTypes.
    """
    MAINLOBBY = 1
    QUAKE = 2
    WALLS = 3
    PAINTBALL = 4
    HUNGERGAMES = 5
    TNTGAMES = 6
    VAMPIREZ = 7
    WALLS3 = 13
    ARCADE = 14
    ARENA = 17
    UHC = 20
    MCGO = 21
    BATTLEGROUND = 23
    SUPERSMASH = 24
    GINGERBREAD = 25
    HOUSING = 26
    SKYWARS = 51
    TRUE_COMBAT = 52
    SPEEDUHC = 54
    SKYCLASH = 55
    LEGACY = 56
    PROTOTYPE = 57
    BEDWARS = 58 # Complete
    MURDERMYSTERY = 59
    BUILDBATTLE = 60
    DUELS = 61
    SKYBLOCK = 63
    PIT = 64
    REPLAY = 65
    SMP = 67
    WOOLGAMES = 68
    
    stat_classes: dict["Game", "Stats"] = nonmember({})
    
    def handle_json(self, json_data: dict):
        if self in self.stat_classes:
            return self.stat_classes[self].process_json(json_data)
        else:
            return NotImplemented
    
    @classmethod
    def handle_all_json(cls, json_data: dict):
        return {cls[i.upper()]: cls[i.upper()].handle_json(v) for i, v in json_data.items()}
        

class Stats(ABC):
    @classmethod
    @abstractmethod
    def process_json(json_data: dict) -> Self: ...

