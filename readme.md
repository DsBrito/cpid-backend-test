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
   git clone https://github.com/DsBrito/cpid-backend-test.git
   cd cpid-backend-test/
   ```

2. Crie e ative um ambiente virtual:
   Entre dentro do diretório cpid-backend-test/
   ```bash
   python3 -m venv .venv
   source venv/bin/activate 
   ```

4. Instale as dependências:
   ```bash
      pip install "fastapi[standard]"
      pip install pydantic_settings
      pip install SQLAlchemy
      pip install mysqlclient
   ```

5. Utilize um banco de dados para a visualização (como o DBeaver) e configure as variáveis de ambiente para conexão com o banco de dados:
   ```py
   # app/settings/.env
      DB_HOST=127.0.0.1
      DB_PORT=3306
      DB_USER=root
      DB_PASS=cpid-test
      DB_NAME=cpid_backend_test
   ```

6. Execute a aplicação:
   ```bash
      fastapi dev app/main.py
   ```

7. Acesse a documentação da API:
   ```
   http://localhost:8000/docs
   ```

**Importante**: Neste projeto há um diretório `help-guide` caso precise de ajuda. 

# Banco de Dados (Caso precise)

Devemos nos certificar que temos um banco MySQL para que o nosso código se conecte, e por questão de simplicidade, vamos usar `docker` para subir um container de um banco MySQL e conectar à ele. Se você já possui um MySQL instalado na sua máquina você pode usá-lo e seguir para a próxima seção (8. Settings). Caso não possua o `docker` instalado, siga esse passo a passo:

- [WSL 2 && Ubuntu 22.04](https://medium.com/@habbema/guia-de-instala%C3%A7%C3%A3o-do-docker-no-wsl-2-com-ubuntu-22-04-9ceabe4d79e8)

Depois vamos executar um container contendo `mysql`:

```bash
docker run --name=stock_db_container --restart on-failure -p 3306:3306 -d mysql/mysql-server
```

Uma vez que o container está no ar, precisamos da senha gerada para o usuário `root`.

```bash
docker logs stock_db_container 2>&1 | grep GENERATED
```

Copie a root password que apareceu e salve ela.

Agora vamos alterar a senha do usuário `root`, basta executar o comando abaixo e depois colar a senha que você copiou acima:

```bash
docker exec -it stock_db_container mysql -uroot -p
```

Execute os comando SQL para alterar a senha, permitir a conexão com um *visual tool* e já aproveite para criar o banco que vamos utilizar:

```sql
ALTER USER 'root'@'localhost' IDENTIFIED BY 'cpid-test';
UPDATE mysql.user SET host = '%' WHERE user='root';
CREATE DATABASE cpid_backend_test;
quit
```

Depois disso, aperte CTRL+D para sair e execute:

```bash
docker restart company_db_container
```

## Observações

- Os tipos de movimentação válidos são "entrada" e "saída"/"saida"
- Para movimentações de saída, é verificado se há estoque suficiente
- O endpoint `/stock-management/movement` é a maneira recomendada para registrar movimentações, pois ele atualiza automaticamente o estoque
- O endpoint `/stock-management/summary/{product_name}` fornece uma visão completa do produto e suas movimentações

<p align="center">
  <img src="https://github.com/user-attachments/assets/aa9117ff-5b42-44d6-aa24-4e2a8be24d97" width="1000" alt="Imagem de exemplo">
</p>
