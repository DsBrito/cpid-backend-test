# Roteiro de Desenvolvimento Backend

Autor: [Samuel Bagatelli Sampaio](https://github.com/samuelbagatelli)
Revisão: Guilherme Marques
Data: abril/20255

# 1. Objetivo

Capacitar os candidatos a criarem uma aplicação Backend (uma API REST) nos padrões do CPID capaz de se comunicar com um banco de dados básico e realizar as operações de Create, Read, Update e Delete - o famoso CRUD - do cadastro de uma empresa.

# 2. Ferramentas

As ferramentas para desenvolvimento são:

- Uma IDE de sua escolha. (Prefira alguma que você tenha familiaridade)
- WSL ou Ubuntu como SO.
- Python3+ → [https://www.python.org/](https://www.python.org/)
- FastAPI → [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)
- SQLAlchemy → [https://www.sqlalchemy.org/](https://www.sqlalchemy.org/)
- MySQL → [https://www.mysql.com/](https://www.mysql.com/)
- Alembic → [https://alembic.sqlalchemy.org/en/latest/tutorial.html](https://alembic.sqlalchemy.org/en/latest/tutorial.html)

Nesta aula, assumiremos conhecimento básico em Python, de sintáxe e de outras ferramentas da linguagem, HTTP e suas especificidades.

# 3. Configurando Ambiente de Trabalho

Usaremos o ambiente virtual do Python o `venv`. Para iniciar um ambiente virtual - e não encher seu computador, ou o do CPID com bibliotecas desnecessárias - siga o passo a passo, executando todos os comando no terminal linux:

1. Crie o ambiente virtual:
    
    ```bash
    mkdir company_app
    cd company_app
    python3 -m venv .venv
    ```
    
2. Ative o ambiente virtual:
    
    ```bash
    source .venv/bin/activate
    ```
    

Pronto, estamos dentro do ambiente virtual. Repare que no terminal há uma referencia à este ambiente no início da linha do terminal `(.venv)`. Agora, todas as bibliotecas que instalarmos, ficarão apenas neste ambiente virtual.

<aside>
💡

Para desativar o ambiente, entre com o comando baixo:

```bash
deactivate
```

e para ativar use o mesmo comando que já usamos antes:

```bash
source .venv/bin/activate
```

</aside>

Quaisquer arquivos que vamos criar ficarão fora dessa pasta `.venv`, de modo que os diretórios ficarão assim:

```
company_app/
├── .venv/
└── app/
		├── __init__.py
		└── main.py
		
```

Não se preocupe em criar a pasta `app` e seus arquivos agora, faremos isso depois.

# 4. Instalando Dependências

Primeiro, vamos começar com o FastAPI. Um framework eficiente para o desenvolvimento de APIs com fácil escalabilidade para o uso da estrutura de micros serviços, mas não se preocupe com isso agora, vamos fazer uma API REST.

Sinta-se à vontade para consultar a documentação, mas para instalar a biblioteca basta executar os comandos:

```bash
pip install "fastapi[standard]"
pip install pydantic_settings
```

Logo em seguida, instale o SQLAlchemy para conexão com o banco de dados e pydantic_settings para configurações de variáveis de ambiente.

```bash
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential pkg-config
```

---

```bash
pip install SQLAlchemy
pip install mysqlclient
```

# 5. Mão na Massa

Crie na raiz do projeto um arquivo `main.py` esse será o arquivo principal da nossa aplicação. Depois disso, importe a biblioteca e inicie uma instância do aplicação com FastAPI. Se tiver alguma dúvida de como fazer isso, consulte a documentação em [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/), mas tente fazer de forma intuitiva.

Uma dica: a classe que inicia a aplicação se chama **FastAPI**.

Crie também um arquivo `__init__.py` para iniciarmos um módulo `Python`no nosso diretório.

Se estiver no terminal linux, você pode usar os comandos abaixo para criar a pasta`app` e demais arquivos dentro dela:

```bash
mkdir app
touch app/__init__.py app/main.py
```

Após instalar o `FastAPI` seu diretório de arquivo deve estar parecido com isso:

```bash
company_app/
├── .venv/
└── app/
		├── __init__.py
		└── main.py
```

---

Em seu arquivo `app/main.py` , insira o código abaixo: 

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def main():
	return {"message": "Hello World"}
```

A partir daqui, já podemos acessar nossa API, basta iniciar a aplicação:

```bash
fastapi dev app/main.py
```

Acesse o URL [http://localhost:8000](http://localhost:8000) para ver o que acontece. Sua mensagem está na tela, tente alterar no código para ver o que acontece.

# 6. Rotas

Um conceito básico quando utilizamos uma API são suas rotas, pense o seguinte, temos uma aplicação de gerência de produtos de um mercado. Nesse mercado temos produtos de limpeza, frutas, legumes, bebidas, higiene pessoal e etc. Então nós como consumidores, quando entramos nesse mercado, esperamos que cada produto esteja separado por setor. Para isso, usamos as rotas.

Caso queiramos um produto de limpeza, podemos fazer uma requisição `GET` para a rota `/limpeza`. Para frutas, podemos acessar `/frutas`, e assim por diante.

Dentro da biblioteca `FastAPI` é bem simples utilizar rotas, basta criar um novo “roteador” *(router)* com a classe `APIRouter`. Para melhor organização, no CPID utilizamos uma pasta para organizar nossos “roteadores”.

```
company_app/
├── .venv/
└── app/
		├── routers/
		|		└── company.py
		├── __init__.py
		└── main.py
```

<aside>
💡

Você pode usar os comandos abaixo para criar a pasta `routers` e `company.py` :

```bash
mkdir app/routers
touch app/routers/company.py
```

</aside>

Vamos voltar para o conteúdo da nossa rota depois, mas por enquanto deixamos assim:

```python
# app/routers/company.py

from fastapi import APIRouter

router = APIRouter(prefix="/company", tags=["Company"])
```

---

Atualize o final do nosso arquivo [`main.py`](http://main.py) parar incluir nosso novo `router`:  

```bash
# app/main.py

## adicione este import:
from app.routers import company

# [...]  código omitido

## adicione este include:
app.include_router(company.router)
```

# 7. Banco de Dados

Devemos nos certificar que temos um banco MySQL para que o nosso código se conecte, e por questão de simplicidade, vamos usar `docker` para subir um container de um banco MySQL e conectar à ele. Se você já possui um MySQL instalado na sua máquina você pode usá-lo e seguir para a próxima seção (8. Settings). Caso não possua o `docker` instalado, siga esse passo a passo:

- [WSL 2 && Ubuntu 22.04](https://medium.com/@habbema/guia-de-instala%C3%A7%C3%A3o-do-docker-no-wsl-2-com-ubuntu-22-04-9ceabe4d79e8)

Depois vamos executar um container contendo `mysql`:

```bash
docker run --name=company_db_container --restart on-failure -p 3306:3306 -d mysql/mysql-server
```

Uma vez que o container está no ar, precisamos da senha gerada para o usuário `root`.

```bash
docker logs company_db_container 2>&1 | grep GENERATED
```

Copie a root password que apareceu e salve ela.

Agora vamos alterar a senha do usuário `root`, basta executar o comando abaixo e depois colar a senha que você copiou acima:

```bash
docker exec -it company_db_container mysql -uroot -p
```

Execute os comando SQL para alterar a senha, permitir a conexão com um *visual tool* e já aproveite para criar o banco que vamos utilizar:

```sql
ALTER USER 'root'@'localhost' IDENTIFIED BY '<nova-senha>';
UPDATE mysql.user SET host = '%' WHERE user='root';
CREATE DATABASE <nome-banco>;
quit
```

Depois disso, aperte CTRL+D para sair e execute:

```bash
docker restart company_db_container
```

# 8. Settings

Para que nosso código possa se conectar ao banco de dados que criamos, precisamos passar algumas informações para ele, e essas informações ficam em variáveis de ambiente dentro do nosso código em um arquivo `settings/.env`. Então devemos ter um novo diretório com a seguinte estrutura:

```bash
app/
└── settings/
		├── .env
		├── config.py
		└── database.py
```

<aside>
💡

Use os comandos abaixo no terminal linux para criar os arquivos:

```bash
mkdir app/settings
cd app/settings
touch .env config.py database.py
```

</aside>

Começando por `config.py` temos:

```python
# app/settings/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
	model_config = SettingsConfigDict(env_file="app/settings/.env")
	
	db_user: str
	db_pass: str
	
	db_host: str
	db_port: int
	db_name: str
```

A classe `Settings` é responsável por identificar o arquivo contendo as variáveis de ambiente `.env` e extrair as variáveis que possuam os mesmos nomes (porém, em CAPS LOCK) dos atributos que definimos para a classe.

Depois disso faremos a conexão com o banco de dados usando a biblioteca SQLAlchemy, da seguinte forma:

```python
# app/settings/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, declarative_base, sessionmaker

from app.settings.config import Settings

settings = Settings() # pyright: ignore

SQLALCHEMY_DATABASE_URL = (
	f"mysql+mysqldb://"
	f"{settings.db_user}"
	f":{settings.db_pass}"
	f"@{settings.db_host}"
	f":{settings.db_port}"
	f"/{settings.db_name}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autoflush=False, bind=engine)

Base = declarative_base()

def get_session():
	"""Create a ORM local session with the database and closes when finished."""
	session = SessionLocal()
	try:
		yield session
	finally:
		session.close()
```

Aqui temos uma conexão dinâmica com o banco de dados. Primeiro, definimos o URL do banco que queremos nos conectar, e ali passamos todas as informações necessárias para o SQLAlchemy fazer essa conexão, como a API de banco de dados que vamos utilizar, que aqui é o `mysqlclient`, o usuário, senha, host e porta para conectar com o banco e o nome do banco de dados.

Logo depois, criamos a `engine` e uma classe de `Session` que será efetivamente nossa conexão com o banco, nos permitindo realizar operações nesse banco.

A função `get_session` é uma função que usamos para garantir que a conexão com o banco será encerrada assim que terminarmos de usá-la.

Agora precisamos configurar o arquivo `.env` para incluir as informações dos bancos de dados.

```
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASS=<senha-que-você-configurou>
DB_NAME=<nome-que-você-deu-ao-banco>
```

# 9. Models

As `models` são uma representação, com classes, de uma tabela do banco de dados. Nesse exemplo temos apenas uma tabela, a `company` então precisamos criar apenas uma `model`. Mas pensando em escalabilidade, crie uma pasta **models/** para melhor organização das models.

Como já instalamos a biblioteca SQLAlchemy, e ela é nossa principal conexão com o banco de dados, vamos usar ela para criar nossas models.

Dentro da pasta **models/** crie um arquivo `company.py` para representar a tabela company. Nossa tabela deve possuir os seguintes campos:

- **ID:** Uma primary key que se auto incrementa à cada inserção;
- **Name:** O nome da empresa; (50)
- **Description:** A descrição da empresa; (100)
- **Telephone:** O número de telefone da empresa; (20)
- **Address:** O endereço físico da empresa. (200)

Os tipos de dados de cada linha da tabela são Strings, exceto pelo ID, que é um inteiro, e o tamanho máximo de cada string está entre parênteses. Dentro do arquivo `company.py` importe `DeclarativeBase, Mapped, mapped_column` da biblioteca `sqlalchemy.orm` para que possamos criar nossa classe modelo:

Vamos primeiro criar a pasta e o arquivo:

```bash
mkdir app/models
touch app/models/company.py
```
E agora podemos editar nosso `models/company.py`:

```python
# app/models/company.py
from sqlalchemy import BigInteger
from sqlalchemy.orm import MappedColumn, mapped_column

from app.settings.database import Base

class Company(Base):
	__tablename__ = "company"
	
	id: Mapped[BigInteger] = mapped_column(
		BigInteger,
		primary_key=True,
		autoincrement=True,
	)
```

Note que ainda estão faltando alguns atributos da classe, ou linhas da nossa tabela, a serem implementados. Seguindo o exemplo acima, preencha os atributos que estão faltando. Caso tenha alguma dúvida, sinta-se à vontade para consultar a [documentação](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#orm-declarative-table), mas se desafie a fazer sem consultar.

# 10. Alembic

Para facilitar a criação da tabela `company` no banco de dados, vamos utilizar a biblioteca Alembic que utiliza o conceito de migrations para criar tabelas em um banco de dados.

## 10.1 Instalação

Primeiro, instale e inicie a biblioteca no diretório raiz da aplicação:

```bash
# ~/company$
pip install alembic
alembic init alembic
```

## 10.2 Configuração

Agora passando para as configurações do Alembic, lembra quando eu disse que uma model é uma representação de uma tabela do banco de dados como uma classe Python? Então, nós podemos fazer o caminho contrário, utilizar uma model para criar uma tabela usando o Alembic. Para isso, precisamos dizer à biblioteca onde estão nossas models e em qual banco ela deve criar isso.

Altere o arquivo `env.py` para incluir as configurações necessárias.

```python
# ~/company/alembic/env.py

#  ... código omitido

# from alembic import context

from app.settings.database import SQLALCHEMY_DATABASE_URL

# ... código omitido 

#config = context.config

config.set_main_option(
    "sqlalchemy.url",
    SQLALCHEMY_DATABASE_URL,
)

#target_metadata = None

from app.models import company
target_metadata = company.Base.metadata

# ... código omitido 
```

## 10.1 Realizar migration

Depois disso, vamos gerar uma migration automaticamente, execute o comando abaixo a partir da raiz do projeto:

```bash
alembic revision --autogenerate -m "initial" --rev-id 1
```

Para criar as tabelas no banco de acordo com a revision gerada, execute o comando abaixo:

```bash
alembic upgrade head
```

# 11. Schemas

Os schemas são padronizações, formas da nossa aplicação dizer o que ela espera receber e o que ela vai responder, vamos criar nossos `schemas` :

Primeiro vamos criar a pasta e o arquivo dentro dessa pasta:

```bash
mkdir app/schemas
touch app/schemas/company.py
```
Agora podemos editar nosso arquivo com o código abaixo:

```python
#app/schemas/company.py

from pydantic import BaseModel

class CompanyRequest(BaseModel):
	name: str
	description: str
	telephone: str
	address: str
```

# 12. CRUD

Agora vamos implementar as nossas funções do CRUD no arquivo `app/routers/company.py`

## 12.1. Create

Para fazermos um create, precisamos fazer uma requisição `POST` à nossa API, vamos criá-la.

```python
# app/routers/company.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.settings.database import get_session
from app.schemas.company import CompanyRequest
from app.models.company import Company

router = APIRouter(prefix="/company", tags=["Company"])

def company_get(company_name: str, session: Session) -> bool:
	query = select(Company).where(Company.name == company_name)
	result = session.scalars(query).first()
	return result

def company_exists(company_name: str, session: Session) -> bool:
	result = company_get(company_name, session)
	return result is not None

@router.post("/create", status_code=status.HTTP_201_CREATED)
async def company_create(
	company: CompanyRequest,
	session: Session = Depends(get_session),
):
	if company_exists(company.name, session):
		raise HTTPException(
			status.HTTP_400_BAD_REQUEST,
			"Company already registered.",
		)
		
	company_dict = company.model_dump()
	
	session.add(Company(**company_dict))
	session.commit()
	
	return company_dict
```

## 12.2. Read

Para fazer uma operação read precisamos de uma requisição `GET` à nossa API, então apenas adicione o código abaixo ao final do arquivo `routers/company.py` :

```python
@router.get("/read/{company_name}")
async def company_read(
	company_name: str,
	session: Session = Depends(get_session),
):
	company = company_get(company_name, session)
    
  if not company:
      raise HTTPException(status.HTTP_404_NOT_FOUND, "Company not found")
  
  return company
```

## 12.3. Update

Fazer um update está diretamente ligado à requisições `PUT`, então adicione o código ao arquivo `routers/company.py`:

```python
# código omitido
## adicionar no from sqlalchemy o import: update
from sqlalchemy import select, update

#código omitido

@router.put("/update/{company_name}", status_code=status.HTTP_200_OK)
async def company_update(
    company_name: str,
    company: CompanyRequest,
    session: Session = Depends(get_session),
):
    if not company_exists(company_name, session):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Company not found")
    
    company_data = company.model_dump(exclude_unset=True)

    query = update(Company).where(Company.name == company_name).values(**company_data)

    session.execute(query)
    session.commit()

    return company_data
```

## 12.4 Delete

```python
# código acima omitido

@router.delete("/delete/{company_name}")
async def company_delete(
	company_name: str, 
	session: Session = Depends(get_session),
):
	company = company_get(company_name, session)
	
	if not company:
		raise HTTPException(status.HTTP_404_NOT_FOUND, "Company not found")
		
	session.delete(company)
	session.commit()
	
	return {"message": "Company removed from database"}
```

# 13. Executando

Para executarmos e testar nosso projeto dentro do ambiente com o comando baixo, caso já não esteja rodando desde aprimeira vez que executamos este mesmo comando:

```bash
fastapi dev app/main.py
```

<aside>
💡

Lembre-se de estar também com o ambiente virtual do python ativo, para isso, use o comando baixo para ativar o `venv` antes de chamar o `fastapi`:

```bash
source .venv/bin/activate
```

</aside>

Agora, acesse o endereço indicado no output do `fastapi`, por padrão é o http://127.0.0.1:8000/docs, e acesso a aplicação documentada com o Swagger UI para testar as rotas da sua nova API.
