from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User

from proyeksi.models import Klimatologi

class FormContextMixin:
    def __init__(self, *args, **kwargs):
        self.context = kwargs.pop("context", {})
        super().__init__(*args, **kwargs)

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        label='Username',
        widget=forms.TextInput(
            attrs={
              'class': 'block mt-1 w-full rounded-md shadow-sm border-gray-300 focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50',
              'autofocus': 'autofocus',
              'placeholder': 'Masukkan Username'
            }
        )
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'block mt-1 w-full rounded-md shadow-sm border-gray-300 focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50',
                'placeholder': 'Masukkan Password'
            }
        ),
    )
    remember_me = forms.BooleanField(
        required=False,
        label='Remember Me',
        widget=forms.CheckboxInput(
            attrs={
                'class': 'rounded border-gray-300 text-indigo-600 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'
            }
        )
    )

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError(
                "Maaf, Login gagal. Silakan coba lagi.")
        return self.cleaned_data


class UserForm(FormContextMixin, forms.Form):
    first_name = forms.CharField(
        required=False,
        max_length=100,
        label='Nama Lengkap',
        widget=forms.TextInput(
            attrs={
              'class': 'block mt-1 mr-3 w-full rounded-md shadow-sm border-gray-300 focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50',
              'placeholder': 'Nama Depan'
            }
        )
    )
    last_name = forms.CharField(
        required=False,
        max_length=100,
        label='Nama Lengkap',
        widget=forms.TextInput(
            attrs={
              'class': 'block mt-1 w-full rounded-md shadow-sm border-gray-300 focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50',
              'placeholder': 'Nama Belakang'
            }
        )
    )
    username = forms.CharField(
        max_length=100,
        label='Nama Pengguna',
        widget=forms.TextInput(
            attrs={
              'class': 'block mt-1 w-full rounded-md shadow-sm border-gray-300 focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50',
              'placeholder': 'Nama Pengguna'
            }
        )
    )
    email = forms.CharField(
        max_length=100,
        label='Email',
        widget=forms.TextInput(
            attrs={
              'class': 'block mt-1 w-full rounded-md shadow-sm border-gray-300 focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50',
              'placeholder': 'user@domain.com'
            }
        )
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'block mt-1 w-full rounded-md shadow-sm border-gray-300 focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50',

                'placeholder': 'Password'
            }
        ),
    )
    new_password = forms.CharField(
        required=False,
        label='Rubah Password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'block mt-1 mr-3 w-full rounded-md shadow-sm border-gray-300 focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50',
                'placeholder': 'Password Baru'
            }
        ),
    )
    repeat_password = forms.CharField(
        required=False,
        label='Rubah Password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'block mt-1 w-full rounded-md shadow-sm border-gray-300 focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50',
                'placeholder': 'Ulangi Password'
            }
        ),
    )

    def clean(self):
        new_password = self.cleaned_data.get("new_password")
        repeat_password = self.cleaned_data.get("repeat_password")
        password = self.cleaned_data.get("password")
                
        if check_password(password, self.context["request"].user.password) is not True:
            raise forms.ValidationError("Password Salah.")

        if new_password != repeat_password:
            raise forms.ValidationError(
                "Password Baru dan Ulangi Password tidak sama.")
            
        return self.cleaned_data

    class Meta:
        model = User


class KlimatologiForm(forms.Form):
    tanggal = forms.DateField(
        label='Tanggal',
        widget=forms.TextInput(
            attrs={
                'class': 'block mt-1 w-full rounded-md shadow-sm border-gray-300 focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50',
                'type': 'date',

                'autofocus': 'autofocus'
            }
        )
    )

    tn = forms.FloatField(
        required=False,
        label='Temperatur Min.',
        widget=forms.TextInput(
            attrs={
                'class': 'block mt-1 w-full rounded-md shadow-sm border-gray-300 focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50',
                'placeholder': 'Tn.'
            }
        )
    )
    tx = forms.FloatField(
        required=False,
        label='Temperatur Max.',
        widget=forms.TextInput(
            attrs={
                'class': 'block mt-1 w-full rounded-md shadow-sm border-gray-300 focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50',
                'placeholder': 'Tx.'
            }
        )
    )
    tavg = forms.FloatField(
        required=False,
        label='Temperatur Rata-Rata',
        widget=forms.TextInput(
            attrs={
                'class': 'block mt-1 w-full rounded-md shadow-sm border-gray-300 focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50',
                'placeholder': 'Tavg.'
            }
        )
    )
    rh_avg = forms.FloatField(
        required=False,
        label='Kelembapan Rata-Rata',
        widget=forms.TextInput(
            attrs={
                'class': 'block mt-1 w-full rounded-md shadow-sm border-gray-300 focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50',
                'placeholder': 'RH_avg.'
            }
        )
    )
    rr = forms.FloatField(
        required=False,
        label='Curah Hujan',
        widget=forms.TextInput(
            attrs={
                'class': 'block mt-1 w-full rounded-md shadow-sm border-gray-300 focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50',
                'placeholder': 'RR.'
            }
        )
    )
    ss = forms.FloatField(
        required=False,
        label='Lama Sinar Matahari',
        widget=forms.TextInput(
            attrs={
                'class': 'block mt-1 w-full rounded-md shadow-sm border-gray-300 focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50',
                'placeholder': 'ss.'
            }
        )
    )
    ff_x = forms.FloatField(
        required=False,
        label='Kecepatan Angin Max',
        widget=forms.TextInput(
            attrs={
                'class': 'block mt-1 w-full rounded-md shadow-sm border-gray-300 focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50',
                'placeholder': 'ff_x.'
            }
        )
    )
    ddd_x = forms.FloatField(
        required=False,
        label='Arah Angin Max',
        widget=forms.TextInput(
            attrs={
                'class': 'block mt-1 w-full rounded-md shadow-sm border-gray-300 focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50',
                'placeholder': 'ddd_x.'
            }
        )
    )
    ff_avg = forms.FloatField(
        required=False,
        label='Kecepatan Angin Rata-Rata',
        widget=forms.TextInput(
            attrs={
                'class': 'block mt-1 w-full rounded-md shadow-sm border-gray-300 focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50',
                'placeholder': 'ff_avg.'
            }
        )
    )
    ddd_car = forms.CharField(
        required=False,
        label='Arah Angin Terbanyak',
        max_length=2,
        widget=forms.TextInput(
            attrs={
                'class': 'block mt-1 w-full rounded-md shadow-sm border-gray-300 focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50',
                'placeholder': 'ddd_car.'
            }
        )
    )

    class Meta:
        model = Klimatologi
