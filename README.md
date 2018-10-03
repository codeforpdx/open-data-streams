# OpenDataPDX

## About
This is the web application for our OpenDataPDX capstone project. 
If you're not familiar with Django, a good introduction is here: https://docs.djangoproject.com/en/2.1/intro/overview/

A Django app is composed of various hierarchical sub-apps.
For this app, opendatapdx/ is the root sub-app, which is the "core" of the app. It defines the overall settings, and requests are first sent here, and then the URL dispatcher decides where to send it (e.g., which sub-app, view etc). The views render a template (html file with variables), to the user's screen. Our app currently has one page (template at cataloger/templates/index.html), which is the home page.

cataloger/ is the sub-app which will contain most of our work. urls.py will decide which view in views.py to send a request to, and it only depends on what the url is. 

## Technologies used:
+ Python 3.6
+ Django & Postgres
+ Heroku
+ Docker & Docker-compose

## Steps for local development (for Linux; using other plaforms might require a different setup process for Git or Docker-compose):
1. Install Git and brush up on how to use it if you're not familiar. A good intro is here: https://guides.github.com/introduction/git-handbook/#basic-git
2. Clone this repository: `git clone https://github.com/AustenHolmberg/opendatapdx.git`
3. Change to the directory: `cd opendatapdx`
4. Add a remote url for the heroku app `git remote add heroku https://git.heroku.com/opendatapdx.git`
5. Install docker community edition (for ubuntu, setups for other platforms are available): https://docs.docker.com/install/linux/docker-ce/ubuntu/
6. Install docker-compose:

`
sudo curl -L https://github.com/docker/compose/releases/download/1.22.0/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
`

`
sudo chmod +x /usr/local/bin/docker-compose
`

7. Build the images for the DB and the application:

`
docker-compose build
`

8. Run the images using docker (launches the application locally, go to http://localhost:8000/ to access).
Note: after building, you only need to run docker-compose up from now on to test the application.

`
docker-compose up
`

#### To push your changes to this repo (development):

To master:
`
git push
`

Or, specify a branch:
`
git push origin <branch-name>
`

## To push your changes to the app on Heroku (production):

`
git push heroku master
`

#### The app on Heroku is accessible at: https://opendatapdx.herokuapp.com/

## Working with the database/models:
You'll likely need to make changes to the DB models at some point.
This involves: 
1. Making your modifications (adding/removing a model, adding/removing fields to an existing model, etc) to the models at cataloger/models.py.
2. Running makemigrations to create a new migration file (will be added to cataloger/migrations/):
`
docker-compose run web pipenv run python3 manage.py makemigrations --settings=opendatapdx.local_settings
`
3. Running migrate to have Django execute the migration:
`
docker-compose run web pipenv run python3 manage.py migrate --settings=opendatapdx.local_settings
`
In order for others to use your migration, you'll need to commit and push the new migration file.

#### Querying the database directly
Run:
`
docker-compose run web pipenv run python3 manage.py shell --settings=opendatapdx.local_settings
`
This will give you a Python shell with live ORM access to your local DB, allowing you to read and write to the DB, test queries, etc.
For example, to get all of the current users (their Profile objects):
```python
>>> from cataloger.models import *        
>>> Profile.objects.all()                 
<QuerySet [<Profile: Profile object (1)>]>
```
Getting the first user's email:
```python
>>> some_user = Profile.objects.first()
>>> some_user.email
>>> 'test@comcast.net'
```

#### Resetting your database (nuke)
Instructions here: http://docs.metasfresh.org/installation_collection/EN/How_do_I_reset_database_using_docker.html
(basically, `docker stop opendatapdx_db_1`, `docker rm opendatapdx_db_1`)

#### Migrating the database on Heroku
`heroku run python manage.py migrate`
