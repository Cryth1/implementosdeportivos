# Generated by Django 4.2 on 2023-05-18 04:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        (
            "estudiante",
            "0003_rename_idcategoria_categoriasimplementos_id_categoria_and_more",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="ClubDeportivo",
            fields=[
                ("id_club", models.AutoField(primary_key=True, serialize=False)),
                ("nombre", models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name="categoriasimplementos",
            name="club_deportivo",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="estudiante.clubdeportivo",
            ),
            preserve_default=False,
        ),
    ]
