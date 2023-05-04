
# Getting started:
This document describes how to install and run the [frontend application](https://oafdev1.westus2.cloudapp.azure.com/) of Omega Assertion Framework(OAF) on your local machine for development and testing purposes. 


1. Generate an .env file using [.env-template](https://github.com/ossf/alpha-omega/blob/scovetta/oaffe/omega/oaf/frontend/.env-template) as reference.
    1. Generate secret key using ```python -c "import secrets; print(secrets.token_hex(64))"``` and add it to the .env file.
    2. Set the ```STATIC_ROOT="/path/to/your/alpha-omega/omega/oaf/frontend/oaffe/static"```
    3. Set the ```DATABASE_HOST='localhost'```

2. Download [Postgres](https://www.postgresql.org/download/) and configure the database.
    1. To log in to the database: ```sudo -i -u postgres```
    2. To call postgres from the terminal: ```psql```
    3. Create database, user and assign privileges
    ```
    CREATE DATABASE triage;
    CREATE USER triage_user WITH PASSWORD ‘triage_password’;
    GRANT ALL PRIVILEGES ON DATABASE triage TO triage_user;
    ```
    4. Create schema after connecting to db as triage_user, assign privileges: 
    ```
    CREATE SCHEMA schema;
    GRANT CREATE ON SCHEMA schema TO triage_user;
    ```

> ### Troubleshooting: 
When the database gets created, the database owner gets assigned to the original hostname (johndoe), you can verify this using ```\l```
| Name    |  Owner   | Encoding |   Collate   |    Ctype    | ICU Locale | Locale Provider |   Access privileges  | 
|-----------|----------|----------|-------------|-------------|------------|-----------------|----------------------|
| triage    | johndoe    | UTF8     | en_US.UTF-8 | en_US.UTF-8 | en-US      | icu             | =Tc/johndoe       |                                                                                                                     

Change the owner of the db to triage_user: ```ALTER DATABASE triage OWNER TO triage_user;```


3. Set up and activate the virtual environment in the alpha-omega project root folder: 
    1. Initialize the Python virtual environment : ```python -m venv venv```
    2. Activate the virtual environment: ```source venv/bin/activate```
    3. Install the requirements:  
```
pip install -r requirements.txt
pip install -r dev-requirements.txt
pip install -r frontend/requirements.txt
```
4. Install frontend project dependencies in package.json: 
```
cd frontend
yarn install
```
5. Run database migrations: 
```python manage.py migrate``` <br>
This creates database tables for the project and applies migrations.
6. Start the django development server 
```python manage.py runserver``` <br>

You can now navigate to ```localhost:8000``` in the web browser to view the project
