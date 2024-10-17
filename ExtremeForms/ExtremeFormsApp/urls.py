from django.contrib import admin
from django.urls import path
from ExtremeFormsApp import views

app_name = 'ExtremeFormsApp'

urlpatterns = [
    path('', views.index, name='index'),
    path('new_form/', views.NewFormView.as_view(), name='new_form'),
    path('new_form_initiated/<int:question_list_id>/', views.NewFormInitiatedView.as_view(), name='new_form_initiated'),
    path('form_result/', views.form_result, name='form_result'),
    path('answer_form/<int:question_list_id>/', views.QuestionListView.as_view(), name='answer_form'),
    path('user_forms/', views.UserFormsView.as_view(), name='user_forms'),
    path('form_details/<int:id>/', views.form_detail_view, name='form_details'),
    path('edit_form/<int:id>/', views.edit_form_view, name='edit_form'),
    path('delete_form/<int:id>/', views.delete_form_view, name='delete_form'),
    path('form_result/<int:id>/', views.form_result_view, name='form_result'),
    path('download_csv/<int:form_id>/', views.download_csv, name='download_csv'),
]
