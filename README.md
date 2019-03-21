# PMSB

Descrição do projeto ...

## Como Instalar

Somente python3 e Djando2

### Instale as dependencias do projeto usando pip

Crie uma copia do arquivo env.exemplo e modifique os valores das variaveis
 de ambiente. Depois execute com os comandos a saguir. 

`pip install -r requirements.txt`

`cd pmsb_web`


### Aplique as migrações

`python manage.py migrate`

### Crie um super usuario

`python manage.py createsuperuser`

### Inicie o servidor de desenvolvimento

`python manage.py runserver`


## APPS

questionarios


## Documentação API Rest
Para ter acesso a documentação da API REST o sistema deve estar com a flag DEBUG=True.
Para visualizar a documentação visite a url http://127.0.0.1:8000/pmsb/docs/api/swagger.