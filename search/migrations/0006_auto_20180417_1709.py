# Generated by Django 2.0.3 on 2018-04-17 20:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0005_auto_20180417_1527'),
    ]

    operations = [
        migrations.RenameField(
            model_name='processcharacter',
            old_name='character_cod',
            new_name='character',
        ),
        migrations.RenameField(
            model_name='processcharacter',
            old_name='process_cod',
            new_name='process',
        ),
    ]
