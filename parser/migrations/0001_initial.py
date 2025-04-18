# Generated by Django 5.2 on 2025-04-09 18:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Province",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("cn_name", models.CharField(max_length=200, unique=True, verbose_name="name in Chinese")),
                ("eng_name", models.CharField(max_length=200, verbose_name="name in English")),
                (
                    "popularity",
                    models.PositiveIntegerField(
                        default=0, help_text="Fills in automatically", verbose_name="province popularity"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SpecialWord",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("cn_name", models.CharField(max_length=200, unique=True, verbose_name="name in Chinese")),
                ("eng_name", models.CharField(max_length=200, verbose_name="name in English")),
            ],
        ),
        migrations.CreateModel(
            name="AddressObject",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("cn_name", models.CharField(max_length=200, unique=True, verbose_name="name in Chinese")),
                ("eng_name", models.CharField(max_length=200, verbose_name="name in English")),
                ("is_parent_item", models.BooleanField(verbose_name="parent items or not")),
                (
                    "hierarchy",
                    models.PositiveIntegerField(
                        help_text="Select object's hierarchy in address. For parent items only!",
                        verbose_name="object hierarchy",
                    ),
                ),
                (
                    "parent_item_1",
                    models.ForeignKey(
                        blank=True,
                        help_text="Select the 1st parent item according to address hierarchy",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="cities",
                        to="parser.addressobject",
                        verbose_name="1st parent item",
                    ),
                ),
                (
                    "parent_item_2",
                    models.ForeignKey(
                        blank=True,
                        help_text="Select the 2nd parent item according to address hierarchy",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="districts",
                        to="parser.addressobject",
                        verbose_name="2nd parent item",
                    ),
                ),
                (
                    "parent_item_3",
                    models.ForeignKey(
                        blank=True,
                        help_text="Select the 3rd parent item according to address hierarchy",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="streets",
                        to="parser.addressobject",
                        verbose_name="3rd parent item",
                    ),
                ),
                (
                    "parent_item_4",
                    models.ForeignKey(
                        blank=True,
                        help_text="Select the 4th parent item according to address hierarchy",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="houses",
                        to="parser.addressobject",
                        verbose_name="4th parent item",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="City",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("cn_name", models.CharField(max_length=200, unique=True, verbose_name="name in Chinese")),
                ("eng_name", models.CharField(max_length=200, verbose_name="name in English")),
                (
                    "popularity",
                    models.PositiveIntegerField(
                        default=0, help_text="Fills in automatically", verbose_name="province popularity"
                    ),
                ),
                (
                    "province",
                    models.ForeignKey(
                        help_text="Select the 1st parent item according to address hierarchy",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="cities",
                        to="parser.province",
                        verbose_name="1st parent item",
                    ),
                ),
            ],
        ),
    ]
