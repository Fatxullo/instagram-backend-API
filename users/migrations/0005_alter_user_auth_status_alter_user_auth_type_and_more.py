# Generated by Django 4.2.3 on 2023-07-07 09:41

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='auth_status',
            field=models.CharField(choices=[('new', 'new'), ('code_verified', 'code_verified'), ('done', 'done'), ('photo_done', 'photo_done')], default='new', max_length=31),
        ),
        migrations.AlterField(
            model_name='user',
            name='auth_type',
            field=models.CharField(choices=[('via_phone', 'via_phone'), ('via_email', 'via_email')], max_length=31),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(blank=True, max_length=13, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='user_photos/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'heic', 'heif'])]),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_roles',
            field=models.CharField(choices=[('ordinary_user', 'ordinary_user'), ('manager', 'manager'), ('admin', 'admin')], default='ordinary_user', max_length=31),
        ),
        migrations.AlterField(
            model_name='userconfirmation',
            name='verify_type',
            field=models.CharField(choices=[('via_phone', 'via_phone'), ('via_email', 'via_email')], max_length=31),
        ),
    ]
