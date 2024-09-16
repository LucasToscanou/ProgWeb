from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'ExtremeFormsApp/index.html')

def new_form(request):
    return render(request, 'ExtremeFormsApp/new_form.html')

def form_result(request):
    return render(request, 'ExtremeFormsApp/form_result.html')
