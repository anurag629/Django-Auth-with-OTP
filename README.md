# Django-Auth-with-OTP

## 1. create folder named 'django auth otp'.

## 2. Now open cmd/terminal in that folder :
* create virtual environment and activate it:

        virtualenv env
        source env/bin/activate

* install following requirements in environment :

        pip install django
        pip install django-crispy-forms
        pip install django-twilio

## 3. Now create django project and apps:

    django-admin startproject otpauth .
    python manage.py startapp users
    python manage.py startapp codes

## 4. add apps other things to settings.py of project :

* add installed apps :

        INSTALLED_APPS = [
            ....,
            'users',
            'codes',
            'crispy_forms',
            ....,
        ]

* add the below code anywhere in settings.py file :

        CRISPY_TEMPLATE_PACK = 'bootstrap4'
        LOGIN_URL = '/login/'
        # default: accounts/login/

## 5. Create templates folder in project directory :
* create base.html file in templates folder you have created and write below code in it :

        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
            <title>OTP Django Auth</title>
        </head>
        <body>
            <div class="container mt-3">
                {% block content %}
                
                {% endblock content %}
            </div>

            <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
            <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
        </body>
        </html>

## 6. Create models in users app :

    from django.db import models
    from django.contrib.auth.models import AbstractUser
    # Create your models here.


    class CustomUser(AbstractUser):
        phone_number = models.CharField(max_length=12)
