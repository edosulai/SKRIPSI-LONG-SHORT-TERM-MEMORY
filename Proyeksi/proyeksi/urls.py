"""proyeksi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import routers

from proyeksi.api import KlimatologiViewSet, RiwayatViewSet
from proyeksi.views import index, AuthView, KlimatologiView, ProyeksiView, UserView
from django.contrib.auth.decorators import login_required

router = routers.DefaultRouter()
router.register('klimatologi', KlimatologiViewSet, 'klimatologi')
router.register('proyeksi', RiwayatViewSet, 'proyeksi')

urlpatterns = [
    path('admin/', admin.site.urls, name="admin"),

    path('klimatologi/', login_required(KlimatologiView.as_view(), login_url='/auth/'), name="klimatologi"),
    path('klimatologi/<str:target>/', login_required(KlimatologiView.as_view(), login_url='/auth/'), name="klimatologi"),

    path('proyeksi/', login_required(ProyeksiView.as_view(), login_url='/auth/'), name="proyeksi"),
    path('proyeksi/<str:target>/', login_required(ProyeksiView.as_view(), login_url='/auth/'), name="proyeksi"),

    path('user/', login_required(UserView.as_view(), login_url='/auth/'), name="user"),

    path('auth/', AuthView.as_view(), name="auth"),

    path('api/', include((router.urls, 'proyeksi'))),

    path('', login_required(index, login_url='/auth/'), name="home")
]
