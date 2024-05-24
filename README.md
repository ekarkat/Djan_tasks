## A task manager APP made with Django
# DjanTask Manager

## Description

This is a simple Django application that manage tasks

## Installation

1. Clone this repository:

    ```
    git clone git@github.com:ekarkat/Djan_tasks.git
    ```

2. Navigate to the project directory:

    ```
    cd Djan_tasks
    ```

3. Create a virtual environment (optional but recommended):

    ```
    python3 -m venv venv
    ```

4. Activate the virtual environment:

    - On macOS and Linux:

    ```
    source venv/bin/activate
    ```

5. Install the dependencies and setup the database:

    ```
    pip3 install -r requirements.txt
    ```
    Create Postgres database and user
    ```
    CREATE DATABASE djantask_db;
    CREATE USER djantask_user WITH PASSWORD 'djan_admin';
    GRANT ALL PRIVILEGES ON DATABASE djantask_db TO djantask_user;
    ```

6. Run the Django application:

    ```
    ./manage.py runserver
    ```

7. Open your web browser and go to `http://127.0.0.1/8000` to see the application running.

## ENJOY