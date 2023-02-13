from rest_framework.routers import APIRootView

from nautobot.core.models.querysets import count_related
from nautobot.dcim.models import Device
from nautobot.extras.api.views import (
    ConfigContextQuerySetMixin,
    NautobotModelViewSet,
    ModelViewSet,
    NotesViewSetMixin,
)
from nautobot.virtualization import filters
from nautobot.virtualization.models import (
    Cluster,
    ClusterGroup,
    ClusterType,
    VirtualMachine,
    VMInterface,
)
from . import serializers


class VirtualizationRootView(APIRootView):
    """
    Virtualization API root view
    """

    def get_view_name(self):
        return "Virtualization"


#
# Clusters
#


class ClusterTypeViewSet(NautobotModelViewSet):
    queryset = ClusterType.objects.annotate(cluster_count=count_related(Cluster, "cluster_type"))
    serializer_class = serializers.ClusterTypeSerializer
    filterset_class = filters.ClusterTypeFilterSet


class ClusterGroupViewSet(NautobotModelViewSet):
    queryset = ClusterGroup.objects.annotate(cluster_count=count_related(Cluster, "cluster_group"))
    serializer_class = serializers.ClusterGroupSerializer
    filterset_class = filters.ClusterGroupFilterSet


class ClusterViewSet(NautobotModelViewSet):
    queryset = (
        Cluster.objects.select_related("cluster_type", "cluster_group", "tenant", "site")
        .prefetch_related("tags")
        .annotate(
            device_count=count_related(Device, "cluster"),
            virtualmachine_count=count_related(VirtualMachine, "cluster"),
        )
    )
    serializer_class = serializers.ClusterSerializer
    filterset_class = filters.ClusterFilterSet


#
# Virtual machines
#


class VirtualMachineViewSet(ConfigContextQuerySetMixin, NautobotModelViewSet):
    queryset = VirtualMachine.objects.select_related(
        "cluster__site",
        "platform",
        "primary_ip4",
        "primary_ip6",
        "status",
        "role",
        "tenant",
    ).prefetch_related("tags")
    filterset_class = filters.VirtualMachineFilterSet

    def get_serializer_class(self):
        """
        Select the specific serializer based on the request context.

        If the `brief` query param equates to True, return the NestedVirtualMachineSerializer

        If the `exclude` query param includes `config_context` as a value, return the VirtualMachineSerializer

        Else, return the VirtualMachineWithConfigContextSerializer
        """

        request = self.get_serializer_context()["request"]
        if request is not None and request.query_params.get("brief", False):
            return serializers.NestedVirtualMachineSerializer

        elif request is not None and "config_context" in request.query_params.get("exclude", []):
            return serializers.VirtualMachineSerializer

        return serializers.VirtualMachineWithConfigContextSerializer


class VMInterfaceViewSet(ModelViewSet, NotesViewSetMixin):
    queryset = VMInterface.objects.select_related(
        "virtual_machine",
        "parent_interface",
        "bridge",
        "status",
    ).prefetch_related("tags", "tagged_vlans")
    serializer_class = serializers.VMInterfaceSerializer
    filterset_class = filters.VMInterfaceFilterSet
    # v2 TODO(jathan): Replace prefetch_related with select_related
    brief_prefetch_fields = ["virtual_machine"]
