# Generated by Django 4.0.2 on 2022-02-19 01:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Klimatologi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tanggal', models.DateField()),
                ('tn', models.FloatField(blank=True, null=True)),
                ('tx', models.FloatField(blank=True, null=True)),
                ('tavg', models.FloatField(blank=True, null=True)),
                ('rh_avg', models.FloatField(blank=True, null=True)),
                ('rr', models.FloatField(blank=True, null=True)),
                ('ss', models.FloatField(blank=True, null=True)),
                ('ff_x', models.FloatField(blank=True, null=True)),
                ('ddd_x', models.FloatField(blank=True, null=True)),
                ('ff_avg', models.FloatField(blank=True, null=True)),
                ('ddd_car', models.CharField(blank=True, max_length=2, null=True)),
            ],
        ),
    ]
