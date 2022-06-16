### Flat.mx Test


API to manage Properties, Categories and Users 🍃

To start the project justo cline the repository and run:
```docker-compose up```

You must have a .env file with the next variables:
```
DB_USER
DB_PASSWORD
DB_HOST
DB_NAME
API_USER
API_PASSWORD
```

Then you can see it in your  [localhost](https://127.0.0.1/5000)


The API routes are:
| Route | Methods |
| ------ | ------ |
| /users | GET |
| /api/properties | GET/POST/PUT/DELETE |
| /api/categories | GET/POST/PUT/DELETE |

Yot have to use basic auth with the same credetials as *API_USER* and *API_PASSWORD*


**Have fun!**
