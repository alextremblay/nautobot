# Generated by Django 3.1.7 on 2021-04-01 06:35

import uuid

import django.core.serializers.json
import django.core.validators
import django.db.models.deletion
import taggit.managers
from django.db import migrations, models

import nautobot.core.fields
import nautobot.core.models.utils
import nautobot.core.ordering
import nautobot.dcim.fields
import nautobot.extras.models.statuses
import nautobot.extras.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("tenancy", "0001_initial"),
        ("dcim", "0003_initial_part_3"),
        ("extras", "0002_initial_part_2"),
        ("ipam", "0001_initial_part_1"),
    ]

    operations = [
        migrations.CreateModel(
            name="Cluster",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("created", models.DateField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "_custom_field_data",
                    models.JSONField(blank=True, default=dict, encoder=django.core.serializers.json.DjangoJSONEncoder),
                ),
                ("name", models.CharField(max_length=100, unique=True)),
                ("comments", models.TextField(blank=True)),
            ],
            options={
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="ClusterGroup",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("created", models.DateField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "_custom_field_data",
                    models.JSONField(blank=True, default=dict, encoder=django.core.serializers.json.DjangoJSONEncoder),
                ),
                ("name", models.CharField(max_length=100, unique=True)),
                ("slug", models.SlugField(max_length=100, unique=True)),
                ("description", models.CharField(blank=True, max_length=200)),
            ],
            options={
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="ClusterType",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("created", models.DateField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "_custom_field_data",
                    models.JSONField(blank=True, default=dict, encoder=django.core.serializers.json.DjangoJSONEncoder),
                ),
                ("name", models.CharField(max_length=100, unique=True)),
                ("slug", models.SlugField(max_length=100, unique=True)),
                ("description", models.CharField(blank=True, max_length=200)),
            ],
            options={
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="VirtualMachine",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("created", models.DateField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "_custom_field_data",
                    models.JSONField(blank=True, default=dict, encoder=django.core.serializers.json.DjangoJSONEncoder),
                ),
                (
                    "local_context_data",
                    models.JSONField(blank=True, encoder=django.core.serializers.json.DjangoJSONEncoder, null=True),
                ),
                ("local_context_data_owner_object_id", models.UUIDField(blank=True, default=None, null=True)),
                ("name", models.CharField(max_length=64)),
                ("vcpus", models.PositiveSmallIntegerField(blank=True, null=True)),
                ("memory", models.PositiveIntegerField(blank=True, null=True)),
                ("disk", models.PositiveIntegerField(blank=True, null=True)),
                ("comments", models.TextField(blank=True)),
                (
                    "cluster",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="virtual_machines",
                        to="virtualization.cluster",
                    ),
                ),
                (
                    "local_context_data_owner_content_type",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        limit_choices_to=nautobot.extras.utils.FeatureQuery("config_context_owners"),
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="contenttypes.contenttype",
                    ),
                ),
                (
                    "platform",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="virtual_machines",
                        to="dcim.platform",
                    ),
                ),
                (
                    "primary_ip4",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="ipam.ipaddress",
                    ),
                ),
                (
                    "primary_ip6",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="ipam.ipaddress",
                    ),
                ),
                (
                    "role",
                    models.ForeignKey(
                        blank=True,
                        limit_choices_to={"vm_role": True},
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="virtual_machines",
                        to="dcim.devicerole",
                    ),
                ),
                (
                    "status",
                    nautobot.extras.models.statuses.StatusField(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="virtualization_virtualmachine_related",
                        to="extras.status",
                    ),
                ),
                ("tags", taggit.managers.TaggableManager(through="extras.TaggedItem", to="extras.Tag")),
                (
                    "tenant",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="virtual_machines",
                        to="tenancy.tenant",
                    ),
                ),
            ],
            options={
                "ordering": ("name",),
                "unique_together": {("cluster", "tenant", "name")},
            },
        ),
        migrations.AddField(
            model_name="cluster",
            name="group",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="clusters",
                to="virtualization.clustergroup",
            ),
        ),
        migrations.AddField(
            model_name="cluster",
            name="site",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="clusters",
                to="dcim.site",
            ),
        ),
        migrations.AddField(
            model_name="cluster",
            name="tags",
            field=taggit.managers.TaggableManager(through="extras.TaggedItem", to="extras.Tag"),
        ),
        migrations.AddField(
            model_name="cluster",
            name="tenant",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="clusters",
                to="tenancy.tenant",
            ),
        ),
        migrations.AddField(
            model_name="cluster",
            name="type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, related_name="clusters", to="virtualization.clustertype"
            ),
        ),
        migrations.CreateModel(
            name="VMInterface",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
                (
                    "_custom_field_data",
                    models.JSONField(blank=True, default=dict, encoder=django.core.serializers.json.DjangoJSONEncoder),
                ),
                ("enabled", models.BooleanField(default=True)),
                ("mac_address", nautobot.dcim.fields.MACAddressCharField(blank=True, null=True)),
                (
                    "mtu",
                    models.PositiveIntegerField(
                        blank=True,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(65536),
                        ],
                    ),
                ),
                ("mode", models.CharField(blank=True, max_length=50)),
                ("name", models.CharField(max_length=64)),
                (
                    "_name",
                    nautobot.core.fields.NaturalOrderingField(
                        "name",
                        blank=True,
                        max_length=100,
                        naturalize_function=nautobot.core.ordering.naturalize_interface,
                    ),
                ),
                ("description", models.CharField(blank=True, max_length=200)),
                (
                    "tagged_vlans",
                    models.ManyToManyField(blank=True, related_name="vminterfaces_as_tagged", to="ipam.VLAN"),
                ),
                (
                    "tags",
                    taggit.managers.TaggableManager(
                        related_name="vminterface", through="extras.TaggedItem", to="extras.Tag"
                    ),
                ),
                (
                    "untagged_vlan",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="vminterfaces_as_untagged",
                        to="ipam.vlan",
                    ),
                ),
                (
                    "virtual_machine",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="interfaces",
                        to="virtualization.virtualmachine",
                    ),
                ),
            ],
            options={
                "verbose_name": "interface",
                "ordering": ("virtual_machine", nautobot.core.models.utils.CollateAsChar("_name")),
                "unique_together": {("virtual_machine", "name")},
            },
        ),
    ]
