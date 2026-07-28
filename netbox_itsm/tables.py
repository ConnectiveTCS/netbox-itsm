import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from netbox.tables import NetBoxTable, PrimaryModelTable, columns

from .models import Service, ServiceAsset, ServiceDependency


class ServiceTable(PrimaryModelTable):
    name = tables.Column(linkify=True)
    service_type = columns.ChoiceFieldColumn()
    status = columns.ChoiceFieldColumn()
    health_status = columns.ChoiceFieldColumn()
    tier_level = columns.ChoiceFieldColumn()
    tags = columns.TagColumn(url_name='plugins:netbox_itsm:service_list')
    dependency_count = tables.Column(
        accessor='outbound_dependencies__count',
        verbose_name=_('Dependencies'),
    )
    asset_count = tables.Column(
        accessor='assets__count',
        verbose_name=_('Assets'),
    )

    class Meta(NetBoxTable.Meta):
        model = Service
        fields = (
            'pk', 'id', 'name', 'service_type', 'status', 'health_status', 'tier_level', 'sla_target',
            'owner_contact', 'escalation_contact', 'owner', 'description', 'dependency_count', 'asset_count',
            'tags', 'created', 'last_updated',
        )
        default_columns = (
            'pk', 'name', 'service_type', 'status', 'health_status', 'tier_level', 'owner', 'sla_target',
        )


class ServiceDependencyTable(PrimaryModelTable):
    service = tables.Column(linkify=True)
    depends_on = tables.Column(linkify=True)
    relationship_type = columns.ChoiceFieldColumn()
    criticality = columns.ChoiceFieldColumn()
    tags = columns.TagColumn(url_name='plugins:netbox_itsm:servicedependency_list')

    class Meta(NetBoxTable.Meta):
        model = ServiceDependency
        fields = (
            'pk', 'id', 'service', 'depends_on', 'relationship_type', 'criticality', 'owner', 'description',
            'tags', 'created', 'last_updated',
        )
        default_columns = ('pk', 'service', 'depends_on', 'relationship_type', 'criticality')


class ServiceAssetTable(PrimaryModelTable):
    service = tables.Column(linkify=True)
    asset_type = columns.ContentTypeColumn(verbose_name=_('Asset Type'))
    asset = tables.Column(accessor='asset', linkify=True, verbose_name=_('Asset'), orderable=False)
    link_type = columns.ChoiceFieldColumn()
    tags = columns.TagColumn(url_name='plugins:netbox_itsm:serviceasset_list')

    class Meta(NetBoxTable.Meta):
        model = ServiceAsset
        fields = (
            'pk', 'id', 'service', 'asset_type', 'asset', 'link_type', 'owner', 'description', 'tags',
            'created', 'last_updated',
        )
        default_columns = ('pk', 'service', 'asset_type', 'asset', 'link_type')
