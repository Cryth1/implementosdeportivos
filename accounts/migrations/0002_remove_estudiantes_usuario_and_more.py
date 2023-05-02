# Generated by Django 4.2 on 2023-04-26 06:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="estudiantes",
            name="Usuario",
        ),
        migrations.RemoveField(
            model_name="funcionarios",
            name="Usuario",
        ),
        migrations.AddField(
            model_name="customuser",
            name="codigo_usuario",
            field=models.CharField(
                default="0000",
                max_length=20,
                unique=True,
                verbose_name="codigo de usuario",
            ),
        ),
        migrations.AddField(
            model_name="customuser",
            name="nombre",
            field=models.CharField(default="", max_length=20, verbose_name="nombre"),
        ),
        migrations.AddField(
            model_name="customuser",
            name="rol",
            field=models.CharField(
                choices=[("ESTUDIANTE", "Estudiante"), ("FUNCIONARIO", "Funcionario")],
                default="ESTUDIANTE",
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="devoluciones",
            name="IDestudiante",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AlterField(
            model_name="multas",
            name="IdEstudiantes",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AlterField(
            model_name="prestamos",
            name="IdEstudiante",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.DeleteModel(
            name="Administradores",
        ),
        migrations.DeleteModel(
            name="Estudiantes",
        ),
        migrations.DeleteModel(
            name="Funcionarios",
        ),
        migrations.DeleteModel(
            name="Usuarios",
        ),
    ]