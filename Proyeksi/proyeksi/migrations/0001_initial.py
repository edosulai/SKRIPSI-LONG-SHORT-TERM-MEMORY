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
                ('ddd_car', models.CharField(blank=True, null=True, max_length=2)),
            ],
        ),
        
        migrations.CreateModel(
            name='Riwayat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestep', models.IntegerField(blank=True, null=True)),
                ('max_batch_size', models.IntegerField(blank=True, null=True)),
                ('max_epoch', models.IntegerField(blank=True, null=True)),
                ('layer_size', models.IntegerField(blank=True, null=True)),
                ('unit_size', models.IntegerField(blank=True, null=True)),
                ('dropout', models.FloatField(blank=True, null=True)),
                ('learning_rate', models.FloatField(blank=True, null=True)),
                ('row_start', models.CharField(blank=True, null=True, max_length=32)),
                ('row_end', models.CharField(blank=True, null=True, max_length=32)),
                ('num_predict', models.IntegerField(blank=True, null=True)),
                ('feature_training', models.CharField(blank=True, null=True, max_length=64)),
                ('feature_predict', models.CharField(blank=True, null=True, max_length=8)),
                ('rmse', models.FloatField(blank=True, null=True)),
                ('valueset', models.JSONField(blank=True, null=True)),
                ('hdf', models.CharField(blank=True, null=True, max_length=64)),
            ],
        ),
    ]
