from django.db.models import Count

from netbox.views import generic
from utilities.views import ViewTab, register_model_view

from . import filtersets, forms, tables
from .models import (
    BusinessCapability,
    Service,
    ServiceAsset,
    ServiceDependency,
    ServicePortfolio,
    ServicePortfolioMember,
)

# ------------------------------------------------------------------------
# Service
# ------------------------------------------------------------------------


@register_model_view(Service, 'list', path='', detail=False)
class ServiceListView(generic.ObjectListView):
    queryset = Service.objects.annotate(
        dependency_count=Count('outbound_dependencies', distinct=True),
        asset_count=Count('assets', distinct=True),
    )
    table = tables.ServiceTable
    filterset = filtersets.ServiceFilterSet
    filterset_form = forms.ServiceFilterForm


@register_model_view(Service)
class ServiceView(generic.ObjectView):
    queryset = Service.objects.all()

    def get_extra_context(self, request, instance):
        dependencies = instance.outbound_dependencies.select_related('depends_on')
        dependents = instance.dependents.select_related('service')
        assets = instance.assets.select_related('asset_type')
        return {
            'dependencies': dependencies,
            'dependents': dependents,
            'assets': assets,
        }


@register_model_view(Service, 'add', detail=False)
@register_model_view(Service, 'edit')
class ServiceEditView(generic.ObjectEditView):
    queryset = Service.objects.all()
    form = forms.ServiceForm


@register_model_view(Service, 'delete')
class ServiceDeleteView(generic.ObjectDeleteView):
    queryset = Service.objects.all()


@register_model_view(Service, 'bulk_import', path='import', detail=False)
class ServiceBulkImportView(generic.BulkImportView):
    queryset = Service.objects.all()
    model_form = forms.ServiceImportForm


@register_model_view(Service, 'bulk_edit', path='edit', detail=False)
class ServiceBulkEditView(generic.BulkEditView):
    queryset = Service.objects.all()
    filterset = filtersets.ServiceFilterSet
    table = tables.ServiceTable
    form = forms.ServiceBulkEditForm


@register_model_view(Service, 'bulk_delete', path='delete', detail=False)
class ServiceBulkDeleteView(generic.BulkDeleteView):
    queryset = Service.objects.all()
    filterset = filtersets.ServiceFilterSet
    table = tables.ServiceTable


@register_model_view(Service, name='dependencies', path='dependencies')
class ServiceDependenciesView(generic.ObjectChildrenView):
    queryset = Service.objects.all()
    child_model = ServiceDependency
    table = tables.ServiceDependencyTable
    filterset = filtersets.ServiceDependencyFilterSet
    tab = ViewTab(
        label='Dependencies',
        badge=lambda obj: obj.outbound_dependencies.count(),
        permission='netbox_itsm.view_servicedependency',
        weight=500,
    )

    def get_children(self, request, parent):
        return ServiceDependency.objects.filter(service=parent).select_related('depends_on')


@register_model_view(Service, name='assets', path='assets')
class ServiceAssetsView(generic.ObjectChildrenView):
    queryset = Service.objects.all()
    child_model = ServiceAsset
    table = tables.ServiceAssetTable
    filterset = filtersets.ServiceAssetFilterSet
    tab = ViewTab(
        label='Assets',
        badge=lambda obj: obj.assets.count(),
        permission='netbox_itsm.view_serviceasset',
        weight=600,
    )

    def get_children(self, request, parent):
        return ServiceAsset.objects.filter(service=parent).select_related('asset_type')


# ------------------------------------------------------------------------
# ServiceDependency
# ------------------------------------------------------------------------


@register_model_view(ServiceDependency, 'list', path='', detail=False)
class ServiceDependencyListView(generic.ObjectListView):
    queryset = ServiceDependency.objects.select_related('service', 'depends_on')
    table = tables.ServiceDependencyTable
    filterset = filtersets.ServiceDependencyFilterSet
    filterset_form = forms.ServiceDependencyFilterForm


@register_model_view(ServiceDependency)
class ServiceDependencyView(generic.ObjectView):
    queryset = ServiceDependency.objects.all()


@register_model_view(ServiceDependency, 'add', detail=False)
@register_model_view(ServiceDependency, 'edit')
class ServiceDependencyEditView(generic.ObjectEditView):
    queryset = ServiceDependency.objects.all()
    form = forms.ServiceDependencyForm


@register_model_view(ServiceDependency, 'delete')
class ServiceDependencyDeleteView(generic.ObjectDeleteView):
    queryset = ServiceDependency.objects.all()


@register_model_view(ServiceDependency, 'bulk_import', path='import', detail=False)
class ServiceDependencyBulkImportView(generic.BulkImportView):
    queryset = ServiceDependency.objects.all()
    model_form = forms.ServiceDependencyImportForm


@register_model_view(ServiceDependency, 'bulk_edit', path='edit', detail=False)
class ServiceDependencyBulkEditView(generic.BulkEditView):
    queryset = ServiceDependency.objects.all()
    filterset = filtersets.ServiceDependencyFilterSet
    table = tables.ServiceDependencyTable
    form = forms.ServiceDependencyBulkEditForm


@register_model_view(ServiceDependency, 'bulk_delete', path='delete', detail=False)
class ServiceDependencyBulkDeleteView(generic.BulkDeleteView):
    queryset = ServiceDependency.objects.all()
    filterset = filtersets.ServiceDependencyFilterSet
    table = tables.ServiceDependencyTable


# ------------------------------------------------------------------------
# ServiceAsset
# ------------------------------------------------------------------------


@register_model_view(ServiceAsset, 'list', path='', detail=False)
class ServiceAssetListView(generic.ObjectListView):
    queryset = ServiceAsset.objects.select_related('service', 'asset_type')
    table = tables.ServiceAssetTable
    filterset = filtersets.ServiceAssetFilterSet
    filterset_form = forms.ServiceAssetFilterForm


@register_model_view(ServiceAsset)
class ServiceAssetView(generic.ObjectView):
    queryset = ServiceAsset.objects.all()


@register_model_view(ServiceAsset, 'add', detail=False)
@register_model_view(ServiceAsset, 'edit')
class ServiceAssetEditView(generic.ObjectEditView):
    queryset = ServiceAsset.objects.all()
    form = forms.ServiceAssetForm


@register_model_view(ServiceAsset, 'delete')
class ServiceAssetDeleteView(generic.ObjectDeleteView):
    queryset = ServiceAsset.objects.all()


@register_model_view(ServiceAsset, 'bulk_import', path='import', detail=False)
class ServiceAssetBulkImportView(generic.BulkImportView):
    queryset = ServiceAsset.objects.all()
    model_form = forms.ServiceAssetImportForm


@register_model_view(ServiceAsset, 'bulk_edit', path='edit', detail=False)
class ServiceAssetBulkEditView(generic.BulkEditView):
    queryset = ServiceAsset.objects.all()
    filterset = filtersets.ServiceAssetFilterSet
    table = tables.ServiceAssetTable
    form = forms.ServiceAssetBulkEditForm


@register_model_view(ServiceAsset, 'bulk_delete', path='delete', detail=False)
class ServiceAssetBulkDeleteView(generic.BulkDeleteView):
    queryset = ServiceAsset.objects.all()
    filterset = filtersets.ServiceAssetFilterSet
    table = tables.ServiceAssetTable


# ------------------------------------------------------------------------
# ServicePortfolio
# ------------------------------------------------------------------------


@register_model_view(ServicePortfolio, 'list', path='', detail=False)
class ServicePortfolioListView(generic.ObjectListView):
    queryset = ServicePortfolio.objects.annotate(
        member_count=Count('portfolio_memberships', distinct=True),
    )
    table = tables.ServicePortfolioTable
    filterset = filtersets.ServicePortfolioFilterSet
    filterset_form = forms.ServicePortfolioFilterForm


@register_model_view(ServicePortfolio)
class ServicePortfolioView(generic.ObjectView):
    queryset = ServicePortfolio.objects.all()

    def get_extra_context(self, request, instance):
        members = instance.portfolio_memberships.select_related('service')
        capabilities = instance.capabilities.select_related('parent_capability')
        return {
            'members': members,
            'capabilities': capabilities,
            'sla_compliance_summary': instance.get_sla_compliance_summary(),
        }


@register_model_view(ServicePortfolio, 'add', detail=False)
@register_model_view(ServicePortfolio, 'edit')
class ServicePortfolioEditView(generic.ObjectEditView):
    queryset = ServicePortfolio.objects.all()
    form = forms.ServicePortfolioForm


@register_model_view(ServicePortfolio, 'delete')
class ServicePortfolioDeleteView(generic.ObjectDeleteView):
    queryset = ServicePortfolio.objects.all()


@register_model_view(ServicePortfolio, 'bulk_import', path='import', detail=False)
class ServicePortfolioBulkImportView(generic.BulkImportView):
    queryset = ServicePortfolio.objects.all()
    model_form = forms.ServicePortfolioImportForm


@register_model_view(ServicePortfolio, 'bulk_edit', path='edit', detail=False)
class ServicePortfolioBulkEditView(generic.BulkEditView):
    queryset = ServicePortfolio.objects.all()
    filterset = filtersets.ServicePortfolioFilterSet
    table = tables.ServicePortfolioTable
    form = forms.ServicePortfolioBulkEditForm


@register_model_view(ServicePortfolio, 'bulk_delete', path='delete', detail=False)
class ServicePortfolioBulkDeleteView(generic.BulkDeleteView):
    queryset = ServicePortfolio.objects.all()
    filterset = filtersets.ServicePortfolioFilterSet
    table = tables.ServicePortfolioTable


@register_model_view(ServicePortfolio, name='members', path='members')
class ServicePortfolioMembersView(generic.ObjectChildrenView):
    queryset = ServicePortfolio.objects.all()
    child_model = ServicePortfolioMember
    table = tables.ServicePortfolioMemberTable
    filterset = filtersets.ServicePortfolioMemberFilterSet
    tab = ViewTab(
        label='Members',
        badge=lambda obj: obj.portfolio_memberships.count(),
        permission='netbox_itsm.view_serviceportfoliomember',
        weight=500,
    )

    def get_children(self, request, parent):
        return ServicePortfolioMember.objects.filter(portfolio=parent).select_related('service')


@register_model_view(ServicePortfolio, name='capabilities', path='capabilities')
class ServicePortfolioCapabilitiesView(generic.ObjectChildrenView):
    queryset = ServicePortfolio.objects.all()
    child_model = BusinessCapability
    table = tables.BusinessCapabilityTable
    filterset = filtersets.BusinessCapabilityFilterSet
    tab = ViewTab(
        label='Capabilities',
        badge=lambda obj: obj.capabilities.count(),
        permission='netbox_itsm.view_businesscapability',
        weight=600,
    )

    def get_children(self, request, parent):
        return BusinessCapability.objects.filter(portfolio=parent).select_related('parent_capability')


# ------------------------------------------------------------------------
# ServicePortfolioMember
# ------------------------------------------------------------------------


@register_model_view(ServicePortfolioMember, 'list', path='', detail=False)
class ServicePortfolioMemberListView(generic.ObjectListView):
    queryset = ServicePortfolioMember.objects.select_related('portfolio', 'service')
    table = tables.ServicePortfolioMemberTable
    filterset = filtersets.ServicePortfolioMemberFilterSet
    filterset_form = forms.ServicePortfolioMemberFilterForm


@register_model_view(ServicePortfolioMember)
class ServicePortfolioMemberView(generic.ObjectView):
    queryset = ServicePortfolioMember.objects.all()


@register_model_view(ServicePortfolioMember, 'add', detail=False)
@register_model_view(ServicePortfolioMember, 'edit')
class ServicePortfolioMemberEditView(generic.ObjectEditView):
    queryset = ServicePortfolioMember.objects.all()
    form = forms.ServicePortfolioMemberForm


@register_model_view(ServicePortfolioMember, 'delete')
class ServicePortfolioMemberDeleteView(generic.ObjectDeleteView):
    queryset = ServicePortfolioMember.objects.all()


@register_model_view(ServicePortfolioMember, 'bulk_import', path='import', detail=False)
class ServicePortfolioMemberBulkImportView(generic.BulkImportView):
    queryset = ServicePortfolioMember.objects.all()
    model_form = forms.ServicePortfolioMemberImportForm


@register_model_view(ServicePortfolioMember, 'bulk_edit', path='edit', detail=False)
class ServicePortfolioMemberBulkEditView(generic.BulkEditView):
    queryset = ServicePortfolioMember.objects.all()
    filterset = filtersets.ServicePortfolioMemberFilterSet
    table = tables.ServicePortfolioMemberTable
    form = forms.ServicePortfolioMemberBulkEditForm


@register_model_view(ServicePortfolioMember, 'bulk_delete', path='delete', detail=False)
class ServicePortfolioMemberBulkDeleteView(generic.BulkDeleteView):
    queryset = ServicePortfolioMember.objects.all()
    filterset = filtersets.ServicePortfolioMemberFilterSet
    table = tables.ServicePortfolioMemberTable


# ------------------------------------------------------------------------
# BusinessCapability
# ------------------------------------------------------------------------


@register_model_view(BusinessCapability, 'list', path='', detail=False)
class BusinessCapabilityListView(generic.ObjectListView):
    queryset = BusinessCapability.objects.annotate(
        supported_service_count=Count('supported_services', distinct=True),
    ).select_related('portfolio', 'parent_capability')
    table = tables.BusinessCapabilityTable
    filterset = filtersets.BusinessCapabilityFilterSet
    filterset_form = forms.BusinessCapabilityFilterForm


@register_model_view(BusinessCapability)
class BusinessCapabilityView(generic.ObjectView):
    queryset = BusinessCapability.objects.all()

    def get_extra_context(self, request, instance):
        return {
            'supported_services': instance.supported_services.all(),
            'child_capabilities': instance.child_capabilities.all(),
        }


@register_model_view(BusinessCapability, 'add', detail=False)
@register_model_view(BusinessCapability, 'edit')
class BusinessCapabilityEditView(generic.ObjectEditView):
    queryset = BusinessCapability.objects.all()
    form = forms.BusinessCapabilityForm


@register_model_view(BusinessCapability, 'delete')
class BusinessCapabilityDeleteView(generic.ObjectDeleteView):
    queryset = BusinessCapability.objects.all()


@register_model_view(BusinessCapability, 'bulk_import', path='import', detail=False)
class BusinessCapabilityBulkImportView(generic.BulkImportView):
    queryset = BusinessCapability.objects.all()
    model_form = forms.BusinessCapabilityImportForm


@register_model_view(BusinessCapability, 'bulk_edit', path='edit', detail=False)
class BusinessCapabilityBulkEditView(generic.BulkEditView):
    queryset = BusinessCapability.objects.all()
    filterset = filtersets.BusinessCapabilityFilterSet
    table = tables.BusinessCapabilityTable
    form = forms.BusinessCapabilityBulkEditForm


@register_model_view(BusinessCapability, 'bulk_delete', path='delete', detail=False)
class BusinessCapabilityBulkDeleteView(generic.BulkDeleteView):
    queryset = BusinessCapability.objects.all()
    filterset = filtersets.BusinessCapabilityFilterSet
    table = tables.BusinessCapabilityTable
