from django.db import models

from django.db.models import Q
from model_utils import Choices

# Create your models here.

ORDER_COLUMN_CHOICES = Choices(
    (0, 'id'),
    (1, 'tanggal'),
    (2, 'tn'),
    (3, 'tx'),
    (4, 'tavg'),
    (5, 'rh_avg'),
    (6, 'rr'),
    (7, 'ss'),
    (8, 'ff_x'),
    (9, 'ddd_x'),
    (10, 'ff_avg'),
    (11, 'ddd_car')
)


class Klimatologi(models.Model):
    tanggal = models.DateField()      # Tanggal
    tn = models.FloatField(blank=True)   # Temperatur minimum
    tx = models.FloatField(blank=True)   # Temperatur maksimum
    tavg = models.FloatField(blank=True)   # Temperatur rata-rata
    rh_avg = models.FloatField(blank=True)   # Kelembapan rata-rata
    rr = models.FloatField(blank=True)   # Curah hujan
    ss = models.FloatField(blank=True)   # Lamanya penyinaran matahari
    ff_x = models.FloatField(blank=True)   # Kecepatan angin maksimum
    ddd_x = models.FloatField(blank=True)  # Arah angin saat kecepatan maksimum
    ff_avg = models.FloatField(blank=True)   # Kecepatan angin rata-rata
    ddd_car = models.CharField(
        blank=True, max_length=2)   # Arah angin terbanya

    def __str__(self) -> str:
        return "{}".format(self.tanggal)


def query_data_by_args(**kwargs):
    draw = int(kwargs.get('draw')[0] if kwargs.get('draw', None) else 0)
    length = int(kwargs.get('length')[0] if  kwargs.get('length', None)  else 0)
    start = int(kwargs.get('start')[0] if  kwargs.get('start', None)  else 0)
    search_value = kwargs.get('search[value]')[0] if  kwargs.get('search[value]', None)  else None
    order_column = int(kwargs.get('order[0][column]')[0] if  kwargs.get('order[0][column]', None)  else 0)
    order = kwargs.get('order[0][dir]')[0] if  kwargs.get('order[0][dir]', None)  else None
    
    order_column = ORDER_COLUMN_CHOICES[order_column]
    if order == 'desc':
        order_column = '-' + order_column

    queryset = Klimatologi.objects.all()
    total = queryset.count()

    if search_value:
        queryset = queryset.filter(
            Q(id__icontains=search_value) |
            Q(tanggal__icontains=search_value) |
            Q(tn__icontains=search_value) |
            Q(tx__icontains=search_value) |
            Q(tavg__icontains=search_value) |
            Q(rh_avg__icontains=search_value) |
            Q(rr__icontains=search_value) |
            Q(ss__icontains=search_value) |
            Q(ff_x__icontains=search_value) |
            Q(ddd_x__icontains=search_value) |
            Q(ff_avg__icontains=search_value) |
            Q(ddd_car__icontains=search_value)
        )

    count = queryset.count()
    queryset = queryset.order_by(order_column)[start:start + length]
    return {
        'items': queryset,
        'count': count,
        'total': total,
        'draw': draw
    }
