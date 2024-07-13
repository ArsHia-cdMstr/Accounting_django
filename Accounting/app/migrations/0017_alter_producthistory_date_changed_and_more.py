# Generated by Django 5.0.6 on 2024-07-13 07:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0016_product_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="producthistory",
            name="date_changed",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name="producthistory",
            name="product",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="product_history",
                to="app.product",
            ),
        ),
        migrations.AlterField(
            model_name="producthistory",
            name="quantity_change",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="producthistory",
            name="remaining_quantity",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
