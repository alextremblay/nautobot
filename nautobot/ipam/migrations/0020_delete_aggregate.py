# Generated by Django 3.2.16 on 2023-02-10 22:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("ipam", "0019_aggregate_to_prefix_data_migration"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Aggregate",
        ),
    ]
