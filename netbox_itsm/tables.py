import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from netbox.tables import NetBoxTable, PrimaryModelTable, columns

from .models import (
    BusinessCapability,
    Service,
    ServiceAsset,
    ServiceDependency,
    ServicePortfolio,
    ServicePortfolioMember,
)


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


class ServicePortfolioTable(PrimaryModelTable):
    name = tables.Column(linkify=True)
    status = columns.ChoiceFieldColumn()
    tags = columns.TagColumn(url_name='plugins:netbox_itsm:serviceportfolio_list')
    member_count = tables.Column(
        accessor='portfolio_memberships__count',
        verbose_name=_('Services'),
    )

    class Meta(NetBoxTable.Meta):
        model = ServicePortfolio
        fields = (
            'pk', 'id', 'name', 'business_domain', 'status', 'portfolio_owner_contact', 'owner', 'description',
            'member_count', 'tags', 'created', 'last_updated',
        )
        default_columns = ('pk', 'name', 'business_domain', 'status', 'owner', 'member_count')


class ServicePortfolioMemberTable(PrimaryModelTable):
    portfolio = tables.Column(linkify=True)
    service = tables.Column(linkify=True)
    role = columns.ChoiceFieldColumn()
    tags = columns.TagColumn(url_name='plugins:netbox_itsm:serviceportfoliomember_list')

    class Meta(NetBoxTable.Meta):
        model = ServicePortfolioMember
        fields = (
            'pk', 'id', 'portfolio', 'service', 'role', 'contribution_percentage', 'owner', 'description', 'tags',
            'created', 'last_updated',
        )
        default_columns = ('pk', 'portfolio', 'service', 'role', 'contribution_percentage')


class BusinessCapabilityTable(PrimaryModelTable):
    name = tables.Column(linkify=True)
    portfolio = tables.Column(linkify=True)
    parent_capability = tables.Column(linkify=True)
    tags = columns.TagColumn(url_name='plugins:netbox_itsm:businesscapability_list')
    supported_service_count = tables.Column(
        accessor='supported_services__count',
        verbose_name=_('Services'),
    )

    class Meta(NetBoxTable.Meta):
        model = BusinessCapability
        fields = (
            'pk', 'id', 'name', 'portfolio', 'parent_capability', 'owner', 'description',
            'supported_service_count', 'tags', 'created', 'last_updated',
        )
        default_columns = ('pk', 'name', 'portfolio', 'parent_capability', 'supported_service_count')
