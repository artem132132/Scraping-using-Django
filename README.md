# Trip Scrap Django

- This is a web scraping project using Django, Django rest framework, BeautifulSoap and Selenium.
- It can automatically search any city, scrap the hotel info and store the info in a database table

## Run Localy

- Setup a virtual environment (Showing for windows)

```bash
py -m venv env_name
Scripts\activate.bat
```

- Clone from git

```bash
git clone git@github.com:Sym-17/trip_scrap_django.git
cd trip_scrap
```

- Install all dependencies and run

```bash
pip install -r requirements.txt
py manage.py runserver
```

This will open a server at: http://127.0.0.1:8000/

## Set up database and migrate

- Go to `trip_scrap\settings.py`
- Change the default database connection
- Migrate the model of `hotel` app by the following command. These will create a table named `hotel_hotel_info` into the database

```bash
py manage.py makemigrations hotel
py manage.py migrate
```

## URL

Here a list of urls for the project:

- Home page: http://127.0.0.1:8000/
- Inserting data by scraping: http://127.0.0.1:8000/hotel/insert-data
- Show all data from database: http://127.0.0.1:8000/hotel/show-all
- Show all data from database using DRF: http://127.0.0.1:8000/hotel/show-all-drf
- Show all data from database page by page using DRF: http://127.0.0.1:8000/hotel/show-all-drf-page
- Post a new data: http://127.0.0.1:8000/hotel/post-data
- See details, edit and delete according to id: http://127.0.0.1:8000/hotel/details/1
  (Change ID as your wish)
- Django Admin Page:
  http://127.0.0.1:8000/admin
  _(Create a superuser first)_
