# Generated by Django 3.2.5 on 2022-06-08 00:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login_i_registracija', '0009_auto_20220608_0132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='putovanja',
            name='latituda',
            field=models.FloatField(default=1.5),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='putovanja',
            name='longituda',
            field=models.FloatField(default=1.5),
            preserve_default=False,
        ),
    ]
