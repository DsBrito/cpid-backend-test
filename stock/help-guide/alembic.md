Caso precise de ajuda para Inicializar o projeto:

certifique de ter o 'alembic' na máquina.

olhe o env.py neste diretório, certifique que esteja com ele nesse estado.

```bash
rm -r alembic/

```


```bash
alembic init alembic
```


```bash
alembic revision --autogenerate -m "initial"
```

```bash
alembic upgrade head
```

```bash
fastapi dev app/main.py
```

A versão de migrate (para ultimo caso) esta presente nesse diretório

---

# Guia do mini-curso

# 10. Alembic

Para facilitar a criação da tabela `company` no banco de dados, vamos utilizar a biblioteca Alembic que utiliza o conceito de migrations para criar tabelas em um banco de dados.

## 10.1 Instalação

Primeiro, instale e inicie a biblioteca no diretório raiz da aplicação:

```bash
# ~/raiz$
pip install alembic
alembic init alembic
```

## 10.2 Configuração

Agora passando para as configurações do Alembic, lembra quando eu disse que uma model é uma representação de uma tabela do banco de dados como uma classe Python? Então, nós podemos fazer o caminho contrário, utilizar uma model para criar uma tabela usando o Alembic. Para isso, precisamos dizer à biblioteca onde estão nossas models e em qual banco ela deve criar isso.

Altere o arquivo `env.py` para incluir as configurações necessárias.

```python
# ~/stock/alembic/env.py

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

from app.models import tables
target_metadata = tables.Base.metadata

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
