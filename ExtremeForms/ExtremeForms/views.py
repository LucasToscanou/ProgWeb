from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView

def homeSec(request):
    return render(request, 'security/homeSec.html')

def register(request):
 if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('sec-home')
 else:
    form = UserCreationForm()
    context = {'form': form, }
    return render(request, 'security/register.html', context)

@login_required
def secretPage(request):
    return render(request, 'security/secretPage.html')

def logout(request):
   return render(request,'security/logout.html')

class MeuUpdateView(UpdateView):
    def get(self, request, pk, *args, **kwargs):
        if request.user.id == pk:
            return super().get(request, pk, args, kwargs)
        else:
            return redirect('sec-home')
