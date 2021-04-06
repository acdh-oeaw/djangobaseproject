[![DOI](https://zenodo.org/badge/95352230.svg)](https://zenodo.org/badge/latestdoi/95352230)

# Django Base Project

## About

As the name suggests, this is a basic Django project. The idea of this base project is mainly to bootstrap the web application development process through setting up such a Django Base Project which already provides a couple of Django apps providing quite generic functionalities needed for building web application bound to the Digital Humanities Domain.

## Install

* clone the repo `git clone `https://github.com/acdh-oeaw/djangobaseproject.git {project-name}`
* cd into into {project-name}: `cd {project-name}`
* remove existing git-repo: `rm -rf .git`
* [optional]
  * create a virtual env, e.g. `virtualenv myenv`
  * activate virtual env, e.g. `source myenv/bin/activate` (Windows: `myenv\Scripts\activate`)
* install needed packages `pip install -r requirements.txt`

## Start

* make migrations `python manage.py makemigrations --settings=djangobaseproject.settings.dev`
* apply migrations `python manage.py migrate --settings=djangobaseproject.settings.dev`
* start dev-server `python manage.py runserver --settings=djangobaseproject.settings.dev`
* open http://127.0.0.1:8000/


# included packages

## [acdh-django-browsing](https://github.com/acdh-oeaw/acdh-django-browsing)

Django-App providing some useful things to create browsing views


## [acdh-django-vocabs](https://github.com/acdh-oeaw/acdh-django-vocabs)

Curate controlled vocabularies as SKOS

## [acdh-django-geonames](https://github.com/acdh-oeaw/acdh-django-geonames)

A django package providing models and views for Geoname Places

* populate vocabs with geoname-feature codes
    * `python manage.py import_ftc --lang=en--settings=djangobaseproject.settings.dev`
* populate db with geoname-places of a given country:
    * `python manage.py import_places ..--country_code=YU--settings=djangobaseproject.settings.dev`
