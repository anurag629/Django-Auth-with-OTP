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

* add CustomUser model in settings.py file of project :

            AUTH_USER_MODEL = 'users.CustomUser'

## 7. Create models in codes app :

    from django.db import models
        from users.models import CustomUser
        import random
        # Create your models here.


        class Code(models.Model):
            number = models.CharField(max_length=5, blank=True)
            user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

            def __str__(self):
                return str(self.number)

            def save(self, *args, **kwargs):
                number_list = [x for x in range(10)]
                code_items = []

                for i in range(5):
                    num = random.choice(number_list)
                    code_items.append(num)

                code_string = "".join(str(item) for item in code_items)
                self.number = code_string
                super().save(*args, **kwargs)

## 8. Create signals.py file in codes app and write the below code :

    from users.models import CustomUser
    from .models import Code
    from django.db.models.signals import post_save
    from django.dispatch import receiver


    @receiver(post_save, sender=CustomUser)
    def post_save_generate_code(sender, instance, created, *args, **kwargs):
        if created:
            Code.objects.create(user=instance)

* now go to apps.py file of codes app and create function in CodesConfig class :
            
        def ready(self):
            import codes.signals

* now go to __init__.py file of codes app and write the following line:

        default_app_config = 'codes.apps.CodesConfig'

## 9. register Code in admin.py of code app.
## 10. register CustomUser in admin.py of users app.

## 11. Create forms.py file in codes app and write below code in it :

    from django import forms
    from .models import Code


    class CodeForm(forms.ModelForm):
        number = forms.CharField(
            label="Code",  help_text="Enter SMS verification code.")

        class Meta:
            model = Code
            fields = ('number',)

## 12. Create views in project folder :

    from django.shortcuts import render, redirect
    from django.contrib.auth.decorators import login_required
    from django.contrib.auth.forms import AuthenticationForm
    from django.contrib.auth import authenticate, login
    from codes.forms import CodeForm
    from codes.models import CustomUser


    @login_required
    def home_view(request):
        return render(request, 'main.html', {})


    def auth_view(request):
        form = AuthenticationForm()
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                request.session['pk'] = user.pk
                return redirect('verify_view')

        return render(request, 'login.html', {'form': form})


    def verify_view(request):
        form = CodeForm(request.POST or None)
        pk = request.session.get('pk')
        if pk:
            user = CustomUser.objects.get(pk=pk)
            code = user.code
            code_user = f"{user.username}: {user.code}"
            if not request.POST:
                # send sms
                print(code_user)

            if form.is_valid():
                num = form.cleaned_data.get('number')

                if str(code) == num:
                    code.save()
                    login(request, user)
                    return redirect('home_view')
                else:
                    return redirect('login_view')
        return render(request, 'verify.html', {'form': form})


## 13. add urls to project :

    from django.contrib import admin
    from django.urls import path
    from .views import home_view, auth_view, verify_view

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('', home_view, name='home_view'),
        path('login/', auth_view, name='login_view'),
        path('verify/', verify_view, name='verify_view'),
    ]


## 14. crete templates :
* create login.html :

        {% extends 'base.html' %}

        {% load crispy_forms_tags %}

        {% block content %}
            <div class="row">
                <div class="col-4">
                    <form action="" method="POST" autocomplate="off">
                        {% csrf_token %}
                        {{form|crispy}}
                        <button type="submit" class="btn btn-primary">Login</button>
                    </form>
                </div>
            </div>

        {% endblock content %}

* create main.html

        {% extends 'base.html' %}

        {% block content %}
        Hello world

        {% endblock content %}

* create verify.html :

        {% extends 'base.html' %}

        {% load crispy_forms_tags %}

        {% block content %}
            <div class="row">
                <div class="col-4">
                    <form action="" method="POST" autocomplate="off">
                        {% csrf_token %}
                        {{form|crispy}}
                        <button type="submit" class="btn btn-primary">Verify</button>
                    </form>
                </div>
            </div>

        {% endblock content %}

## 15. Create utils.py file in project and add folloeing code :
    import os
    from twilio.rest import Client

    account_sid = 'your twilio sid'
    auth_token = 'your auth token'
    client = Client(account_sid, auth_token)


    def send_sms(user_code, phone_number):
        message = client.messages.create(
            body=f'Hi there your verification code is - {user_code}',
            from_='your twilio number',
            to=f'+91{phone_number}'
        )
        print(message.sid)

## 15. add twilio 'send_sms' function from utils in views.py file :
     send_sms(code_user, user.phone_number)


# Thank You! All Done.