from django.db.models import Count

from netbox.views import generic
from utilities.views import ViewTab, register_model_view

from . import filtersets, forms, tables
from .models import Service, ServiceAsset, ServiceDependency

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
