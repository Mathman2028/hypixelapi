from aiohttp import ClientSession
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import TYPE_CHECKING
from .games import Game, Stats
from .skyblock import profiles, bazaar, auctionhouse

if TYPE_CHECKING:
    from aiohttp import ClientResponse


class HypixelException(Exception):
    pass


class Hypixel:
    """The general class used to make API calls."""

    def __init__(self, key: str):
        self._key = key
        self._session = ClientSession("https://api.hypixel.net")

    @property
    def key(self):
        return self._key

    async def __aenter__(self):
        return self

    async def close(self):
        """Close the session, if you aren't using context managers."""
        await self._session.close()

    async def __aexit__(self, exc, exc_info, traceback):
        await self.close()

    async def get_player(self, uuid) -> "Player":
        """Get general data about a player given a UUID, along with game stats"""
        async with self._session.get(
            "/player", params={"uuid": uuid}, headers={"API-Key": self.key}
        ) as response:
            response: "ClientResponse"
            data = await response.json()
            if not data["success"]:
                raise HypixelException(response.status, data["cause"])
            player = data["player"]

            return Player(
                uuid=player["uuid"],
                display_name=player["displayname"],
                rank=player["rank"]
                if "rank" in player and player["rank"] != "NORMAL"
                else player["monthlyPackageRank"]
                if "monthlyPackageRank" in player
                and player["monthlyPackageRank"] != None
                else player["newPackageRank"]
                if "newPackageRank" in player and player["newPackageRank"] != "NONE"
                else player["packageRank"]
                if "packageRank" in player and player["packageRank"] != "NONE"
                else None,
                first_login=datetime.fromtimestamp(
                    player["firstLogin"] / 1000, timezone.utc
                ),
                last_login=datetime.fromtimestamp(
                    player["lastLogin"] / 1000, timezone.utc
                ),
                last_logout=datetime.fromtimestamp(
                    player["lastLogout"] / 1000, timezone.utc
                ),
                raw_stats=player["stats"],
                stats=Game.handle_all_json(player["stats"]),
            )

    async def get_skyblock_profile(self, profile_id) -> profiles.Profile:
        """Get skyblock data about a profile, given a profile ID."""
        async with self._session.get(
            "/skyblock/profile",
            params={"profile": profile_id},
            headers={"API-Key": self.key},
        ) as r:
            data = await r.json()
            if not data["success"]:
                raise HypixelException(r.status, data["cause"])
            return profiles.Profile.process_json(data["profile"])

    async def get_skyblock_profiles(self, uuid) -> list[profiles.Profile]:
        """Get all the skyblock profiles of a player, given the UUID."""
        async with self._session.get(
            "/skyblock/profiles", params={"uuid": uuid}, headers={"API-Key": self.key}
        ) as r:
            data = await r.json()
            if not data["success"]:
                raise HypixelException(r.status, data["cause"])
            return [profiles.Profile.process_json(i) for i in data["profiles"]]

    async def get_bazaar_data(self) -> dict[str, bazaar.Product]:
        """Get the bazaar data."""
        async with self._session.get("/skyblock/bazaar") as r:
            data = await r.json()
            if not data["success"]:
                raise HypixelException(r.status, data["cause"])
            return {
                k: bazaar.Product.process_json(v) for k, v in data["products"].items()
            }

    async def get_auction_house_data(self, page=0) -> auctionhouse.AuctionHouse:
        """Get all auctions on some page."""
        async with self._session.get("/skyblock/auctions", params={"page": page}) as r:
            data = await r.json()
            if not data["success"]:
                raise HypixelException(r.status, data["cause"])
            return auctionhouse.AuctionHouse.process_json(data)


@dataclass(slots=True)
class Player:
    uuid: str
    display_name: str
    rank: str | None
    first_login: datetime
    last_login: datetime
    last_logout: datetime
    raw_stats: dict
    stats: dict[Game, Stats]
