# Steps for local development (Linux):
1. Install docker-compose:

`
sudo curl -L https://github.com/docker/compose/releases/download/1.22.0/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
`

`
sudo chmod +x /usr/local/bin/docker-compose
`

2. Build the images for the DB and the application:

`
docker-compose build
`

3. Run the images using docker (launches the application locally, go to http://0.0.0.0:8000/ to access).
Note: after building, you only need to run docker-compose up from now on to test the application.

`
docker-compose up
`
