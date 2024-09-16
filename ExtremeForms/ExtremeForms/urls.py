from django.contrib import admin
from django.urls import path
from ExtremeFormsApp import views
from django.urls.conf import include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('security/', views.homeSec , name='sec-home'),
    path('', include('ExtremeFormsApp.urls')),
]
