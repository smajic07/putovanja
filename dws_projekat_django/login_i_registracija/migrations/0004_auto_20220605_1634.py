# Generated by Django 3.2.5 on 2022-06-05 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login_i_registracija', '0003_zahtjevi_putovanja_vrsta_prevoza'),
    ]

    operations = [
        migrations.AddField(
            model_name='putovanja',
            name='opis_putovanja',
            field=models.CharField(default='eke', max_length=1000),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='putovanja',
            name='vrsta_prevoza',
            field=models.CharField(max_length=100),
        ),
    ]
