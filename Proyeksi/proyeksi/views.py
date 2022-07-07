from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from proyeksi.models import Klimatologi, Riwayat
from proyeksi.forms import LoginForm, KlimatologiForm, UserForm, ProyeksiForm


def index(request):
    return render(request, 'home.html', {
        'title': 'Home'
    })

class AuthView(View):
    http_method_names = ['get', 'post', 'put', 'delete']

    def dispatch(self, *args, **kwargs):
        method = self.request.POST.get('_method', '').lower()
        if method == 'put':
            return self.put(*args, **kwargs)
        if method == 'delete':
            return self.delete(*args, **kwargs)
        return super(AuthView, self).dispatch(*args, **kwargs)

    def get(self, request):
        return render(request, 'auth/login.html', {
            'title': 'Login Sistem',
            'login_form': LoginForm()
        })

    def post(self, request):
        loginform = LoginForm(request.POST)

        if loginform.is_valid():
            if not loginform.cleaned_data.get('remember_me'):
                self.request.session.set_expiry(0)
                self.request.session.modified = True
            login(request, authenticate(username=loginform.cleaned_data.get(
                'username'), password=loginform.cleaned_data.get('password')))
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


class KlimatologiView(View):
    http_method_names = ['get', 'post', 'put', 'delete']

    def dispatch(self, *args, **kwargs):
        method = self.request.POST.get('_method', '').lower()
        if method == 'put':
            return self.put(*args, **kwargs)
        if method == 'delete':
            return self.delete(*args, **kwargs)
        return super(KlimatologiView, self).dispatch(*args, **kwargs)

    def get(self, request, target=None):
        if target and target.isnumeric():
            klimatologi = get_object_or_404(Klimatologi, id=target)
            return render(request, 'klimatologi/form.html', {
                'id': klimatologi.id,
                'title': 'Edit Data Klimatologi',
                'subtitle': 'Edit Data',
                'klimatologi_form': KlimatologiForm(initial={
                    'tanggal': klimatologi.tanggal,
                    'tn': klimatologi.tn,
                    'tx': klimatologi.tx,
                    'tavg': klimatologi.tavg,
                    'rh_avg': klimatologi.rh_avg,
                    'rr': klimatologi.rr,
                    'ss': klimatologi.ss,
                    'ff_x': klimatologi.ff_x,
                    'ddd_x': klimatologi.ddd_x,
                    'ff_avg': klimatologi.ff_avg,
                    'ddd_car': klimatologi.ddd_car
                })
            })

        elif target == 'tambah':
            return render(request, 'klimatologi/form.html', {
                'title': 'Tambah Data Klimatologi',
                'subtitle': 'Tambah Data',
                'klimatologi_form': KlimatologiForm()
            })

        return render(request, 'klimatologi/index.html', {
            'title': 'Data Klimatologi'
        })

    def post(self, request):
        klimatologiform = KlimatologiForm(request.POST)
        if klimatologiform.is_valid():
            klimatologiform.save()
            return redirect('klimatologi')

        return render(request, 'klimatologi/form.html', {
            'title': 'Tambah Data Klimatologi',
            'klimatologi_form': KlimatologiForm(initial={
                'tanggal': klimatologiform.cleaned_data.get('tanggal'),
                'tn': klimatologiform.cleaned_data.get('tn'),
                'tx': klimatologiform.cleaned_data.get('tx'),
                'tavg': klimatologiform.cleaned_data.get('tavg'),
                'rh_avg': klimatologiform.cleaned_data.get('rh_avg'),
                'rr': klimatologiform.cleaned_data.get('rr'),
                'ss': klimatologiform.cleaned_data.get('ss'),
                'ff_x': klimatologiform.cleaned_data.get('ff_x'),
                'ddd_x': klimatologiform.cleaned_data.get('ddd_x'),
                'ff_avg': klimatologiform.cleaned_data.get('ff_avg'),
                'ddd_car': klimatologiform.cleaned_data.get('ddd_car')
            }),
            'errors': klimatologiform.errors
        })

    def put(self, request, target):
        klimatologiform = KlimatologiForm(request.POST)
        if klimatologiform.is_valid():
            klimatologi = get_object_or_404(Klimatologi, id=target)
            klimatologi.tanggal = klimatologiform.cleaned_data.get('tanggal')
            klimatologi.tn = klimatologiform.cleaned_data.get('tn')
            klimatologi.tx = klimatologiform.cleaned_data.get('tx')
            klimatologi.tavg = klimatologiform.cleaned_data.get('tavg')
            klimatologi.rh_avg = klimatologiform.cleaned_data.get('rh_avg')
            klimatologi.rr = klimatologiform.cleaned_data.get('rr')
            klimatologi.ss = klimatologiform.cleaned_data.get('ss')
            klimatologi.ff_x = klimatologiform.cleaned_data.get('ff_x')
            klimatologi.ddd_x = klimatologiform.cleaned_data.get('ddd_x')
            klimatologi.ff_avg = klimatologiform.cleaned_data.get('ff_avg')
            klimatologi.ddd_car = klimatologiform.cleaned_data.get('ddd_car')
            klimatologi.save()
            return redirect('klimatologi')

        return render(request, 'klimatologi/form.html', {
            'id': target,
            'title': 'Edit Data Klimatologi',
            'klimatologi_form': KlimatologiForm(initial={
                'tanggal': klimatologiform.cleaned_data.get('tanggal'),
                'tn': klimatologiform.cleaned_data.get('tn'),
                'tx': klimatologiform.cleaned_data.get('tx'),
                'tavg': klimatologiform.cleaned_data.get('tavg'),
                'rh_avg': klimatologiform.cleaned_data.get('rh_avg'),
                'rr': klimatologiform.cleaned_data.get('rr'),
                'ss': klimatologiform.cleaned_data.get('ss'),
                'ff_x': klimatologiform.cleaned_data.get('ff_x'),
                'ddd_x': klimatologiform.cleaned_data.get('ddd_x'),
                'ff_avg': klimatologiform.cleaned_data.get('ff_avg'),
                'ddd_car': klimatologiform.cleaned_data.get('ddd_car')
            }),
            'errors': klimatologiform.errors
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


class ProyeksiView(View):
    http_method_names = ['get', 'post', 'put', 'delete']

    def dispatch(self, *args, **kwargs):
        method = self.request.POST.get('_method', '').lower()
        if method == 'put':
            return self.put(*args, **kwargs)
        if method == 'delete':
            return self.delete(*args, **kwargs)
        return super(ProyeksiView, self).dispatch(*args, **kwargs)

    def get(self, request, target=None):
        if target and target.isnumeric():
            riwayat = get_object_or_404(Riwayat, id=target)
            return render(request, 'proyeksi/result.html', {
                'title': 'Hasil Proyeksi',
                'learning_rate': riwayat.learning_rate,
                'dropout': riwayat.dropout,
                'sequence': riwayat.sequence,
                'max_epoch': riwayat.max_epoch,
                'batch_size': riwayat.batch_size,
                'hidden_units': riwayat.hidden_units,
                'much_predict': riwayat.much_predict,
                'nan_handling': riwayat.nan_handling,
            })

        elif target == 'baru':
            first = Klimatologi.objects.first()
            last = Klimatologi.objects.last()
            return render(request, 'proyeksi/form.html', {
                'title': 'Proyeksi',
                'proyeksi_form': ProyeksiForm(initial={
                    'timestep': 2,
                    'max_epoch': 50,
                    'max_batch_size': 1,
                    'layer_size': 1,
                    'unit_size': 1,
                    'learning_rate': 0.1,
                    'dropout': 0.0,
                    'row_start': first.tanggal, #yyyy-mm-dd
                    'row_end': last.tanggal,
                    'num_predict': 5,
                })
            })
        
        return render(request, 'proyeksi/index.html', {
            'title': 'Riwayat Proyeksi'
        })

    def post(self, request):
        proyeksiform = ProyeksiForm(request.POST)
        if proyeksiform.is_valid():
            return render(request, 'proyeksi/result.html', {
                'title': 'Hasil Proyeksi',
                'proyeksi_form': ProyeksiForm(initial={
                    'timestep': proyeksiform.cleaned_data.get('timestep'),
                    'max_epoch': proyeksiform.cleaned_data.get('max_epoch'),
                    'max_batch_size': proyeksiform.cleaned_data.get('max_batch_size'),
                    'layer_size': proyeksiform.cleaned_data.get('layer_size'),
                    'unit_size': proyeksiform.cleaned_data.get('unit_size'),
                    'learning_rate': proyeksiform.cleaned_data.get('learning_rate'),
                    'dropout': proyeksiform.cleaned_data.get('dropout'),
                    'row_start': proyeksiform.cleaned_data.get('row_start').strftime('%Y-%m-%d'),
                    'row_end': proyeksiform.cleaned_data.get('row_end').strftime('%Y-%m-%d'),
                    'num_predict': proyeksiform.cleaned_data.get('num_predict')
                })
            })

        return render(request, 'proyeksi/form.html', {
            'title': 'Proyeksi',
            'proyeksi_form': ProyeksiForm(initial={
                'timestep': proyeksiform.cleaned_data.get('timestep'),
                'max_epoch': proyeksiform.cleaned_data.get('max_epoch'),
                'max_batch_size': proyeksiform.cleaned_data.get('max_batch_size'),
                'layer_size': proyeksiform.cleaned_data.get('layer_size'),
                'unit_size': proyeksiform.cleaned_data.get('unit_size'),
                'learning_rate': proyeksiform.cleaned_data.get('learning_rate'),
                'dropout': proyeksiform.cleaned_data.get('dropout'),
                'row_start': proyeksiform.cleaned_data.get('row_start'),
                'row_end': proyeksiform.cleaned_data.get('row_end'),
                'num_predict': proyeksiform.cleaned_data.get('num_predict')
            }),
            'errors': proyeksiform.errors
        })
