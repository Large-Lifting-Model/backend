# LLM-backend

This repository is to store any code, README or other files made by the backend team.

Please follow this guide to setup your own Django backend server 
- https://stackpython.medium.com/how-to-start-django-project-with-a-database-postgresql-aaa1d74659d8


# Tech Stack & Tools

## Backend
- Python 3.9+
    - Django
        - Django REST Framework
        - Authentication options:
            - [django-rest-knox](https://jazzband.github.io/django-rest-knox/)
            - [dj-rest-auth](https://dj-rest-auth.readthedocs.io/en/latest/)
        


## Database
- PostgreSQL

## Tools
- Development Tools:
    - [VS Code](https://code.visualstudio.com/)
    - [Git](https://git-scm.com/)
    - [Postman](https://www.postman.com/) 
    - [Django](https://www.djangoproject.com/)
    - [PostgreSQL](https://www.postgresql.org/)
    - [Docker] TBD
    - [GoogleCloud] TBD


# Local Environment Setup
### Django Project Setup
1. Clone this repository
2. Create a virtual environment
    > python -m venv .venv
3. Activate the virtual environment (Windows PowerShell)
    > .venv\Scripts\activate
4. Install the required packages
    > pip install -r requirements.txt


### PostgreSQL Database Setup and Configuration
1. Install PostgreSQL along pgAgent (using Stack Builder),
2. Login in the SQL Shell as superuser (psql) [[1]](https://docs.djangoproject.com/en/4.2/ref/databases/#optimizing-postgresql-s-configuration) [[2]](https://djangocentral.com/using-postgresql-with-django/) and then run the following:
    ```sql
    CREATE DATABASE llm_db;

    <!-- Use this username and password to setup pgadmin4 -->
    CREATE USER userdb WITH PASSWORD 'largeliftingmodel';  

    <!-- Optimizing PostgreSQL's Configuration-->
    ALTER ROLE userdb SET client_encoding TO 'utf8';
    ALTER ROLE userdb SET default_transaction_isolation TO 'read committed';
    ALTER ROLE userdb SET timezone TO 'UTC';

    <!-- GRANT ALL PRIV.. might not be needed if we are changing the owner but I haven't checked -->
    GRANT ALL PRIVILEGES ON DATABASE llm_db TO userdb;
    ALTER DATABASE llm_db OWNER TO userdb;

    <!-- Need to be able to create databases for testing -->
    ALTER USER userdb CREATEDB;
    ```
3. Use or copy the config/config.ini.example file to create a config.ini file in the same directory. Setting this up will allow easier re-configuration
4. Edit the config.ini file to match the database name, user and password created in the previous steps (or copy the below example for now)
    - config.ini:
        ```ini
        [Django]
        SECRET_KEY = 
        DEBUG = True
        ALLOWED_HOSTS = *
        CORS_ALLOW_ALL_ORIGINS = True

        [PostgreSQL]
        DBNAME = llm_db
        HOST = localhost
        PORT = 5432
        USER = userdb
        PASSWORD = largeliftingmodel
        ```

### Django Project Setup Continued
1. Migration
    > python manage.py migrate
2. Run the tests (will be added in the future)
    > python manage.py test
3. Note: Whenever there are changes in the model (i.e. added new fields for a certain model), make sure to run this and then perform step 1:
    > python manage.py makemigrations
4. Run the server
    > python manage.py runserver
5. Visit localhost:8000
    - For now, there shouldn't be anything as it's current unimplemented.
 

## Expected Starting Project Structure

Note: (might not be updated)
```
backend [root]
├── config
│   ├── config example.ini
│   └── config.ini
├── llm-backend
│   ├── backend
│   ├── workout
│   └── manage.py
├── virtualenv [ignored in git]
├── .gitignore
├── README.md
└── requirements.txt
```



## Miscellaneous Notes
1. Django admin panel access
    > python manage.py makesuperuser
- Input email/username/password
2. Apply migrations after each change/pull is made
    > python manage.py makemigrations

    > python manage.py migrate
3. Make sure to git pull and fix any conflicts before committing to your branch, then
    create a pull request and ask someone to review your changes