# Django API

This is a very basic Django API.

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
curl -H "Authorization: JWT <your_token>" \
        http://localhost:8000/api/v1/reviews/
```

### Create review
```bash
curl -H "Authorization: JWT <your_token>" \
        --request POST \
        --url http://localhost:8000/api/v1/reviews/ \
        --header 'content-type: application/json' \
        --data '{"rating": 5, "title": "This is Pokemon title", "summary": "This is not a summary....", "company": "The Pokemon Company"}'
````
