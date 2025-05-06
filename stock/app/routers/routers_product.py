from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.settings.database import get_session
from app.schemas.product import ProductRequest #, ProductCreateRequest, ProductUpdateRequest
from app.models.tables import Product

router = APIRouter(prefix="/product", tags=["├── Atende requisito 1° - CRUD de produtos ──├"])

def product_get(product_name: str, session: Session) -> bool:
	query = select(Product).where(Product.name == product_name)
	result = session.scalars(query).first()
	return result


def product_exists(product_name: str, session: Session) -> bool:
	result = product_get(product_name, session)
	return result is not None


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def product_create(
	product: ProductRequest,
	session: Session = Depends(get_session),
):
	"""
	Criar um novo produto.

	Cria um produto a partir dos dados enviados no corpo da requisição.
	Retorna o produto criado.

	- **product**: objeto com os dados do produto (name, price, quantity, etc.)

	**Erros possíveis**:
	- 400: Produto já registrado.

	**Importante**
	- Atenção com a pontuação do preço, deve utilizar "." e não ','
	"""
	if product_exists(product.name, session):
		raise HTTPException(
			status.HTTP_400_BAD_REQUEST,
			"Product already registered.",
		)

	product_dict = product.model_dump()

	session.add(Product(**product_dict))
	session.commit()

	return product_dict


@router.get("/read/{product_name}")
async def product_read(
	product_name: str,
	session: Session = Depends(get_session),
):
	"""
	Buscar um produto por nome.

	Retorna os dados do produto com o nome especificado.

	- **product_name**: nome do produto (string)

	Exemplo de uso:
	`Notebook Dell`

	**Erros possíveis**:
	- 404: Produto não encontrado.
	"""

	product = product_get(product_name, session)

	if not product:
		raise HTTPException(status.HTTP_404_NOT_FOUND, "Product not found")
	return product


@router.put("/update/{product_name}", status_code=status.HTTP_200_OK)
async def product_update(
    product_name: str,
    product: ProductRequest,
    session: Session = Depends(get_session),
):
    """
    Atualizar um produto existente.

    Atualiza os dados de um produto com base no nome informado.

    - **product_name**: nome do produto atual a ser atualizado.
    - **product**: novos dados para atualizar


    **Erros possíveis**:
    - 404: Produto não encontrado.

	**Importante**:
	- O produto que esta de entrada no parâmetro sofrerá todas as alterações do `Request body`. 
    """
    if not product_exists(product_name, session):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Product not found")

    product_data = product.model_dump(exclude_unset=True)

    query = update(Product).where(Product.name == product_name).values(**product_data)

    session.execute(query)
    session.commit()

    return product_data


@router.delete("/delete/{product_name}")
async def product_delete(
	product_name: str,
	session: Session = Depends(get_session),
):
	"""
	Deletar um produto por nome.

	Remove o produto especificado do banco de dados.

	- **product_name**: nome do produto (string)

	Exemplo de uso:
	`Notebook Dell`

	**Erros possíveis**:
	- 404: Produto não encontrado.
	"""
	product = product_get(product_name, session)

	if not product:
		raise HTTPException(status.HTTP_404_NOT_FOUND, "Product not found")

	session.delete(product)
	session.commit()

	return {"message": "Product removed from database"}