# Generated by Django 3.1.5 on 2021-02-01 15:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0003_cards'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Cards',
            new_name='Card',
        ),
    ]
