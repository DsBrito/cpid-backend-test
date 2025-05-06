# from fastapi import FastAPI

# from app.routers import stock

# app = FastAPI()

# @app.get("/")
# async def main():
# 	return {"message": "Hello World"}

# app.include_router(stock.router)


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import routers_product, routers_moviment, routers_stock_management

app = FastAPI(
    title="DsBrito -> Stock Management API",
    description="""(CPID - Backend teste - feito por DsBrito) API para gerenciamento de estoque e movimentações.

    Requisitos do teste:
    - 1° Um endpoint para informar os dados do produto,
    - 2° Um endpoint para registrar a movimentação de entrada ou saída,
    - 3° Um endpoint para retornar os dados de movimentação e estoque do produto.""",
    version="1.0.0",
)

# rotas
app.include_router(routers_product.router)
app.include_router(routers_moviment.router)
app.include_router(routers_stock_management.router)

# @app.get("/")
async def main():
    return {"message": "Stock Management API is running"}