#!/bin/sh
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete
find . -path "*.sqlite3" -delete
python3 manage.py makemigrations
python3 manage.py migrate
