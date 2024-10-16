from django.contrib import admin
from django.urls import path
from ExtremeFormsApp import views


app_name = 'ExtremeFormsApp'


urlpatterns = [
    path('', views.index , name='index'),
    path('new_form/', views.NewFormView.as_view() , name='new_form'),
    path('form_result/', views.form_result , name='form_result'),
    path('answer_form/<int:question_list_id>/', views.QuestionListView.as_view() , name='answer_form'),
]
