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
