# Generated by Django 5.0.7 on 2024-12-17 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sofom_project', '0003_datos_credito_fecha_otorgamiento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datos_credito',
            name='monto_prestamo',
            field=models.IntegerField(),
        ),
    ]