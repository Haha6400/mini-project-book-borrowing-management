# README

## Setting up your own project

### Check out your branch

`git checkout -b <your-branch-name>`

### Install dependencies

api
```bash
  docker-compose run --rm api poetry install
```

web
```bash
  docker-compose run --rm web npm install
```

then, run `docker-compose up`

### Access

**web**: http://localhost:3000/

**pgAdmin**: http://localhost:5000/

Setup database

  1. Login pgAdmin with:
    username: admin@admin.com
    password: admin

  2. Click on Add New Server and fill out with following info:

    - General:
      Name: <your-db-connection-name>

    - Connection:
      Host name/address: db
      Port: 5432
      Username: postgres
      Password: postgres

  3. Once connection is setup, click on Object, then Create, then Database with following information:
    - General:
      Database: <your-db-name>

  4. Open Tools, then Query Tool
  - Make sure the opened Query Tool's tab title <your-db-name> in it
  - Create a table name user with columns specified in `api/models/users.py`

**api**: http://localhost:8000/

Setup connection between your api and db

  1. Open `api/models/__init__.py`

  2. Replace `DATABASE`'s value with <your-db-name>

  3. Play with the api at http://localhost:8000/docs#/

It's recommended to use SERIAL for primary key
https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-serial/

## TODO

- [ ] add eslint and pylint
- [ ] add migration
- [ ] add RECOMMENDED_RESOURCES.md
- [ ] add automated upgrade