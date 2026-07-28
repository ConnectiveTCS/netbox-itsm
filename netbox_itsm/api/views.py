from django.db.models import Count

from netbox.api.viewsets import NetBoxModelViewSet

from .. import filtersets
from ..models import (
    BusinessCapability,
    Service,
    ServiceAsset,
    ServiceDependency,
    ServicePortfolio,
    ServicePortfolioMember,
)
from .serializers import (
    BusinessCapabilitySerializer,
    ServiceAssetSerializer,
    ServiceDependencySerializer,
    ServicePortfolioMemberSerializer,
    ServicePortfolioSerializer,
    ServiceSerializer,
)

__all__ = (
    'BusinessCapabilityViewSet',
    'ServiceViewSet',
    'ServiceAssetViewSet',
    'ServiceDependencyViewSet',
    'ServicePortfolioViewSet',
    'ServicePortfolioMemberViewSet',
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


class ServicePortfolioViewSet(NetBoxModelViewSet):
    queryset = ServicePortfolio.objects.prefetch_related('tags').annotate(
        member_count=Count('portfolio_memberships', distinct=True),
    )
    serializer_class = ServicePortfolioSerializer
    filterset_class = filtersets.ServicePortfolioFilterSet


class ServicePortfolioMemberViewSet(NetBoxModelViewSet):
    queryset = ServicePortfolioMember.objects.select_related('portfolio', 'service').prefetch_related('tags')
    serializer_class = ServicePortfolioMemberSerializer
    filterset_class = filtersets.ServicePortfolioMemberFilterSet


class BusinessCapabilityViewSet(NetBoxModelViewSet):
    queryset = BusinessCapability.objects.select_related('portfolio', 'parent_capability').prefetch_related(
        'tags', 'supported_services',
    ).annotate(
        supported_service_count=Count('supported_services', distinct=True),
    )
    serializer_class = BusinessCapabilitySerializer
    filterset_class = filtersets.BusinessCapabilityFilterSet
