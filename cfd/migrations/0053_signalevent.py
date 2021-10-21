# Generated by Django 3.1.2 on 2021-08-10 18:34

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cfd', '0052_auto_20210624_1906'),
    ]

    operations = [
        migrations.CreateModel(
            name='SignalEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_datetime', models.DateTimeField(default=datetime.datetime.now, verbose_name='تاریخ و زمان')),
                ('event_type', models.CharField(choices=[('open', 'باز شده'), ('close', 'بسته شده'), ('change_sl', 'حد ضرر باز شده'), ('change_tp', 'حد سود باز شده'), ('dec_lot', 'کاهش حجم ورود'), ('inc_lot', 'افزایش حجم ورود')], default='open', max_length=10, verbose_name='نوع رخداد')),
                ('event_price', models.DecimalField(decimal_places=4, max_digits=11, verbose_name='قیمت')),
                ('operation_value', models.CharField(blank=True, max_length=10, null=True, verbose_name='مقدار عملیاتی')),
                ('description', models.TextField(blank=True, null=True, verbose_name='توضیحات')),
                ('signal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='cfd.signal', verbose_name='سیگنال')),
            ],
            options={
                'verbose_name': 'رخداد سیگنال',
                'verbose_name_plural': 'رخدادهای سیگنال',
                'ordering': ['-event_datetime'],
            },
        ),
    ]