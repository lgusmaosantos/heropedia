# Heropedia
A base de dados de heróis mais completa de todos os universos possíveis. Desafio para admissão como desenvolvedor web Pl/Sr da Softfocus.

### Requerimentos
Python 3.6.9 ou superior
PostgreSQL 10 ou superior
Nome de usuário e senha de um perfil PostgreSQL com permissão para criar e possuir um banco de dados

### Instalação (Linux)
Crie um banco de dados PostgreSQL usando os dados do usuário definido em Requerimentos. Guarde o nome do banco de dados criado.

Abra a pasta do projeto em linha de comando. Instale e ative um ambiente virtual Python 3:

`python3 -m venv venv`

`source ./venv/bin/activate`

Instale no ambiente virtual ativo as dependências do projeto:

`pip install -r requirements.txt`

Na subpasta `heropedia/heropedia`, onde está presente o arquivo `settings.py`, crie um arquivo com o nome `db_settings.py` e o preencha como abaixo:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'heropedia',
        'USER': 'django',
        'PASSWORD': 'senhaboa',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
```
Substitua os valores de `NAME`, `USER` e `PASSWORD` para o nome do banco de dados criado, nome de usuário e senha do perfil PostgreSQL. Se você estiver usando uma instância do PostgreSQL em outro host e/ou porta, certifique-se de alterar os valores de `HOST` e `PORT` de acordo.

Volte à raiz do projeto (`heropedia`) na linha de comando. Gere e aplique as migrações de banco de dados do projeto:

`./manage.py makemigrations`

`./manage.py migrate`

Crie um superusuário da aplicação. Este passo é opcional, mas recomendado pois algumas funções do projeto (criação, edição e exclusão, por exemplo) requerem um usuário autenticado para executar:

`./manage.py createsuperuser`

Agora se pode executar a aplicação:

`./manage.py runserver`

Por padrão, o Django usa a porta 8000 para operar. Caso precise usar outra porta, faça como abaixo:

`./manage.py runserver <PORTA_DESEJADA>` (sem os <>)

Por fim, vá ao seu navegador web e digite o endereço abaixo para usar a aplicação:

`http://localhost:8000`

Para acessar o painel administrativo da aplicação, visite:

`http://localhost:8000/admin`
