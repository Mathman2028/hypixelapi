from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum

@dataclass
class Profile:
    profile_id: str
    player_ids: list[str]
    cute_name: str | None
    selected: bool | None
    community_upgrades: dict | None
    banking: "Banking"
    
    @classmethod
    def process_json(cls, json_data: dict):
        return Profile(
            profile_id=json_data["profile_id"],
            player_ids=[i for i in json_data["members"]],
            cute_name=json_data.get("cute_name", None),
            selected=json_data.get("selected", None),
            community_upgrades=json_data.get("community_upgrades", None),
            banking=Banking.handle_json(json_data["banking"]) if "banking" in json_data else None
        )

@dataclass
class Banking:
    balance: int
    transactions: list["Transaction"]
    
    @classmethod
    def handle_json(cls, json_data):
        return cls(
            balance=json_data["balance"],
            transactions=[Transaction.handle_json(i) for i in json_data["transactions"]]
        )

class TransactionType(Enum):
    DEPOSIT = 0
    WITHDRAW = 1

@dataclass
class Transaction:
    timestamp: datetime
    action: TransactionType
    initiator_name: str
    amount: float
    
    @classmethod
    def handle_json(cls, json_data):
        return cls(
            timestamp=datetime.fromtimestamp(json_data["timestamp"]/1000, tz=timezone.utc),
            action=TransactionType[json_data["action"]],
            initiator_name=json_data["initiator_name"],
            amount=json_data["amount"]
        )