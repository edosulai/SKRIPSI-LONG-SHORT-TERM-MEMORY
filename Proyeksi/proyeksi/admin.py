from django.contrib import admin

# Register your models here.
from .models import Klimatologi, Riwayat

admin.site.register(Klimatologi)
admin.site.register(Riwayat)