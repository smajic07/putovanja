# Generated by Django 3.2.5 on 2022-06-06 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login_i_registracija', '0005_putovanja_slika'),
    ]

    operations = [
        migrations.AddField(
            model_name='zahtjevi_putovanja',
            name='tip',
            field=models.CharField(default='nesto', max_length=100),
            preserve_default=False,
        ),
    ]
