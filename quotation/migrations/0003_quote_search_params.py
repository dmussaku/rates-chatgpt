# Generated by Django 4.1.7 on 2023-03-19 19:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("quotation", "0002_rename_quote_quotelineitem_quote_option"),
    ]

    operations = [
        migrations.AddField(
            model_name="quote",
            name="search_params",
            field=models.JSONField(blank=True, null=True),
        ),
    ]
