# Generated by Django 3.2.6 on 2021-10-15 08:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20211014_1421'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='athlete',
            name='athleteid',
        ),
        migrations.RemoveField(
            model_name='club',
            name='clubid',
        ),
        migrations.RemoveField(
            model_name='record',
            name='resultid',
        ),
    ]