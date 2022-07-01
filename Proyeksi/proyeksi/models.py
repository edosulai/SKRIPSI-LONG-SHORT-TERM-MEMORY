from django.db import models

from django.db.models import Q
from model_utils import Choices

# Create your models here.


class Klimatologi(models.Model):
    tanggal = models.DateField()
    tn = models.FloatField(blank=True, null=True)
    tx = models.FloatField(blank=True, null=True)
    tavg = models.FloatField(blank=True, null=True)
    rh_avg = models.FloatField(blank=True, null=True)
    rr = models.FloatField(blank=True, null=True)
    ss = models.FloatField(blank=True, null=True)
    ff_x = models.FloatField(blank=True, null=True)
    ddd_x = models.FloatField(blank=True, null=True)
    ff_avg = models.FloatField(blank=True, null=True)
    ddd_car = models.CharField(blank=True, null=True, max_length=2)

    def __str__(self) -> str:
        return "{}".format(self.tanggal)

    def query_data_by_args(**kwargs):
        draw = int(kwargs.get('draw')[0] if kwargs.get('draw', None) else 0)
        length = int(
            kwargs.get('length')[0] if kwargs.get('length', None) else 0)
        start = int(kwargs.get('start')[0] if kwargs.get('start', None) else 0)
        search_value = kwargs.get('search[value]')[0] if kwargs.get(
            'search[value]', None) else None
        order_column = int(
            kwargs.get('order[0][column]')[0] if kwargs.
            get('order[0][column]', None) else 0)
        order = kwargs.get('order[0][dir]')[0] if kwargs.get(
            'order[0][dir]', None) else None

        order_column = Choices((0, 'id'),
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
                                (11, 'ddd_car'))[order_column]

        if order == 'desc':
            order_column = '-' + order_column

        queryset = Klimatologi.objects.all()
        total = queryset.count()

        if search_value:
            queryset = queryset.filter(
                Q(id__icontains=search_value)
                | Q(tanggal__icontains=search_value)
                | Q(tn__icontains=search_value)
                | Q(tx__icontains=search_value)
                | Q(tavg__icontains=search_value)
                | Q(rh_avg__icontains=search_value)
                | Q(rr__icontains=search_value)
                | Q(ss__icontains=search_value)
                | Q(ff_x__icontains=search_value)
                | Q(ddd_x__icontains=search_value)
                | Q(ff_avg__icontains=search_value)
                | Q(ddd_car__icontains=search_value))

        count = queryset.count()
        queryset = queryset.order_by(order_column)[start:start + length]
        return {
            'items': queryset,
            'count': count,
            'total': total,
            'draw': draw
        }

class Riwayat(models.Model):
    timestep = models.IntegerField(blank=True, null=True)
    max_batch_size = models.IntegerField(blank=True, null=True)
    max_epoch = models.IntegerField(blank=True, null=True)
    layer_size = models.IntegerField(blank=True, null=True)
    unit_size = models.IntegerField(blank=True, null=True)
    dropout = models.FloatField(blank=True, null=True)
    learning_rate = models.FloatField(blank=True, null=True)
    row_start = models.IntegerField(blank=True, null=True)
    row_end = models.IntegerField(blank=True, null=True)
    num_predict = models.IntegerField(blank=True, null=True)
    logs = models.TextField(blank=True, null=True)
    hdf = models.BinaryField(blank=True, null=True)

    def __str__(self) -> str:
        return "{}".format(self.tanggal)
    
    def query_data_by_args(**kwargs):
        draw = int(kwargs.get('draw')[0] if kwargs.get('draw', None) else 0)
        length = int(
            kwargs.get('length')[0] if kwargs.get('length', None) else 0)
        start = int(kwargs.get('start')[0] if kwargs.get('start', None) else 0)
        search_value = kwargs.get('search[value]')[0] if kwargs.get(
            'search[value]', None) else None
        order_column = int(
            kwargs.get('order[0][column]')[0] if kwargs.
            get('order[0][column]', None) else 0)
        order = kwargs.get('order[0][dir]')[0] if kwargs.get(
            'order[0][dir]', None) else None

        order_column = Choices((0, 'id'), 
                                (1, 'timestep'), 
                                (2, 'max_batch_size'), 
                                (3, 'max_epoch'),
                                (4, 'layer_size'), 
                                (5, 'unit_size'), 
                                (6, 'dropout'),
                                (7, 'learning_rate'), 
                                (8, 'row_start'), 
                                (9, 'row_end'),
                                (10, 'num_predict'))[order_column]

        if order == 'desc':
            order_column = '-' + order_column

        queryset = Riwayat.objects.all()
        total = queryset.count()

        if search_value:
            queryset = queryset.filter(
                Q(id__icontains=search_value)
                | Q(timestep__icontains=search_value)
                | Q(max_batch_size__icontains=search_value)
                | Q(max_epoch__icontains=search_value)
                | Q(layer_size__icontains=search_value)
                | Q(unit_size__icontains=search_value)
                | Q(dropout__icontains=search_value)
                | Q(learning_rate__icontains=search_value)
                | Q(row_start__icontains=search_value)
                | Q(row_end__icontains=search_value)
                | Q(num_predict__icontains=search_value))

        count = queryset.count()
        queryset = queryset.order_by(order_column)[start:start + length]
        return {
            'items': queryset,
            'count': count,
            'total': total,
            'draw': draw
        }