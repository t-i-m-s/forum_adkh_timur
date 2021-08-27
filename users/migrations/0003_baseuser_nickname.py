# Generated by Django 3.2 on 2021-05-15 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_baseuser_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='baseuser',
            name='nickname',
            field=models.CharField(default='name', max_length=100, unique=True, verbose_name='nickname'),
            preserve_default=False,
        ),
    ]
