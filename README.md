# OpenDataPDX

## Steps for local development (Linux):
1. Install git
2. Clone this repository: git clone https://github.com/AustenHolmberg/opendatapdx.git
3. Install docker-compose:

`
sudo curl -L https://github.com/docker/compose/releases/download/1.22.0/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
`

`
sudo chmod +x /usr/local/bin/docker-compose
`

4. Build the images for the DB and the application:

`
docker-compose build
`

5. Run the images using docker (launches the application locally, go to http://0.0.0.0:8000/ to access).
Note: after building, you only need to run docker-compose up from now on to test the application.

`
docker-compose up
`

#### To push your changes to this repo (development):

`
master: git push
specify a brach: git push origin <branch-name>
`


## To push your changes to the app on Heroku (production):

`
git push heroku master
`

#### The app on Heroku is accessible at: https://opendatapdx.herokuapp.com/
