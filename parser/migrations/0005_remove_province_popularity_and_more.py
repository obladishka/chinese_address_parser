# Generated by Django 5.2 on 2025-04-10 18:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("parser", "0004_specialword_popularity"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="province",
            name="popularity",
        ),
        migrations.RemoveField(
            model_name="specialword",
            name="popularity",
        ),
        migrations.DeleteModel(
            name="City",
        ),
    ]
