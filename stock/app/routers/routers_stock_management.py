from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.settings.database import get_session
from app.schemas.moviment import MovimentRequest
from app.models.tables import Product, Moviment

router = APIRouter(prefix="/stock-management", tags=["├── Atende o requisito 2° e 3° (com alteração no estoque) ──├"])

@router.post("/movement", status_code=status.HTTP_201_CREATED)
async def register_movement(
    moviment: MovimentRequest,
    session: Session = Depends(get_session),
):
    """
    (2°) - Registra uma movimentação de entrada ou saída e atualiza o estoque automaticamente.
    
    Exemplo de requisição (entrada):
    ```json
    {
        "product_name": "Notebook Dell",
        "moviment_type": "entrada",
        "moviment_reason": "compra",
        "amount": 10
    }
    ```
    
    Exemplo de requisição (saída):
    ```json
    {
        "product_name": "Notebook Dell",
        "moviment_type": "saída",
        "moviment_reason": "venda",
        "amount": 5
    }
    ```
    """
    # Verificar se o produto existe
    query = select(Product).where(Product.name == moviment.product_name)
    product = session.scalars(query).first()
    
    if not product:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"Produto {moviment.product_name} não encontrado no estoque",
        )
    
    # Registrar a movimentação
    moviment_dict = moviment.model_dump()
    new_moviment = Moviment(**moviment_dict)
    session.add(new_moviment)
    
    # Atualizar o estoque do produto
    if moviment.moviment_type.lower() == "entrada":
        product.amount += moviment.amount
    elif moviment.moviment_type.lower() == "saída" or moviment.moviment_type.lower() == "saida":
        if product.amount < moviment.amount:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                f"Estoque insuficiente para  {moviment.product_name}. Estoque corrente: {product.amount}, Requisição: {moviment.amount}",
            )
        product.amount -= moviment.amount
    else:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Movimento deve ser 'entrada' ou 'saída'",
        )
    
    session.commit()
    
    return {
        "moviment": moviment_dict,
        "product": {
            "name": product.name,
            "current_stock": product.amount
        }
    }


@router.get("/summary/{product_name}")
async def get_stock_summary(
    product_name: str,
    session: Session = Depends(get_session),
):
    """
    (3°) - Retorna um resumo completo do produto, incluindo dados do estoque, 
    totais de entrada e saída, e histórico de movimentações.

    """
    # Verificar se o produto existe
    query_product = select(Product).where(Product.name == product_name)
    product = session.scalars(query_product).first()
    
    if not product:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"Produto {product_name} não encontrado no estoque",
        )
    
    # Buscar todas as movimentações do produto
    query_moviments = select(Moviment).where(Moviment.product_name == product_name)
    moviments = session.scalars(query_moviments).all()
    
    # Calcular entradas e saídas
    total_input = 0
    total_output = 0
    
    for moviment in moviments:
        if moviment.moviment_type.lower() == "entrada":
            total_input += moviment.amount
        elif moviment.moviment_type.lower() == "saída" or moviment.moviment_type.lower() == "saida":
            total_output += moviment.amount
    
    return {
        "product": {
            "name": product.name,
            "description": product.description,
            "current_stock": product.amount,
            "price": product.price,
            "category": product.category,
            "brand": product.brand,
            "supplier": product.supplier,
            "code": product.code
        },
        "movements_summary": {
            "total_input": total_input,
            "total_output": total_output,
            "balance": total_input - total_output
        },
        "movements_history": [
            {
                "id": m.id,
                "type": m.moviment_type,
                "reason": m.moviment_reason,
                "amount": m.amount,
                "date": m.movement_responsible
            } for m in moviments
        ]
    }