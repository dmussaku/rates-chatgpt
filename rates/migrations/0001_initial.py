# Generated by Django 4.1.7 on 2023-03-17 15:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200)),
                ("description", models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Port",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("country_code", models.CharField(max_length=10)),
                ("code", models.CharField(max_length=20)),
                ("name", models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name="Surcharge",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2, max_digits=19, verbose_name="Rate price"
                    ),
                ),
                ("valid_from", models.DateTimeField()),
                ("valid_until", models.DateTimeField()),
                (
                    "carrier_id",
                    models.CharField(
                        choices=[
                            ("COSU", "COSCO"),
                            ("MSCU", "Mediterranean Shipping Company"),
                            ("HLCU", "Hapag-Lloyd"),
                            ("MAEU", "Maersk"),
                        ],
                        max_length=10,
                    ),
                ),
                (
                    "surcharge_type",
                    models.CharField(
                        choices=[
                            ("danger", "Surcharge for Dangerous Goods"),
                            ("customs", "Surcharge for Customs Fee"),
                        ],
                        max_length=10,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="MainRate",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2, max_digits=19, verbose_name="Rate price"
                    ),
                ),
                ("valid_from", models.DateTimeField()),
                ("valid_until", models.DateTimeField()),
                (
                    "carrier_id",
                    models.CharField(
                        choices=[
                            ("COSU", "COSCO"),
                            ("MSCU", "Mediterranean Shipping Company"),
                            ("HLCU", "Hapag-Lloyd"),
                            ("MAEU", "Maersk"),
                        ],
                        max_length=10,
                    ),
                ),
                (
                    "container_type",
                    models.CharField(
                        choices=[
                            ("22GP", "20 foot container"),
                            ("42GP", "Standart 40 foot container"),
                            ("45GP", "40 foot high cube container"),
                        ],
                        max_length=10,
                    ),
                ),
                (
                    "pod",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="pod",
                        to="rates.port",
                    ),
                ),
                (
                    "pol",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="pol",
                        to="rates.port",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
