# PMSB

Descrição do projeto ...

## Como Instalar

Primeiro certifique-se de ter instalado Python3 e GIT na sua maquina.

### Instale as dependencias do projeto usando pip

Crie uma copia do arquivo env.exemplo e modifique os valores das variaveis
 de ambiente. Depois execute com os comandos a saguir. 

`pip install -r requirements.txt`


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

* conta
* core
* pinax
* questionarios
* relatorios


## Documentação API Rest
Para ter acesso a documentação da API REST o sistema deve estar com a flag DEBUG=True.
Para visualizar a documentação visite a url http://127.0.0.1:8000/pmsb/docs/api/swagger.
