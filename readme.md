# Sistema de Gerenciamento de Estoque - API

API desenvolvida para gerenciar a movimentação de estoque de produtos, permitindo cadastro de produtos, registro de entradas e saídas, e consulta do histórico de movimentações.

## Tecnologias utilizadas

- **Python**: Linguagem de programação principal
- **FastAPI**: Framework para construção de APIs
- **SQLAlchemy**: ORM para interação com o banco de dados
- **MySQL**: Banco de dados relacional

## Estrutura do projeto

```bash
app/
├── models/
│   └── tables.py           # Modelos de dados (Product, Moviment)
├── routers/
│   ├── routers_stock.py              # Endpoints de cadastro de produtos
│   ├── routers_moviment.py           # Endpoints de movimentação
│   └── routers_stock_management.py   # Endpoints de gerenciamento de estoque
├── schemas/
│   ├── moviment.py        # Esquemas de validação para movimentação
│   └── product.py           # Esquemas de validação para produtos
└── settings/
│   ├── config.py
    └── database.py       ]
```


## Como executar o projeto

### Pré-requisitos

- Python 3.8 ou superior
- MySQL

### Instalação

1. Clone o repositório:
   ```bash
   git clone 
   cd 
   ```

2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate 
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure as variáveis de ambiente para conexão com o banco de dados:
   ```
   DATABASE_URL=mysql+mysqlconnector://usuario:senha@localhost:3306/nome_do_banco
   ```

5. Execute a aplicação:
   ```bash
   uvicorn main:app --reload
   ```

6. Acesse a documentação da API:
   ```
   http://localhost:8000/docs
   ```

## API Endpoints

### Produtos (Stock)

#### Criar um novo produto

- **Endpoint**: `POST /stock/create`
- **Descrição**: Cadastra um novo produto no estoque

#### Consultar um produto

- **Endpoint**: `GET /stock/read/{stock_name}`
- **Descrição**: Retorna os detalhes de um produto específico pelo nome
- **Parâmetros de URL**: `stock_name` (string) - Nome do produto

#### Atualizar um produto

- **Endpoint**: `PUT /stock/update/{stock_name}`
- **Descrição**: Atualiza os dados de um produto existente
- **Parâmetros de URL**: `stock_name` (string) - Nome do produto


#### Excluir um produto

- **Endpoint**: `DELETE /stock/delete/{stock_name}`
- **Descrição**: Remove um produto do estoque
- **Parâmetros de URL**: `stock_name` (string) - Nome do produto


### Movimentações (Moviment)

#### Criar uma movimentação

- **Endpoint**: `POST /moviment/create`
- **Descrição**: Registra uma nova movimentação sem alterar o estoque


#### Consultar uma movimentação

- **Endpoint**: `GET /moviment/read/{moviment_id}`
- **Descrição**: Retorna os detalhes de uma movimentação específica pelo ID
- **Parâmetros de URL**: `moviment_id` (int) - ID da movimentação


#### Atualizar uma movimentação

- **Endpoint**: `PUT /moviment/update/{moviment_id}`
- **Descrição**: Atualiza os dados de uma movimentação existente
- **Parâmetros de URL**: `moviment_id` (int) - ID da movimentação

#### Excluir uma movimentação

- **Endpoint**: `DELETE /moviment/delete/{moviment_id}`
- **Descrição**: Remove uma movimentação do banco de dados
- **Parâmetros de URL**: `moviment_id` (int) - ID da movimentação

#### Consultar movimentações de um produto

- **Endpoint**: `GET /moviment/product/{product_name}`
- **Descrição**: Retorna todas as movimentações de um produto específico e um resumo das entradas, saídas e saldo atual
- **Parâmetros de URL**: `product_name` (string) - Nome do produto


### Gerenciamento de Estoque (Stock Management)

#### Registrar movimentação e atualizar estoque

- **Endpoint**: `POST /stock-management/movement`
- **Descrição**: Registra uma movimentação de entrada ou saída e atualiza o estoque automaticamente


#### Resumo do estoque de um produto

- **Endpoint**: `GET /stock-management/summary/{product_name}`
- **Descrição**: Retorna um resumo completo do produto, incluindo dados do estoque, totais de entrada e saída, e histórico de movimentações
- **Parâmetros de URL**: `product_name` (string) - Nome do produto

## Observações

- Os tipos de movimentação válidos são "entrada" e "saída"/"saida"
- Para movimentações de saída, é verificado se há estoque suficiente
- O endpoint `/stock-management/movement` é a maneira recomendada para registrar movimentações, pois ele atualiza automaticamente o estoque
- O endpoint `/stock-management/summary/{product_name}` fornece uma visão completa do produto e suas movimentações