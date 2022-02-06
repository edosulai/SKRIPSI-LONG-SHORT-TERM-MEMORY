from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
# from django.views.generic import ListView

def index(request):
    context = {
        'title': 'Home'
    }
    return render(request, 'dashboard.html', context)


class Klimatologi(View):
    def get(self, request):
        context = {
            'title': 'Data Klimatologi'
        }
        return render(request, 'klimatologi/index.html', context)


class Proyeksi(View):
    def get(self, request):
        # context = {
        #   'title': 'Proyeksi Data'
        # }
        # return render(request, 'dashboard.html', context)
        return HttpResponse("Proyeksi")


class User(View):
    def get(self, request):
        # context = {
        #   'title': 'Proyeksi Data'
        # }
        # return render(request, 'dashboard.html', context)
        return HttpResponse("User")
