#!/bin/bash

DB_FILE=osCam/db.sqlite3

# If the database file does not exist, install requirements, migrate, and create user
if [[ ! -f "$DB_FILE" ]]; then
    echo "Running setup..."
    pip install -r oscam/requirements.txt
    cd osCam/
    ./clear_models.sh

    python manage.py createsuperuser
    cd ..
fi

echo "Starting Open-Source Security Camera..."
echo "Go to http://127.0.0.1:8000/ to view your dashboard"
echo "Type Ctrl-C to exit"
sleep 3

python motiondetect.py &
cd osCam/
python3 manage.py runserver
