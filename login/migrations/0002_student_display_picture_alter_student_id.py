# Generated by Django 4.2 on 2023-04-08 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='display_picture',
            field=models.ImageField(default='default_profile_pic.png', null=True, upload_to='displaypictures'),
        ),
        migrations.AlterField(
            model_name='student',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
