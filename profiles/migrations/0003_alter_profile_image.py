# Generated by Django 3.2.25 on 2024-03-29 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_alter_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='../default_profile_vs0i8n', upload_to='images/'),
        ),
    ]
