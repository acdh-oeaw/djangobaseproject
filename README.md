# Django Base Project

## about

As the name suggests, this is a basic django project. The idea of this base project is mainly to bootstrap the web application development process through setting up such a Django Base Project which already provides a couple a django apps providing quite generic functionalites needed for building web application bound to the Digital Humanities Domain

## install

1. Download or Clone this repo
2. Rename the root folder of this project `djangobaseproject` to the name chosen for your new project (e.g. to `mynewproject`)
3. Likewise rename `djangobaseproject` folder in your projects root folder.
4. Adapt the information in `webpage/metadata.py` according to your needs.
5. Create an virtual environment and run `pip install -r requirements.txt`

### first steps

This projects uses modularized settings (to keep sensitiv information out of version control or being able to use the same code for developement and production). Thefore you'll have to append all `manage.py` commands with a `--settings` parameter pointing to the settings file you'd like to run the code with. For developement just append `--settings={nameOfYouProject}.settings.dev` to the following commands, e.g. `python manage.py makemigrations --settings=djangobaseproject.settings.dev`

6. Run `makemigrations`, `migrate`, and `runserver` and check [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## next steps

Build your custom awesome Web App.

## Tests

To get needed software you can run

    pip install -r requirements_test.txt

To run the tests execute

    python manage.py test --settings=djangobaseproject.settings.test
