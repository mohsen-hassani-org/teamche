# Generated by Django 3.1.2 on 2021-05-13 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cfd', '0047_ptaanalysis_candle_pressure'),
    ]

    operations = [
        migrations.AddField(
            model_name='classicanalysis',
            name='trend_lilne',
            field=models.CharField(choices=[('bl', 'خط روند صعودی'), ('br', 'خط روند نزولی'), ('nt', 'بدون خط روند')], default='nt', max_length=2, verbose_name='خط روند'),
        ),
    ]