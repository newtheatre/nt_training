# Nottingham New Theatre Technical Training 
## Django-based training system - contains a training specification, split into categories; full membership details; and details of individual training sessions.

The training site is a move from a paper training system to a digital one. It is extendable, and fully customisable through the Django admin interface. 

Its use over a paper system is not only good for trees, but also serves to be accessible anywhere, by anyone; easier to update and manage, filter, or organise; and offers a higher level of authorisation.

### Key Idea
Training is given to a person (or people) through training sessions, where another person is designated trainer. Anyone can be a trainer, but training sessions can only be added by authorised users.

# Running locally 

You will need: 
* Django 1.11.1 
* Python 3.6.1 (and Pip) 
* Ruby and Rubygems (for Bootstrap 4, Sass and Compass)

## Installation 
### Python Virtualenv 
Using your preferred mechanism, create a virtual Python environment. This could be with PyCharm or virtualenv. I used virtualenv, like so:

```
virtualenv <dir>
``` 

Where `<dir>` is a given directory; something like `training`
#### Activate the virtualenv 

```
**Windows**
<virtualenv_dir>/Scripts/activate.bat

**Unix**
source <virtualenv_dir>/bin/activate
``` 

#### Install the requirements 

```
cd <dir>
pip install -r requirements.txt 
```

#### Run the server 
```
python manage.py runserver 
``` 
Pages can be browsed locally at http://localhost:8000/

### Sass
Once Rubygems is installed, run:
```
gem install bundler
bundle install 
```
to install the relevant gems.

To compile the Sass, navigate to <dir>/static/nt_training/static/ directory and run:
``` 
compass compile --force
``` 
Or 
```
compass watch
```
to recompile after every save of a Sass file.

# Help 

The [Django documentation](https://docs.djangoproject.com/en/1.11/) is a good place to start, or just drop us an email - [it@newtheatre.org.uk](mailto:it@newtheatre.org.uk)