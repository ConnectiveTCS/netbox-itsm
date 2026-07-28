from django import forms
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _

from netbox.forms import (
    NetBoxModelBulkEditForm,
    NetBoxModelFilterSetForm,
    NetBoxModelImportForm,
    PrimaryModelForm,
)
from utilities.forms.fields import (
    CommentField,
    ContentTypeChoiceField,
    CSVContentTypeField,
    CSVModelChoiceField,
    DynamicModelChoiceField,
    SlugField,
)
from utilities.forms.rendering import FieldSet

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

#: Infrastructure object types that a Service can be linked to.
ASSET_CONTENT_TYPES = models.Q(app_label='dcim', model__in=('device', 'interface', 'module')) | \
    models.Q(app_label='virtualization', model='virtualmachine') | \
    models.Q(app_label='circuits', model='circuit')


# ------------------------------------------------------------------------
# Service
# ------------------------------------------------------------------------

class ServiceForm(PrimaryModelForm):
    slug = SlugField(slug_source='name')
    comments = CommentField()

    fieldsets = (
        FieldSet(
            'name', 'slug', 'service_type', 'status', 'health_status', 'tier_level', 'owner', 'tags',
            name=_('Service'),
        ),
        FieldSet('sla_target', 'owner_contact', 'escalation_contact', name=_('SLA & Contacts')),
        FieldSet('description', name=_('Additional Details')),
    )

    class Meta:
        model = Service
        fields = (
            'name', 'slug', 'service_type', 'status', 'health_status', 'tier_level', 'sla_target',
            'owner_contact', 'escalation_contact', 'owner', 'description', 'comments', 'tags',
        )


class ServiceImportForm(NetBoxModelImportForm):
    service_type = forms.ChoiceField(choices=ServiceTypeChoices, required=False)
    status = forms.ChoiceField(choices=ServiceStatusChoices, required=False)
    health_status = forms.ChoiceField(choices=ServiceHealthChoices, required=False)
    tier_level = forms.ChoiceField(choices=ServiceTierChoices, required=False)

    class Meta:
        model = Service
        fields = (
            'name', 'slug', 'service_type', 'status', 'health_status', 'tier_level', 'sla_target',
            'owner_contact', 'escalation_contact', 'description', 'comments',
        )


class ServiceBulkEditForm(NetBoxModelBulkEditForm):
    service_type = forms.ChoiceField(choices=ServiceTypeChoices, required=False)
    status = forms.ChoiceField(choices=ServiceStatusChoices, required=False)
    health_status = forms.ChoiceField(choices=ServiceHealthChoices, required=False)
    tier_level = forms.ChoiceField(choices=ServiceTierChoices, required=False)
    sla_target = forms.CharField(max_length=20, required=False)
    owner_contact = forms.CharField(max_length=200, required=False)
    escalation_contact = forms.CharField(max_length=200, required=False)
    description = forms.CharField(max_length=200, required=False)
    comments = CommentField()

    model = Service
    fieldsets = (
        FieldSet('service_type', 'status', 'health_status', 'tier_level', name=_('Service')),
        FieldSet('sla_target', 'owner_contact', 'escalation_contact', name=_('SLA & Contacts')),
    )
    nullable_fields = ('sla_target', 'owner_contact', 'escalation_contact', 'description', 'comments')


class ServiceFilterForm(NetBoxModelFilterSetForm):
    model = Service
    fieldsets = (
        FieldSet('q', 'filter_id', 'tag'),
        FieldSet('service_type', 'status', 'health_status', 'tier_level', name=_('Attributes')),
    )
    service_type = forms.MultipleChoiceField(choices=ServiceTypeChoices, required=False)
    status = forms.MultipleChoiceField(choices=ServiceStatusChoices, required=False)
    health_status = forms.MultipleChoiceField(choices=ServiceHealthChoices, required=False)
    tier_level = forms.MultipleChoiceField(choices=ServiceTierChoices, required=False)


# ------------------------------------------------------------------------
# ServiceDependency
# ------------------------------------------------------------------------

class ServiceDependencyForm(PrimaryModelForm):
    service = DynamicModelChoiceField(queryset=Service.objects.all())
    depends_on = DynamicModelChoiceField(queryset=Service.objects.all())
    comments = CommentField()

    fieldsets = (
        FieldSet('service', 'depends_on', 'relationship_type', 'criticality', 'tags', name=_('Dependency')),
        FieldSet('description', name=_('Additional Details')),
    )

    class Meta:
        model = ServiceDependency
        fields = (
            'service', 'depends_on', 'relationship_type', 'criticality', 'owner', 'description', 'comments', 'tags',
        )


class ServiceDependencyImportForm(NetBoxModelImportForm):
    service = CSVModelChoiceField(
        queryset=Service.objects.all(),
        to_field_name='name',
        help_text=_('Dependent service'),
    )
    depends_on = CSVModelChoiceField(
        queryset=Service.objects.all(),
        to_field_name='name',
        help_text=_('Service depended upon'),
    )
    relationship_type = forms.ChoiceField(choices=ServiceDependencyTypeChoices, required=False)
    criticality = forms.ChoiceField(choices=ServiceDependencyCriticalityChoices, required=False)

    class Meta:
        model = ServiceDependency
        fields = ('service', 'depends_on', 'relationship_type', 'criticality', 'description', 'comments')


class ServiceDependencyBulkEditForm(NetBoxModelBulkEditForm):
    relationship_type = forms.ChoiceField(choices=ServiceDependencyTypeChoices, required=False)
    criticality = forms.ChoiceField(choices=ServiceDependencyCriticalityChoices, required=False)
    description = forms.CharField(max_length=200, required=False)
    comments = CommentField()

    model = ServiceDependency
    fieldsets = (
        FieldSet('relationship_type', 'criticality', name=_('Dependency')),
    )
    nullable_fields = ('description', 'comments')


class ServiceDependencyFilterForm(NetBoxModelFilterSetForm):
    model = ServiceDependency
    fieldsets = (
        FieldSet('q', 'filter_id', 'tag'),
        FieldSet('service_id', 'depends_on_id', 'relationship_type', 'criticality', name=_('Attributes')),
    )
    service_id = DynamicModelChoiceField(queryset=Service.objects.all(), required=False, label=_('Service'))
    depends_on_id = DynamicModelChoiceField(queryset=Service.objects.all(), required=False, label=_('Depends on'))
    relationship_type = forms.MultipleChoiceField(choices=ServiceDependencyTypeChoices, required=False)
    criticality = forms.MultipleChoiceField(choices=ServiceDependencyCriticalityChoices, required=False)


# ------------------------------------------------------------------------
# ServiceAsset
# ------------------------------------------------------------------------

class ServiceAssetForm(PrimaryModelForm):
    service = DynamicModelChoiceField(queryset=Service.objects.all())
    asset_type = ContentTypeChoiceField(
        queryset=ContentType.objects.filter(ASSET_CONTENT_TYPES),
        label=_('Asset type'),
    )
    comments = CommentField()

    fieldsets = (
        FieldSet('service', 'asset_type', 'asset_id', 'link_type', 'tags', name=_('Asset Link')),
        FieldSet('description', name=_('Additional Details')),
    )

    class Meta:
        model = ServiceAsset
        fields = ('service', 'asset_type', 'asset_id', 'link_type', 'owner', 'description', 'comments', 'tags')


class ServiceAssetImportForm(NetBoxModelImportForm):
    service = CSVModelChoiceField(
        queryset=Service.objects.all(),
        to_field_name='name',
    )
    asset_type = CSVContentTypeField(
        queryset=ContentType.objects.filter(ASSET_CONTENT_TYPES),
        label=_('Asset type'),
    )
    link_type = forms.ChoiceField(choices=ServiceAssetLinkTypeChoices, required=False)

    class Meta:
        model = ServiceAsset
        fields = ('service', 'asset_type', 'asset_id', 'link_type', 'description', 'comments')


class ServiceAssetBulkEditForm(NetBoxModelBulkEditForm):
    link_type = forms.ChoiceField(choices=ServiceAssetLinkTypeChoices, required=False)
    description = forms.CharField(max_length=200, required=False)
    comments = CommentField()

    model = ServiceAsset
    fieldsets = (
        FieldSet('link_type', name=_('Asset Link')),
    )
    nullable_fields = ('description', 'comments')


class ServiceAssetFilterForm(NetBoxModelFilterSetForm):
    model = ServiceAsset
    fieldsets = (
        FieldSet('q', 'filter_id', 'tag'),
        FieldSet('service_id', 'asset_type', 'link_type', name=_('Attributes')),
    )
    service_id = DynamicModelChoiceField(queryset=Service.objects.all(), required=False, label=_('Service'))
    asset_type = ContentTypeChoiceField(
        queryset=ContentType.objects.filter(ASSET_CONTENT_TYPES),
        required=False,
        label=_('Asset type'),
    )
    link_type = forms.MultipleChoiceField(choices=ServiceAssetLinkTypeChoices, required=False)
