# Generated by Django 5.0.6 on 2024-07-11 09:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0005_bankaccount_bank_name_alter_bankaccount_account_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="bankaccount",
            name="account_number",
            field=models.PositiveIntegerField(blank=True, null=True, unique=True),
        ),
    ]
