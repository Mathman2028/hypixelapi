from dataclasses import dataclass
from typing import Any

@dataclass
class Product:
    product_id: str
    sell_summary: list["Order"]
    buy_summary: list["Order"]
    sell_quick_status: "ProductQuickStatus"
    buy_quick_status: "ProductQuickStatus"
    
    @classmethod
    def process_json(cls: type["Product"], json_data):
        return cls(
            product_id=json_data["product_id"],
            sell_summary=[Order.process_json(i) for i in json_data["sell_summary"]],
            buy_summary=[Order.process_json(i) for i in json_data["buy_summary"]],
            sell_quick_status=ProductQuickStatus.process_json(json_data["quick_status"], "sell"),
            buy_quick_status=ProductQuickStatus.process_json(json_data["quick_status"], "buy")
        )

@dataclass
class Order:
    amount: int
    price_per_unit: float
    orders: int
    
    @classmethod
    def process_json(cls: type["Order"], json_data):
        return cls(
            amount=json_data["amount"],
            price_per_unit=json_data["pricePerUnit"],
            orders=json_data["orders"]
        )

@dataclass
class ProductQuickStatus:
    price: float
    volume: int
    moving_week: int
    orders: int
    
    @classmethod
    def process_json(cls: type["ProductQuickStatus"], json_data: dict[str, Any], prefix: str):
        json_data = {k.removeprefix(prefix): v for k, v in json_data.items() if k.startswith(prefix)}
        return cls(
            price=json_data["Price"],
            volume=json_data["Volume"],
            moving_week=json_data["MovingWeek"],
            orders=json_data["Orders"]
        )