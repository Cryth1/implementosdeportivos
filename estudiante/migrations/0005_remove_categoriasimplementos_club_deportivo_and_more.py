# Generated by Django 4.2 on 2023-05-18 04:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("estudiante", "0004_clubdeportivo_categoriasimplementos_club_deportivo"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="categoriasimplementos",
            name="club_deportivo",
        ),
        migrations.DeleteModel(
            name="ClubDeportivo",
        ),
    ]
