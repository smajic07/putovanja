# Generated by Django 3.2.5 on 2022-06-07 00:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login_i_registracija', '0006_zahtjevi_putovanja_tip'),
    ]

    operations = [
        migrations.AddField(
            model_name='agencije',
            name='slika',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.AddField(
            model_name='korisnici',
            name='slika',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]