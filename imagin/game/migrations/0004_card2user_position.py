# Generated by Django 3.1.5 on 2021-02-03 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0003_card_card2user'),
    ]

    operations = [
        migrations.AddField(
            model_name='card2user',
            name='position',
            field=models.CharField(choices=[('hand', 'hand'), ('table', 'table')], default='hand', max_length=10),
        ),
    ]