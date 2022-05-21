# Generated by Django 3.1.2 on 2022-05-21 06:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TodoList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='آخرین ویرایش')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='ایجاد شده در')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='todo_lists', to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'Todo لیست',
                'verbose_name_plural': 'Todo لیست',
                'unique_together': {('date', 'user')},
            },
        ),
        migrations.CreateModel(
            name='TodoListItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='عنوان')),
                ('desc', models.TextField(verbose_name='توضیحات')),
                ('status', models.IntegerField(choices=[(0, 'در انتظار انجام'), (100, 'انجام شد'), (200, 'انجام نشد')], default=0, verbose_name='وضعیت')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='آخرین ویرایش')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='ایجاد شده در')),
                ('todo_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='todo_list.todolist', verbose_name='Todo')),
            ],
            options={
                'verbose_name': 'آیتم Todo لیست',
                'verbose_name_plural': 'آیتم Todo لیست',
            },
        ),
        migrations.CreateModel(
            name='TodoListItemTimeTrack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_datetime', models.DateTimeField(blank=True, null=True, verbose_name='شروع')),
                ('end_datetime', models.DateTimeField(blank=True, null=True, verbose_name='پایان')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='آخرین ویرایش')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='ایجاد شده در')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='time_tracks', to='todo_list.todolistitem', verbose_name='آیتم')),
            ],
            options={
                'verbose_name': 'Todo لیست زمان',
                'verbose_name_plural': 'Todo لیست زمان',
            },
        ),
    ]
