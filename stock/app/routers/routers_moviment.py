from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, update, func
from sqlalchemy.orm import Session

from app.settings.database import get_session
from app.schemas.moviment import MovimentRequest
from app.models.tables import Moviment, Product

router = APIRouter(prefix="/moviment", tags=["├── Atende o requisito 2° e 3° (sem alterar o estoque) - CRUD de movimentação de produtos ──├"])

def moviment_get(moviment_id: int, session: Session):
    query = select(Moviment).where(Moviment.id == moviment_id)
    result = session.scalars(query).first()
    return result


def moviment_exists(moviment_id: int, session: Session) -> bool:
    result = moviment_get(moviment_id, session)
    return result is not None


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def moviment_create(
    moviment: MovimentRequest,
    session: Session = Depends(get_session),
):
    """
    Registra uma nova movimentação sem alterar o estoque.
    Use /stock-management/movement para registrar uma movimentação e atualizar o estoque automaticamente.
    
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

    **Importante**:
    - O tipo de movimentação aceita é "entrada", "saída" ou "saida".
    - É apenas uma criação em cima da tabela de 'moviments', para simular a entrada ou saída de um produto. Portantando não altera a quantidade real de produtos no banco.   
    - Caso queira alterar automaticamente ao inseir ou retirar um produto no banco, utilize a rota de Gestão de estoque.
    
    """
    # Verifica se o produto existe
    query = select(Product).where(Product.name == moviment.product_name)
    product = session.scalars(query).first()
    
    if not product:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"Produto {moviment.product_name} não encontrado no estoque",
        )
        
    # Validação do tipo de movimentação
    if moviment.moviment_type.lower() not in ["entrada", "saída", "saida"]:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Movement type must be 'entrada' or 'saída'",
        )
    
    moviment_dict = moviment.model_dump()
    
    session.add(Moviment(**moviment_dict))
    session.commit()

    return moviment_dict


@router.get("/read/{moviment_id}")
async def moviment_read(
    moviment_id: int,
    session: Session = Depends(get_session),
):
    """
    Retorna os detalhes de apenas uma movimentação específica pelo ID.
    """
    moviment = moviment_get(moviment_id, session)

    if not moviment:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Movimento não encontrado")
    return moviment


@router.put("/update/{moviment_id}", status_code=status.HTTP_200_OK)
async def moviment_update(
    moviment_id: int,
    moviment: MovimentRequest,
    session: Session = Depends(get_session),
):
    """
    Atualiza uma movimentação existente pelo ID.
    
    Exemplo de requisição:
    ```json
    {
        "product_name": "Notebook Dell",
        "moviment_type": "saída",
        "moviment_reason": "venda",
        "amount": 5
    }
    ```
    """
    if not moviment_exists(moviment_id, session):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Movimento não encontrado")
    
    # Validação do tipo de movimentação
    if moviment.moviment_type.lower() not in ["entrada", "saída", "saida"]:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Movement type must be 'entrada' or 'saída'",
        )

    moviment_data = moviment.model_dump(exclude_unset=True)

    query = update(Moviment).where(Moviment.id == moviment_id).values(**moviment_data)

    session.execute(query)
    session.commit()

    return moviment_data


@router.delete("/delete/{moviment_id}")
async def moviment_delete(
    moviment_id: int,
    session: Session = Depends(get_session),
):
    """
    Remove uma movimentação do banco de dados pelo ID.
    """
    moviment = moviment_get(moviment_id, session)

    if not moviment:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Movimento não encontrado")

    session.delete(moviment)
    session.commit()

    return {"message": "Movimento removido do banco de dados"}


@router.get("/product/{product_name}")
async def get_product_moviments(
    product_name: str,
    session: Session = Depends(get_session),
):
    """
    Retorna todas as movimentações de um produto específico e um resumo das entradas, saídas e saldo atual.
    """
    # Verificar se o produto existe
    product_query = select(Product).where(Product.name == product_name)
    product = session.scalars(product_query).first()
    
    if not product:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Produto {product_name} não encontrado")
    
    # Query para encontrar todas as movimentações de um produto
    query = select(Moviment).where(Moviment.product_name == product_name)
    moviments = session.scalars(query).all()
    
    if not moviments:
        # Retorna informações do produto mesmo sem movimentações
        return {
            "product_name": product_name,
            "product_current_stock": product.amount,
            "moviments": [],
            "summary": {
                "total_input": 0,
                "total_output": 0,
                "current_stock": product.amount
            }
        }
    
    # Calcular entradas, saídas e saldo
    total_input = 0
    total_output = 0
    
    for moviment in moviments:
        if moviment.moviment_type.lower() == "entrada":
            total_input += moviment.amount
        elif moviment.moviment_type.lower() == "saída" or moviment.moviment_type.lower() == "saida":
            total_output += moviment.amount
    
    # Retornar o resumo das movimentações
    return {
        "product_name": product_name,
        "product_current_stock": product.amount,
        "moviments": moviments,
        "summary": {
            "total_input": total_input,
            "total_output": total_output,
            "current_stock": product.amount  # Usando o valor real do estoque do produto
        }
    }