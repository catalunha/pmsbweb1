# PMSB

Descrição do projeto ...

## Como Instalar

Primeiro certifique-se de ter instalado Python3 e GIT na sua maquina.

### Instale as dependencias do projeto usando pip

Sempre instale dependencias atravez do arquivo de dependencias.

`pip install -r requirements_server.txt`


Apos instalar entre na pasta `pmsb_web`.

`cd pmsb_web`

### Configure o Ambiente

Crie um arquivo `.env` e copie o conteudo do arquivo `.env.exemplo` para o arquivo `.env`.

Modifique a linha do banco de dados baseado na documentação da biblioteca [dj-database-url](https://github.com/kennethreitz/dj-database-url):

`DATABASE_URL=postgres://pmsb_db_user:pmsb_db_pass@127.0.0.1:5433/pmsb_db`

### Aplique as Migrações

`python manage.py migrate`

### Crie Um Super Usuario

`python manage.py createsuperuser`

### Inicie o Servidor de Desenvolvimento

`python manage.py runserver`


## APPS

questionarios