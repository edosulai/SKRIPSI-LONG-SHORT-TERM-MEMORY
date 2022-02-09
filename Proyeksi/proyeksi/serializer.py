from django.conf import settings
from rest_framework import serializers
from proyeksi.models import Klimatologi

# Klimatologi Serializer
class KlimatologiSerializer(serializers.ModelSerializer):
  tanggal = serializers.DateField(format=settings.DATE_FORMAT)
  class Meta:
    model = Klimatologi
    fields = '__all__'