#!/bin/bash

DB_FILE=osCam/db.sqlite3
EMAIL_FILE=.env
SETUP="GOOD"

# Function to prompt user to enter email credentials
setup_email(){

    SETUP="GOOD"
    if [[ ! -f "$EMAIL_FILE" ]]; then
      echo "Would you like to configure your email settings before starting the app?"
      read -p '[Y/N]: ' CONTINUE
    else
        break
    fi

    # If the user wants to configure collect their information and format the env file
    if [[ "$CONTINUE" = "Y" ]]; then
      read -p "Email Address: " EMAIL
      read -p "Secret key: " SECRET_KEY

      printf "EMAIL_HOST=smtp.gmail.com\n" > .env
      printf "EMAIL_HOST_USER=$EMAIL\n" >> .env
      printf "EMAIL_HOST_PASSWORD=$SECRET_KEY\n" >> .env
      printf "RECIPIENT_ADDRESS=$EMAIL\n" >> .env

    # Else just continue booting the server as normal
    elif [[ "$CONTINUE" = "N" ]]; then
      break
    else
      echo "Invalid character. Exiting"
      SETUP="INVALID"
    fi
}


# If the database file does not exist, install requirements, migrate, and create user
if [[ ! -f "$DB_FILE" ]]; then
    echo "Running setup..."
    pip install -r oscam/requirements.txt
    cd osCam/
    ./clear_models.sh

    while true;
    do
      setup_email

      if [[ "$SETUP" == "GOOD" ]]; then
        break
      fi
    done

    python manage.py createsuperuser
    cd ..

else

    while true;
    do
      setup_email

      if [[ "$SETUP" == "GOOD" ]]; then
        break
      fi
    done
fi

echo "Starting Open-Source Security Camera..."
echo "Go to http://127.0.0.1:8000/ to view your dashboard"
echo "Type Ctrl-C to exit"
sleep 3

python motiondetect.py &
cd osCam/
python3 manage.py runserver
