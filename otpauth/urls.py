from django.contrib import admin
from django.urls import path
from .views import home_view, auth_view, verify_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home_view'),
    path('login/', auth_view, name='login_view'),
    path('verify/', verify_view, name='verify_view'),
]
