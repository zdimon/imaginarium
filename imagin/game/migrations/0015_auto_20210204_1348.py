# Generated by Django 3.1.5 on 2021-02-04 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0014_remove_gameuser_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='card_images'),
        ),
        migrations.AlterField(
            model_name='gameuser',
            name='association',
            field=models.TextField(default='Придумываем ассоциацию'),
        ),
        migrations.AlterField(
            model_name='gameuser',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='user_images', verbose_name='Выберите картинку'),
        ),
        migrations.AlterField(
            model_name='gameuser',
            name='login',
            field=models.CharField(max_length=50, unique=True, verbose_name='Ваше имя'),
        ),
    ]
