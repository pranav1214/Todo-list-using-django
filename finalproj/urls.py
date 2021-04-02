
from django.contrib import admin
from django.urls import path
from todoapp.views import home, create, delete, ulogin, usignup, ulogout


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('usignup/', usignup, name='usignup'),
    path('ulogin/', ulogin, name='ulogin'),
    path('ulogout/', ulogout, name='ulogout'),
    path('create/', create, name='create'),
    path('delete/<int:id>', delete, name='delete'),
]
