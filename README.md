# COLLECTIFY - API
A rest API written with django and rest framework: https://www.django-rest-framework.org/tutorial/1-serialization/ .

## INSTALLATION

### Python
Download and install python3.9 from https://www.python.org/downloads/.

### Pipenv
After python installation, run in your terminal:
```
pip install pipenv
```

Then in root folder of the project:

#### Create a virtual environment using python3
```
pipenv --three 
```

#### Connect to your new virtual environment
```
pipenv shell
```

#### Install requirements into a Pipfile and Pipfile.lock
```
pipenv install -r requirements.txt
pipenv lock
```

#### Install requirements from Pipfile to your virtual environment
```
pipenv install
```

#### Exit the virtual environment
```
exit
```

### Virtualenv wrapper (deprecated, skip these steps if using pipenv)
After python installation, run in your terminal:
```
pip install virtualenv
pip install virtualenvwrapper
```
And add these lines in ~/.bashrc:
```
# Virtualenvwrapper
export VIRTUALENVWRAPPER_PYTHON="/usr/local/bin/python3"
export WORKON_HOME="~/.virtualenvs"
export VIRTUALENVWRAPPER_VIRTUALENV="/usr/local/bin/virtualenv"
source /usr/local/bin/virtualenvwrapper.sh
```

#### Create a virtual environment
```
mkvirtualenv <environment name>
```

#### Choose a virtual environment
```
workon <environment name>
```

#### Quit a virtual environment
```
deactivate
```

### Django
In root folder (use a virtual environment):
```
pip install -r requirements.py
```

## USAGE

### Local

#### Config:
Comment these two lines at the end of collectify_api/settings.py:
```
- STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
- django_heroku.settings(locals())
```

#### Run server:
In root folder:
```
python3 manage.py runserver
```
Then open your web browser and go to:
```
http://127.0.0.1:8000
```
or
```
http://localhost:8000
```

#### Tests:
In root folder:
```
python3 manage.py test
```

### Heroku
Open your web browser and go to:
```
https://collectify-api.herokuapp.com
```

## URL ENDPOINTS
```
/admin/
/users/
/cars/
/colors/
```
