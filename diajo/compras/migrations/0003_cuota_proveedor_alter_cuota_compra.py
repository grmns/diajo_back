# Generated by Django 5.0.2 on 2024-05-25 06:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0002_cuota'),
    ]

    operations = [
        migrations.AddField(
            model_name='cuota',
            name='proveedor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='compras.proveedor'),
        ),
        migrations.AlterField(
            model_name='cuota',
            name='compra',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='compras.compra'),
        ),
    ]
