# Generated by Django 3.2.5 on 2022-06-05 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login_i_registracija', '0002_korisnik_putovanja_putovanja_zahtjevi_putovanja'),
    ]

    operations = [
        migrations.AddField(
            model_name='zahtjevi_putovanja',
            name='vrsta_prevoza',
            field=models.CharField(default=2, max_length=100),
            preserve_default=False,
        ),
    ]
