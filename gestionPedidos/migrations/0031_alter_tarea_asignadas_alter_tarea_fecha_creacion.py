# Generated by Django 5.0.2 on 2024-03-07 07:30

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionPedidos', '0030_tarea_asignadas_tarea_fecha_creacion'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='tarea',
            name='asignadas',
            field=models.ManyToManyField(blank=True, related_name='tareas_asignadas', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='tarea',
            name='fecha_creacion',
            field=models.DateTimeField(null=True),
        ),
    ]