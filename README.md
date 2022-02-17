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
    
        
