# Generated by Django 3.2.6 on 2021-09-16 08:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_remove_athlete_license'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='athlete',
            name='club',
        ),
        migrations.RemoveField(
            model_name='meet',
            name='athletes',
        ),
        migrations.AddField(
            model_name='club',
            name='type',
            field=models.CharField(choices=[('CLUB', 'CLUB'), ('NATIONALTEAM', 'NATIONALTEAM'), ('REGIONALTEAM', 'REGIONALTEAM'), ('UNATTACHED', 'UNATTACHED')], default='UNATTACHED', max_length=25),
        ),
        migrations.CreateModel(
            name='AthleteClub',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('athlete', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.athlete')),
                ('club', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.club')),
            ],
        ),
        migrations.AddField(
            model_name='meet',
            name='athleteclubs',
            field=models.ManyToManyField(to='main.AthleteClub'),
        ),
    ]
