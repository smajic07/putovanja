# Generated by Django 3.2.5 on 2022-06-07 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login_i_registracija', '0007_auto_20220607_0201'),
    ]

    operations = [
        migrations.AddField(
            model_name='zahtjevi_putovanja',
            name='latituda',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='zahtjevi_putovanja',
            name='longituda',
            field=models.FloatField(null=True),
        ),
    ]
