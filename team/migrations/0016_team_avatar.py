# Generated by Django 3.1.2 on 2021-06-24 15:57

from django.db import migrations, models
import team.models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0015_remove_team_dmo_manager'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='avatar',
            field=models.ImageField(default='account/profile.png', max_length=300, upload_to='account/avatars', validators=[team.models.file_size_validator], verbose_name='تصویر نمایه'),
        ),
    ]