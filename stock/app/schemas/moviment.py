from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Literal

class MovimentRequest(BaseModel):
    product_name: str = Field(..., min_length=1, max_length=50, description="Nome do produto")
    moviment_type: str = Field(
        ..., 
        min_length=1, 
        max_length=50, 
        description="Tipo da movimentação (entrada ou saída)"
    )
    moviment_reason: str = Field(
        ..., 
        min_length=1, 
        max_length=50, 
        description="Motivo da movimentação (compra, venda, ajuste, etc)"
    )
    amount: int = Field(..., gt=0, description="Quantidade movimentada")
    movement_responsible: Optional[datetime] = Field(
        None, 
        description="Data e hora da movimentação (preenchido automaticamente se não informado)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "product_name": "Notebook Dell",
                "moviment_type": "entrada",
                "moviment_reason": "compra",
                "amount": 10
            }
        }