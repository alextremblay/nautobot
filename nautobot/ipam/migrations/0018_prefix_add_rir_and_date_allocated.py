# Generated by Django 3.2.16 on 2023-02-10 16:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("ipam", "0017_prefix_remove_is_pool"),
    ]

    operations = [
        migrations.AddField(
            model_name="prefix",
            name="date_allocated",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="prefix",
            name="rir",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="prefixes",
                to="ipam.rir",
            ),
        ),
    ]
