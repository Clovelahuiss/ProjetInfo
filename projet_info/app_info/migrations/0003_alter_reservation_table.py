# Generated by Django 4.1.6 on 2024-01-29 15:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_info', '0002_reservation_table_delete_evenement_reservation_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='table',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_info.table'),
        ),
    ]