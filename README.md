# My Favorite Books REST API

Implements an simple API server to keep track of user's favorite books performing CRUD operations. It uses JWT tokens
for user's authentication. The token is expired after 24 hours and a new token is granted.

**IT uses PostgreSQL as its database.** Make sure its installed and configured properly on the system.



## Get JWT authorization token.

Returns JWT authorization token used for accessing protected routes and resources.

**To access all of the following resource routes, JWT token must be present in Authorization header.**

- **ROUTE:** `/auth/`
- **METHODS:**: `GET` | `POST`
- **RESPONSE:**:
    - **STATUS CODE:** 200 OK
    - **JSON BODY:**
```json
{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1ODY3MTk0MzV9.5oUkAvJJrtvvfbg2t2zNLJrHpBbGlsUe70VlCDDmWC4"
}
```



## Insert book.

Insert a new book into the database if it doesn't exists.

- **ROUTE:** `/books/insert/`
- **METHODS:** `POST`
- **REQUIRED JSON KEYS:** `title`, `amazon_url`, `author`, `genre`
- **EXAMPLE REQUEST JSON BODY:**
```json

{
    "title": "Sarojini's Mother",
    "amazon_url": "https://www.amazon.in/Sarojinis-Mother-Kunal-Basu-ebook/dp/B0842TPQKC/",
    "author": "Kunal Basu",
    "genre": "Fiction"
}

```
- **RESPONSE:**
    - **STATUS CODE:** 200 OK



## Get single book.

Get details of single book from the API.

- **ROUTE:** `/books/get/`
- **METHODS:** `GET` | `POST`
- **REQUIRED JSON KEYS:** `title`
- **EXAMPLE REQUEST JSON BODY:**
```json

{
    "title": "Harry Potter and the Sorcerer's Stone"
}

```
- **RESPONSE:**
    - **STATUS CODE:** 200 OK
    - **JSON BODY:**
 ```json

{
    "title": "Harry Potter and the Sorcerer's Stone",
    "amazon_url": "https://www.amazon.com/dp/059035342X/",
    "author": "J.K. Rowling",
    "genre": "Fantasy"
}
  
```



## Get all books.

Returns JSON list of all user's favorite books.

- **ROUTE:** `/books/`
- **METHODS:** `GET` | `POST`
- **RESPONSE:**
    - **STATUS CODE:** 200 OK
    - **JSON BODY:**
```json

 [
      {
        "amazon_url": "",
        "author": "",
        "genre": "",
        "title": ""
      },
      {
        "amazon_url": "",
        "author": "",
        "genre": "",
        "title": ""
      }   
 ]

```


   - **STATUS CODE:** 409 CONFLICT

```json

{"message": "Book already exists."}

```



## Update book details.

Update various fields of the book. Pass any JSON keys with values to `update` key which needs to be updated. 

- **ROUTE:** `/books/update/`
- **METHODS:** `PUT`
- **REQUIRED JSON KEYS:** `title`, `update`
- **EXAMPLE REQUEST JSON BODY:**
```json


{
    "title": "Chats with the Dead",
    "update": {
        "genre": "Literature and Fiction"    
    }
}

```
- **RESPONSE:**
    - **STATUS CODE:** 200 OK
    
    
    
## Delete book.

Delete the book from the database.

- **ROUTE:** `/books/delete/`
- **METHODS:** `DELETE`
- **REQUIRED JSON KEYS:** `title`
- **EXAMPLE REQUEST JSON BODY:**
```json
{
    "title": "Amnesty"
}
```
- **RESPONSE:**
    - **STATUS CODE:** 200 OK
    
    
    
## Error codes.

- **301 Redirect**

Redirects to `/auth/` if JWT token is expired.


- **400 Client Error**

    - Returns when the HTTP body is not of `application/json` mime type.
```json
{"message": "Invalid JSON body."}
```

- Returns when any of the required keys from JSON object is missing along with the missing keys.
    
```json
{
    "message": "Missing required keys for book entry.",
    "missing_keys": []    
}
```


- **401 Unauthorized**
    
- Returns when JWT token is not present in the authorization header.
    
```json
{"message": "Unauthorized"}
```
- Returns when an improper JWT token has been passed.

```json
{"message": "Invalid JWT Authorization Token"}
```

- Returns when the JWT token has cannot be decoded using server's verified signature.
```json
{"message": "Can't decode JWT Authorization Token"}
```


- **404 Not Found**

Returns when `title` is required key in request JSON body and no book is found with the same title.

```json
    {"message": "Book with title 'title' doesn't exists."}
```
