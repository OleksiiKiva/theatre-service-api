<h1 align="center">🎭 Theatre Service API 🎭</h1>
<h3 align="center">This is API services for booking theater tickets based on DRF</h3>

## 👀 Features

---

* Managing reservations and tickets
* Creating plays with genres and actors
* Creating theatre halls
* Adding performances
* Filtering plays and performances
* JWT authenticated
* Admin panel
* OpenAPI 3 documentation

## 🛢️Technology stack

---

* Backend: Python 3.12, Django 5.04, Django Rest Framework 3.15, PostgreSQL 16.2
* Virtual Environment: venv
* Environment Variables: .env
* Database Migrations: Django Migrations
* Authentication: Django Authentication, JWT
* Configured Throttle Rates
* Dependency Management: pip
* Containerization: Docker
* Collaboration and Version Control: Git, GitHub
* API Documentation: Swagger
* Testing: Unittest

## 🔀 REST API Description

---

* the app is available at: [http://localhost:8000](http://localhost:8000)
* GET /admin/ -- login Django admin panel
* 😎 **user branch**

     method                     | GET                 | POST                                             | PUT                     | PATCH                              
                                                                                                            ---|---|---|---|---
     `/api/user/register/`      | -                   | create new user                                  | -                       | -                                  
     `/api/user/token/`         | -                   | use user credential & get access & refresh token | -                       | -                                  
     `/api/user/token/refresh/` | -                   | use valid refresh token & get access token       | -                       | -                                  
     `/api/user/token/verify/`  | -                   | use token & get valid token status               | -                       | -                                  
     `/api/user/me/`            | get user credential | -                                                | update login & password | particial update login or password 

* ✏️️ **theatre branch**

     method                                  | GET                       | POST                                   | PUT                                       | PATCH                                              | DELETE                                    
                                                                                                            ---|---|---|---|---|---
     `/api/theatre/genres/`                  | get genres list           | create new genre (only admin)          | -                                         | -                                                  | -                                         
     `/api/theatre/genres/<id>/`             | -                         | -                                      | -                                         | -                                                  | -                                         
     `/api/theatre/actors/`                  | get actors list           | create new actor (only admin)        | -                                         | -                                                  | -                                         
     `/api/theatre/actors/<id>/`             | -                         | -                                      | -                                         | -                                                  | -                                         
     `/api/theatre/plays/`                   | get plays list            | create new play (only admin)         | -                                         | -                                                  | -                                         
     `/api/theatre/plays/<id>/`              | get play **pk=id**        | -                                      | -                                         | -                                                  | -                                         
     `/api/theatre/plays/<id>/upload-image/` | -                         | upload image                        | -                                         | -                                                  | -                                         
     `/api/theatre/theatrehalls/`            | get theatre halls list    | create new theatre hall (only admin) | -                                         | -                                                  | -                                         
     `/api/theatre/theatrehalls/<id>/`       | -                         | -                                      | -                                         | -                                                  | -                                         
     `/api/theatre/performances/`            | get performances list     | create new performance (only admin)  | -                                         | -                                                  | -                                         
     `/api/theatre/performances/<id>/`       | get performance **pk=id** | -                                      | update performance **pk=id** (only admin) | partital update performance **pk=id** (only admin) | delete performance **pk=id** (only admin) 
     `/api/theatre/reservations/`            | get reservations list     | create new reservation               | -                                         | -                                                  | -                                         
     `/api/theatre/reservations/<id>/`       | -                         | -                                      | -                                         | -                                                  | -                                         

* 🗂️ **doc branch**
    - GET `/api/schema/` -- download .yaml file
    - GET `/api/doc/swagger/` -- API documentation on SwaggerUI
    - GET `/api/doc/redoc/` -- API documentation on ReDoc

## 🚀 Install using GitHub

---

1. Install Python
1. Create PostgresSQL db
1. Clone the repo
   ```commandline
   git clone https://github.com/OleksiiKiva/theatre-service-api.git
   ```
1. Open the project folder in your IDE
1. Open the project terminal folder. Create & activate venv
   ```commandline
   python -m venv venv
   venv\Scripts\activate (on Windows)
   source venv/bin/activate (on Linux/MacOS)
   ```
1. Install all requirements
   ```commandline
   pip install -r requirements.txt
   ```
1. Rename `.env.sample` file as `.env`. Add the environment variables to `.env` file as `KEY=VALUE` pair
   ```
   SECRET_KEY=<your secret key>
   POSTGRES_USER=<your db username>
   POSTGRES_PASSWORD=<your db user password>
   POSTGRES_DB=theatre
   POSTGRES_HOST=db
   POSTGRES_PORT=5432
   PGDATA=/var/lib/postgresql/data
   ```
    - generate `SECRET_KEY`. Use Python shell `python3 manage.py shell` follow
      commands:
      ```commandline 
      from django.core.management.utils import get_random_secret_key
      print(get_random_secret_key())
      ```
    - copy paste `SECRET_KEY` value to `.env` file
1. Apply migrations & update the database schema
   ```commandline
   python manage.py migrate
   ```
1. Start development server
   ```commandline
   python manage.py runserver
   ```

## 🔑 Credentials

---

1. Use the following command to load prepared data from fixture for a quick test
    ```
    python manage.py loaddata theatre_service_db_data.json
    ```
    - credentials for this fixture: Admin login: `admin@site.com`. Admin password: `Admin-12345`. Users
      password: `User-12345`
1. Or create a superuser and populate the db yourself

## 🔐 How to Obtain JSON Web Token (JWT)

---

To get access protected endpoints you need to obtain a JWT by authenticating as a user or admin.
Follow these steps to get your JWT token:

1. Create user via /api/user/register/
1. Use user credentials obtain `access_token` & `refresh_token` via /api/user/token/
1. Include `access_token` in the `Authorization` header of your requests to protected API endpoints
1. If `access_token` expires, you can use `refresh_token` to obtain a new one

## 🐋 Run with docker

---

1. Install Docker
1. Use next commands to
    - building containers
     ```
     docker-compose build
     ```
    - run containers
     ```
     docker-compose up
     ```
    - stop containers
     ```
     docker-compose stop
     ```
    - destroy containers
     ```
     docker-compose down
     ```

## 📧 Contacts

---

Please send bug reports and suggestions by email:
[oleksii.kiva@gmail.com](mailto:oleksii.kiva@gmail.com)
