from django.db.models import Count

from netbox.api.viewsets import NetBoxModelViewSet

from .. import filtersets
from ..models import Service, ServiceAsset, ServiceDependency
from .serializers import ServiceAssetSerializer, ServiceDependencySerializer, ServiceSerializer

__all__ = (
    'ServiceViewSet',
    'ServiceAssetViewSet',
    'ServiceDependencyViewSet',
)


class ServiceViewSet(NetBoxModelViewSet):
    queryset = Service.objects.prefetch_related('tags').annotate(
        dependency_count=Count('outbound_dependencies', distinct=True),
        asset_count=Count('assets', distinct=True),
    )
    serializer_class = ServiceSerializer
    filterset_class = filtersets.ServiceFilterSet


class ServiceDependencyViewSet(NetBoxModelViewSet):
    queryset = ServiceDependency.objects.select_related('service', 'depends_on').prefetch_related('tags')
    serializer_class = ServiceDependencySerializer
    filterset_class = filtersets.ServiceDependencyFilterSet


class ServiceAssetViewSet(NetBoxModelViewSet):
    queryset = ServiceAsset.objects.select_related('service', 'asset_type').prefetch_related('tags')
    serializer_class = ServiceAssetSerializer
    filterset_class = filtersets.ServiceAssetFilterSet
