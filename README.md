# OpenDataPDX

## About
This is the web application for our OpenDataPDX capstone project. 
If you're not familiar with Django, a good introduction is here: https://docs.djangoproject.com/en/2.1/intro/overview/

A bit about the structure of this Django app:
A Django app is composed of various hierarchical sub-apps.
For this app, opendatapdx/ is the root sub-app, which is the "core" of the app. It defines the overall settings, and requests are first sent here, and then the URL dispatcher decides where to send it (e.g., which sub-app, view etc).
cataloger/ is the sub-app which will contain most of our work. urls.py will deicde which view in views.py to send a request to, and it only depends on what the url is. 

## Technologies used:
+ Python 3.6
+ Django & Postgres
+ Heroku
+ Docker-compose

## Steps for local development (Linux):
1. Install git and brush up on how to use it if you're not familiar. A good intro is here: https://guides.github.com/introduction/git-handbook/#basic-git
2. Clone this repository: `git clone https://github.com/AustenHolmberg/opendatapdx.git`
3. Change to the directory: `cd opendatapdx`
4. Add a remote url for the heroku app `git remote add heroku https://git.heroku.com/opendatapdx.git`
5. Install docker-compose:

`
sudo curl -L https://github.com/docker/compose/releases/download/1.22.0/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
`

`
sudo chmod +x /usr/local/bin/docker-compose
`

6. Build the images for the DB and the application:

`
docker-compose build
`

7. Run the images using docker (launches the application locally, go to http://0.0.0.0:8000/ to access).
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
