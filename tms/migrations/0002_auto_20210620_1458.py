# Generated by Django 3.1.4 on 2021-06-20 12:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tms', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TestRun',
            new_name='TestResult',
        ),
    ]
