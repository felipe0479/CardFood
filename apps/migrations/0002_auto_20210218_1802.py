# Generated by Django 2.2.18 on 2021-02-18 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='codigo',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='client',
            name='cedula',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='client',
            name='celular',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
