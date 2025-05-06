from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class ProductRequest(BaseModel):
    name: str = Field(examples=["Notebook Dell"])
    amount: int = Field(examples=[10])
    price: float = Field(examples=[3500.00])
    category: str = Field(examples=["Eletrônicos"])
    manufacture_date: date = Field(examples=["2023-08-01"])
    expiration_date: Optional[date] = Field(default=None, examples=[None])
    brand: Optional[str] = Field(default=None, examples=["Dell"])
    supplier: Optional[str] = Field(default=None, examples=["Distribuidora XYZ"])
    description: Optional[str] = Field(
        default=None, 
        examples=["Notebook Dell com processador i7, 16GB RAM, SSD 512GB"]
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Notebook Dell",
                "amount": 10,
                "price": 3500.00,
                "category": "Eletrônicos",
                "manufacture_date": "2023-08-01",
                "expiration_date": None,
                "brand": "Dell",
                "supplier": "Distribuidora XYZ",
                "description": "Notebook Dell com processador i7, 16GB RAM, SSD 512GB"
            }
        }
    }