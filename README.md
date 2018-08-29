# opendatapdx

## Once you have Python 3 installed:
### Create a new virtual environment, and switch to it:
`
python3 -m venv <your-envs-dir>/opendatapdx
source <your-envs-dir>/opendatapdx/bin/activate
`

### Install the dependencies for the project:
`
pip -r install requirements.txt
`

### Setup the database and start the application locally:
`
python manage.py migrate
python manage.py runserver
`
