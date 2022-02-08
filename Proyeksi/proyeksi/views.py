from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from proyeksi.forms import LoginForm, KlimatologiForm, UserForm


def index(request):
    return render(request, 'home.html', {
        'title': 'Home'
    })


def klimatologi(request):
    return render(request, 'klimatologi/index.html', {
        'title': 'Data Klimatologi'
    })

class Auth(View):
    http_method_names = ['get', 'post', 'put', 'delete']

    def dispatch(self, *args, **kwargs):
        method = self.request.POST.get('_method', '').lower()
        if method == 'put':
            return self.put(*args, **kwargs)
        if method == 'delete':
            return self.delete(*args, **kwargs)
        return super(Auth, self).dispatch(*args, **kwargs)

    def get(self, request):
        return render(request, 'auth/login.html', {
            'title': 'Login Sistem',
            'login_form': LoginForm()
        })

    def post(self, request):
        loginform = LoginForm(request.POST)

        if loginform.is_valid():
            login(request, authenticate(username=loginform.cleaned_data.get('username'), password=loginform.cleaned_data.get('password')))
            return redirect('home')
        
        return render(request, 'auth/login.html', {
            'title': 'Login Sistem',
            'login_form': LoginForm(),
            'errors': loginform.errors
        })

    def delete(self, request):
        if request.user.is_authenticated:
            logout(request)
        return redirect('auth')


class Klimatologi(View):

    def get(self, request):
        return render(request, 'klimatologi/form.html', {
            'title': 'Tambah Data Klimatologi',
            'klimatologi_form': KlimatologiForm()
        })


class Proyeksi(View):
    http_method_names = ['get', 'post', 'put', 'delete']
    
    def get(self, request):
        return render(request, 'home.html', {
          'title': 'Proyeksi Data'
        })


class UserView(View):
    http_method_names = ['get', 'post', 'put', 'delete']

    def dispatch(self, *args, **kwargs):
        method = self.request.POST.get('_method', '').lower()
        if method == 'put':
            return self.put(*args, **kwargs)
        if method == 'delete':
            return self.delete(*args, **kwargs)
        return super(UserView, self).dispatch(*args, **kwargs)
    
    def get(self, request):
        return render(request, 'auth/form.html', {
          'title': 'Edit Profil',
          'user_form': UserForm(initial={
              'first_name': request.user.first_name,
              'last_name': request.user.last_name,
              'username': request.user.username,
              'email': request.user.email
          })
        })
        
    def put(self, request):
        userform = UserForm(request.POST, context={"request": request})

        if userform.is_valid():
            user = User.objects.get(id=request.user.id)
            user.first_name = userform.cleaned_data.get('first_name')
            user.last_name = userform.cleaned_data.get('last_name')
            user.email = userform.cleaned_data.get('email')
            user.username = userform.cleaned_data.get('username')
            if userform.cleaned_data.get('new_password') != '':
                user.set_password(userform.cleaned_data.get('new_password'))
            user.save()
            return redirect('home')

        return render(request, 'auth/form.html', {
          'title': 'Edit Profil',
          'user_form': UserForm(initial={
              'first_name': request.user.first_name,
              'last_name': request.user.last_name,
              'username': request.user.username,
              'email': request.user.email
          }),
          'errors': userform.errors
        })
