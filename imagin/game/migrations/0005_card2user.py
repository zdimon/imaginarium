# Generated by Django 3.1.5 on 2021-02-01 15:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0004_auto_20210201_1505'),
    ]

    operations = [
        migrations.CreateModel(
            name='Card2User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.card')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.gameuser')),
            ],
        ),
    ]
