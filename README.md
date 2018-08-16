# Django API

This is a very basic Django API.

## Set up Project
### Virtual Environment
This project uses Python 3.7. In addition, creating a 
[virtual environment][venv] is suggested in order to avoid
conflicts with dependencies in other projects or to keep clean your main
Python interpreter.


### Installing dependencies
This project uses [`poetry`][poetry] in order to keep track of the dependencies.
After cloning the repository you can run the following command in order to
install the dependencies of this project:

```bash
poetry install
```

### Run Migrations
This is project uses Django, so it is important to run the migrations:

```bash
python manage.py migrate
```

### Run Server
In order to start the server, run the following command:

```bash
python manage.py runserver
```

## Usage
### Obtain a token
````bash
curl --request POST \
        --url http://localhost:8000/api/v1/auth-jwt/ \
        --header 'content-type: application/json' \
        --data '{"username": "m", "password": "proyectoepika"}'
        
        
curl --request POST \
        --url http://localhost:8000/api/v1/auth-jwt/ \
        --header 'content-type: application/json' \
        --data '{"username": "pikachu", "password": "pokemonpower"}'
````

### Request reviews
```bash
curl -H "Authorization: JWT  <your_token>" \
        http://localhost:8000/api/v1/reviews/
```

### Create review
```bash
curl -H "Authorization: JWT  <your_token>" \
        --request POST \
        --url http://localhost:8000/api/v1/reviews/ \
        --header 'content-type: application/json' \
        --data '{"rating": 5, "title": "This is a Pokemon title", "summary": "This is the summary ...", "company": "The Pokemon Company"}'
````

[poetry]: https://poetry.eustace.io/
[venv]: https://docs.python.org/3/library/venv.html
