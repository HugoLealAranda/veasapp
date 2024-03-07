# Generated by Django 5.0.2 on 2024-03-07 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionPedidos', '0028_message'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tarea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('fecha_vencimiento', models.DateField()),
                ('completada', models.BooleanField(default=False)),
            ],
        ),
    ]
