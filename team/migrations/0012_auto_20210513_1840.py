# Generated by Django 3.1.2 on 2021-05-13 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0011_auto_20210420_1250'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendance',
            name='leave_hours',
        ),
        migrations.AddField(
            model_name='attendance',
            name='leave_minutes',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='مدت مرخصی (دقیقه)'),
        ),
    ]