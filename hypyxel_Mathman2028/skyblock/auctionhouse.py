from dataclasses import dataclass
from datetime import datetime
from ..nbt import parse_data


@dataclass
class AuctionHouse:
    page: int
    total_pages: int
    total_auctions: int
    last_updated: datetime
    auctions: list["Auction"]

    @classmethod
    def process_json(cls: type["AuctionHouse"], json_data: dict):
        return cls(
            page=json_data["page"],
            total_pages=json_data["totalPages"],
            total_auctions=json_data["totalAuctions"],
            last_updated=datetime.fromtimestamp(json_data["lastUpdated"] / 1000),
            auctions=[Auction.process_json(i) for i in json_data["auctions"]],
        )


@dataclass
class Auction:
    uuid: str
    auctioneer: str
    profile_id: str
    coop: list[str]
    start: datetime
    end: datetime
    item_name: str
    item_lore: str
    extra: str
    category: str
    tier: str
    starting_bid: int
    item_data: dict
    claimed: bool
    claimed_bidders: list
    highest_bid_amount: int
    bids: list["Bid"]

    @classmethod
    def process_json(cls: type["Auction"], json_data: dict):
        return cls(
            uuid=json_data["uuid"],
            auctioneer=json_data["auctioneer"],
            profile_id=json_data["profile_id"],
            coop=json_data["coop"],
            start=datetime.fromtimestamp(json_data["start"] / 1000),
            end=datetime.fromtimestamp(json_data["end"] / 1000),
            item_name=json_data["item_name"],
            item_lore=json_data["item_lore"],
            extra=json_data["extra"],
            category=json_data["category"],
            tier=json_data["tier"],
            starting_bid=json_data["starting_bid"],
            item_data=parse_data(json_data["item_bytes"].encode("ascii")),
            claimed=json_data["claimed"],
            claimed_bidders=json_data["claimed_bidders"],
            highest_bid_amount=json_data["highest_bid_amount"],
            bids=[Bid.process_json(i) for i in json_data["bids"]],
        )


@dataclass
class Bid:
    auction_id: str
    bidder: str
    profile_id: str
    amount: int
    timestamp: datetime

    @classmethod
    def process_json(cls: type["Bid"], json_data):
        cls(
            auction_id=json_data["auction_id"],
            bidder=json_data["bidder"],
            profile_id=json_data["profile_id"],
            amount=json_data["amount"],
            timestamp=json_data["timestamp"],
        )
