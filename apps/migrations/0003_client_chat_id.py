# Generated by Django 3.1.6 on 2021-02-23 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0002_auto_20210218_1802'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='chat_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
