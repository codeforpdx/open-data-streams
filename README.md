# OpenDataPDX

## About
This is the web application for our OpenDataPDX capstone project.

## Technologies used:
+ Python 3.6
+ Django & Postgres
+ Heroku
+ Docker-compose

## Steps for local development (Linux):
1. Install git and brush up on how to use it if you're not familiar. A good intro is here: https://guides.github.com/introduction/git-handbook/#basic-git
2. Clone this repository: `git clone https://github.com/AustenHolmberg/opendatapdx.git`
3. Add a remote url for the heroku app `git remote add heroku https://git.heroku.com/opendatapdx.git`
4. Install docker-compose:

`
sudo curl -L https://github.com/docker/compose/releases/download/1.22.0/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
`

`
sudo chmod +x /usr/local/bin/docker-compose
`

5. Build the images for the DB and the application:

`
docker-compose build
`

6. Run the images using docker (launches the application locally, go to http://0.0.0.0:8000/ to access).
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
