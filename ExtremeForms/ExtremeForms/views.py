from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.views.generic.edit import UpdateView
from django.views import View

def register(request):
 if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('sec-login')
 else:
    form = UserCreationForm()
    context = {'form': form, }
    return render(request, 'security/register.html', context)

@login_required
def logout(request):
   return render(request,'security/logout.html')

class MeuUpdateView(UpdateView):
    def get(self, request, pk, *args, **kwargs):
        if request.user.id == pk:
            return super().get(request, pk, args, kwargs)
        else:
            return redirect('sec-login')

@login_required
def userPage(request):
    return render(request, 'security/user_page.html', {'user': request.user})

