import django_filters
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

from netbox.filtersets import PrimaryModelFilterSet
from utilities.filtersets import register_filterset

from .choices import (
    ServiceAssetLinkTypeChoices,
    ServiceDependencyCriticalityChoices,
    ServiceDependencyTypeChoices,
    ServiceHealthChoices,
    ServiceStatusChoices,
    ServiceTierChoices,
    ServiceTypeChoices,
)
from .models import Service, ServiceAsset, ServiceDependency


@register_filterset
class ServiceFilterSet(PrimaryModelFilterSet):
    service_type = django_filters.MultipleChoiceFilter(choices=ServiceTypeChoices, null_value=None)
    status = django_filters.MultipleChoiceFilter(choices=ServiceStatusChoices, null_value=None)
    health_status = django_filters.MultipleChoiceFilter(choices=ServiceHealthChoices, null_value=None)
    tier_level = django_filters.MultipleChoiceFilter(choices=ServiceTierChoices, null_value=None)

    class Meta:
        model = Service
        fields = ('id', 'name', 'slug', 'sla_target', 'owner_contact', 'escalation_contact')

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value) |
            Q(description__icontains=value) |
            Q(comments__icontains=value) |
            Q(owner_contact__icontains=value)
        )


@register_filterset
class ServiceDependencyFilterSet(PrimaryModelFilterSet):
    service_id = django_filters.ModelMultipleChoiceFilter(
        field_name='service',
        queryset=Service.objects.all(),
        label='Service (ID)',
    )
    depends_on_id = django_filters.ModelMultipleChoiceFilter(
        field_name='depends_on',
        queryset=Service.objects.all(),
        label='Depends on (ID)',
    )
    relationship_type = django_filters.MultipleChoiceFilter(choices=ServiceDependencyTypeChoices, null_value=None)
    criticality = django_filters.MultipleChoiceFilter(choices=ServiceDependencyCriticalityChoices, null_value=None)

    class Meta:
        model = ServiceDependency
        fields = ('id',)

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(service__name__icontains=value) |
            Q(depends_on__name__icontains=value) |
            Q(description__icontains=value)
        )


@register_filterset
class ServiceAssetFilterSet(PrimaryModelFilterSet):
    service_id = django_filters.ModelMultipleChoiceFilter(
        field_name='service',
        queryset=Service.objects.all(),
        label='Service (ID)',
    )
    asset_type = django_filters.ModelChoiceFilter(
        queryset=ContentType.objects.all(),
    )
    link_type = django_filters.MultipleChoiceFilter(choices=ServiceAssetLinkTypeChoices, null_value=None)

    class Meta:
        model = ServiceAsset
        fields = ('id', 'asset_id')

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(service__name__icontains=value) |
            Q(description__icontains=value)
        )
