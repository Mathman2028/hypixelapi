from dataclasses import dataclass
from collections import defaultdict
from . import games

@dataclass(slots=True)
class BedwarsStats(games.Stats):
    chests: "Chests"
    experience: int
    coins: int
    all_modes: "ModeStats"
    cosmetics: "Cosmetics"
    solo: "ModeStats"
    duos: "ModeStats"
    threes: "ModeStats"
    fours: "ModeStats"
    teams: "ModeStats"
    game = games.Game.BEDWARS

    @classmethod
    def process_json(cls, json_data: dict[str, int]):
        json_data = defaultdict(int, json_data)
        return cls(
            experience=json_data["Experience"],
            coins=json_data["coins"],
            chests=Chests.handle_chests(json_data),
            cosmetics=Cosmetics(
                kill_effect=json_data["activeKillEffect"],
                bed_destroy=json_data["activeBedDestroy"],
                projectile_trail=json_data["activeProjectileTrail"],
            ),
            all_modes=ModeStats._handle_mode(json_data),
            solo=ModeStats._handle_mode(json_data, "eight_one_"),
            duos=ModeStats._handle_mode(json_data, "eight_two_"),
            threes=ModeStats._handle_mode(json_data, "four_three_"),
            fours=ModeStats._handle_mode(json_data, "four_four_"),
            teams=ModeStats._handle_mode(json_data, "two_four_"),
        )
games.Game.stat_classes[games.Game.BEDWARS] = BedwarsStats

@dataclass(slots=True)
class ModeStats:
    """Dataclass storing bedwars stats."""

    kills: "KillDeathCount"
    deaths: "KillDeathCount"
    final_kills: "KillDeathCount"
    final_deaths: "KillDeathCount"
    beds: "BedStats"
    winloss: "WinLossStats"
    resources: "ResourcesCollected"
    purchases: "ItemsPurchased"
    plays: int

    @classmethod
    def _handle_mode(cls, json_data: dict[str, int], prefix: str = ""):
        json_data = defaultdict(
            int,
            {
                k.removeprefix(prefix): v
                for k, v in json_data.items()
                if k.startswith(prefix)
            },
        )
        return (
            cls(
                beds=BedStats(
                    breaks=json_data["beds_broken_bedwars"],
                    losses=json_data["beds_lost_bedwars"],
                ),
                deaths=KillDeathCount.handle_kill_death(json_data, "deaths"),
                final_deaths=KillDeathCount.handle_kill_death(
                    json_data, "final_deaths"
                ),
                kills=KillDeathCount.handle_kill_death(json_data, "kills"),
                final_kills=KillDeathCount.handle_kill_death(json_data, "final_kills"),
                plays=json_data["games_played_bedwars"],
                resources=ResourcesCollected.process_resources(json_data),
                purchases=ItemsPurchased(
                    total=json_data["items_purchased_bedwars"],
                    permanent=json_data["permanent_items_purchased_bedwars"],
                ),
                winloss=WinLossStats(
                    wins=json_data["wins_bedwars"],
                    losses=json_data["losses_bedwars"],
                ),
            )
        )


@dataclass(slots=True)
class KillDeathCount:
    """Dataclass storing information on different ways to die.
    Can be used for kills, final kills, deaths, or final deaths.
    """

    total: int
    magic: int
    void: int
    entity_attack: int
    entity_explosion: int
    fall: int
    projectile: int
    fire_tick: int

    @classmethod
    def handle_kill_death(cls, json_data: dict[str, int], kill_death: str):
        return (
            cls(
                total=json_data[f"{kill_death}_bedwars"],
                entity_attack=json_data[f"entity_attack_{kill_death}_bedwars"],
                entity_explosion=json_data[f"entity_explosion_{kill_death}_bedwars"],
                magic=[f"magic_{kill_death}_bedwars"],
                void=json_data[f"void_{kill_death}_bedwars"],
                fall=json_data[f"fall_{kill_death}_bedwars"],
                fire_tick=json_data[f"fire_tick_{kill_death}_bedwars"],
                projectile=json_data[f"projectile_{kill_death}_bedwars"],
            )
        )


@dataclass(slots=True)
class Chests:
    """Dataclass for opened chests."""

    total: int
    common: int
    rare: int
    
    @classmethod
    def handle_chests(cls, json_data):
        return cls(
            total=json_data["Bedwars_openedChests"],
            common=json_data["Bedwars_openedCommons"],
            rare=json_data["Bedwars_openedRares"],
        )


@dataclass(slots=True)
class ResourcesCollected:
    """Dataclass for resource collection stats."""

    total: int
    iron: int
    gold: int
    diamond: int
    emerald: int

    @classmethod
    def process_resources(cls, json_data: dict[str, int]):
        return cls(
            total=json_data["resources_collected_bedwars"],
            iron=json_data["iron_resources_collected_bedwars"],
            gold=json_data["gold_resources_collected_bedwars"],
            diamond=json_data["diamond_resources_collected_bedwars"],
            emerald=json_data["emerald_resources_collected_bedwars"],
        )


@dataclass(slots=True)
class BedStats:
    """Dataclass for bed stats."""

    breaks: int
    losses: int

    @property
    def bblr(self):
        return self.breaks / self.losses


@dataclass(slots=True)
class WinLossStats:
    """Dataclass for general winning and losing stats."""

    wins: int
    losses: int

    @property
    def wlr(self):
        return self.wins / self.losses


@dataclass(slots=True)
class ItemsPurchased:
    """Dataclass for item purchase stats."""

    total: int
    permanent: int

    @classmethod
    def process_items(cls, json_data: dict[str, int]):
        return cls(
            total=json_data["items_purchased_bedwars"],
            permanent=json_data["permanent_items_purchased_bedwars"],
        )


@dataclass
class Cosmetics:
    """Dataclass for active cosmetics."""

    kill_effect: str
    bed_destroy: str
    projectile_trail: str
