from rest_framework import serializers
from proyeksi.models import Klimatologi

# Klimatologi Serializer
class KlimatologiSerializer(serializers.ModelSerializer):
  class Meta:
    model = Klimatologi
    fields = '__all__'