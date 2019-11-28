# innovaccer-summergeeks-2020
REST API of SDE Intern Assignment Project for Innovaccer SummerGeeks 2020

<br>

## Tech Stack
- Django
- PostgreSQL
- Amazon Web Services (AWS)

<br>

## Steps for Local Deployment
- Install `python3` and `python3-pip` on your local machine.
- Install `postgresql` on your local machine and create a new user (authenticated with password) and a new database.
- Get SMTP properties of an email address with which you'll be sending emails.
- Create a file at project's root directory named `config.json`, and copy-paste the following content in it:
  ```json
  {
    "SECRET_KEY": "<application-secret-key>",
    "DB_ENGINE": "django.db.backends.postgresql_psycopg2",
    "DB_NAME": "<database-name>",
    "DB_USER": "<database-user>",
    "DB_PASSWORD": "<database-password>",
    "DB_HOST": "<database-host>",
    "DB_PORT": 5432,
    "EMAIL_HOST": "<smtp-host>",
    "EMAIL_PORT": 587,
    "EMAIL_HOST_USER": "<smtp-username>",
    "EMAIL_HOST_PASSWORD": "<smtp-password>",
    "EMAIL_USE_TLS": true
  }
  ```
- Get your AWS credentials and store them in the file `~/.aws/credentials`. Make sure, you subscribed to SNS services in `ap-southeast-1` region.
- Run following set of commands to create a virtual environment, install required dependencies and migrate your models to database:
  ```shell
  sudo apt install -y libpq-dev python3-dev virtualenv
  virtualenv -p python3 env
  source env/bin/activate
  pip install -r requirements.txt
  python manage.py makemigrations innovaccer entry_mgmt
  python manage.py migrate
  ```
- Now, your local development environment is set. To run the server, type `python manage.py runserver`. By default, the server will start on port 8000.

<br>

## REST API Documentation

- POST `~/entry/check_in/`

  Request Body
  ```json
  {
    "host": {
      "name": "<host-name>",
      "email": "<host-email-address>",
      "phone_number": "<host-phone-number>",
      "address": "<host-address>"
    },
    "visitor": {
      "name": "<visitor-name>",
      "email": "<visitor-email-address>",
      "phone_number": "<visitor-phone-number>"
    }
  }
  ```
  
    Expected Response Codes
    - <b>201</b> : Visitor checked in successfully
    - <b>400</b> : Possible Reasons:
      - Visitor with given phone number already registered
        ```json
        {
          "duplicate": "visitor/phone_number"
        }
        ```
      - Invalid email or phone number formats
      - Not all fields were present in the request body object
    - <b>500</b> : Internal server error, something went wrong on server-side

- POST `~/entry/check_out/`

  Request Body
  ```json
  {
    "phone_number": "<visitor-phone-number>"
  }
  ```
  
  Expected Response Codes
  - <b>200</b> : Visitor checked out successfully
  - <b>400</b> : Possible Reasons:
    - Invalid phone number format
    - Not all fields were present in the request body object
  - <b>404</b> : No visitor with given phone number checked in
  - <b>500</b> : Internal server error, something went wrong on server-side
