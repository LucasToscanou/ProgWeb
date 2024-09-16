from django.shortcuts import render
from django.http import HttpResponse

def homeSec(request):
    return render(request, 'ExtremeFormsApp/new_form.html') #render(request, 'security/homeSec.html')