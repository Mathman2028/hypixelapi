from enum import Enum, auto
from dataclasses import dataclass, field
from operator import getitem
from functools import partial
import json


class Tier(Enum):
    COMMON = 0
    UNCOMMON = 1
    RARE = 2
    EPIC = 3
    LEGENDARY  = 4
    MYTHIC = 5
    SUPREME = 6
    SPECIAL = 7
    VERY_SPECIAL = 8
    UNOBTAINABLE = 9

class Soulbound(Enum):
    COOP = auto()
    SOLO = auto()

class SwordType(Enum):
    SCYTHE = auto()
    KARAMBIT = auto()
    DAGGER = auto()
    AXE = auto()
    KATANA = auto()

class Origin(Enum):
    RIFT = auto()
    BINGO = auto()

class Crystal(Enum):
    FARM = auto()
    WHEAT_ISLAND = auto()
    RESOURCE_REGENERATOR = auto()
    DESERT_ISLAND = auto()
    MITHRIL = auto()
    WOODCUTTING = auto()
    FOREST_ISLAND = auto()
    FISHING = auto()
    NETHER_WART_ISLAND = auto()
    WINTER_ISLAND = auto()

class PrivateIsland(Enum):
    POND = auto()
    MINING_FOREST = auto()
    NETHER_WART = auto()
    NETHER = auto()
    WINTER = auto()
    DESERT = auto()
    FARMING = auto()
    MINING = auto()
    BARN = auto()

@dataclass(frozen=True)
class Item:
    id: str
    material: str
    name: str
    tier: Tier | None = None
    stats: dict | None = None
    color: str | None = None
    skin: str | None = None
    category: str | None = None
    durability: int | None = None
    npc_sell_price: int | None = None
    salvages: list | None = None
    soulbound: Soulbound | None = None
    glowing: bool = False
    unstackable: bool = False
    requirements: list | None = None
    museum: bool = False
    generator: str | None = None
    generator_tier: int | None = None
    furniture: str | None = None
    item_specific: dict | None = None
    description: str | None = None
    upgrade_costs: list | None = None
    gear_score: int | None = None
    dungeon_item: bool | None = None
    gemstone_slots: list | None = None
    dungeon_item_conversion_cost: dict | None = None
    catacombs_requirements: list | None = None
    enchantments: dict | None = None
    hide_from_viewrecipe_command: bool | None = None
    sword_type: SwordType | None = None
    ability_damage_scaling: float | None = None
    origin: Origin | None = None
    tiered_stats: dict | None = None
    motes_sell_price: int | None = None
    can_have_attributes: bool = False
    crystal: Crystal | None = None
    salvageable_from_recipe: bool = False
    rift_transferrable: bool = False
    salvage: dict | None = None
    private_island: PrivateIsland | None = None
    cannot_reforge: bool = False
    lose_motes_value_on_transfer: bool = False
    prestige: dict | None = None
    item_durability: float | None = None
    
    def __post_init__(self):
        if self.tier:
            object.__setattr__(self, "tier", Tier[self.tier])
        if self.origin:
            object.__setattr__(self, "origin", Origin[self.origin])
        if self.sword_type:
            object.__setattr__(self, "sword_type", SwordType[self.sword_type])
        if self.private_island:
            object.__setattr__(self, "private_island", PrivateIsland[self.private_island])
        if self.crystal:
            object.__setattr__(self, "crystal", Crystal[self.crystal])
        if self.soulbound:
            object.__setattr__(self, "soulbound", Soulbound[self.soulbound])
    
    @classmethod
    def handle_json(cls: type["Item"], json_data: dict):
        return cls(**json_data)

with open("c:\\Users\\jayhu\\hypixel-stuff\\hypixelapi\\skyblock\\items.json") as f:
    json_data = json.load(f)
    items = {k: Item(**v) for k, v in json_data.items()}

def from_name(name: str):
    if name.upper().replace(" ", "_") in items:
        return items[name.upper().replace(" ", "_")]
    else:
        for i in items.values():
            if i.name == name:
                return i