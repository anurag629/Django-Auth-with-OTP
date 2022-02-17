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

* 