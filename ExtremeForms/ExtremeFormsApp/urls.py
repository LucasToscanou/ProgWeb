from django.contrib import admin
from django.urls import path
from ExtremeFormsApp import views

urlpatterns = [
    path('', views.index , name='index'),
    path('/new_form/', views.new_form , name='form'),
    path('/form_result/', views.form_result , name='form_result'),
]
