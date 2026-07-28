from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from netbox.models import PrimaryModel

from .choices import (
    ServiceAssetLinkTypeChoices,
    ServiceDependencyCriticalityChoices,
    ServiceDependencyTypeChoices,
    ServiceHealthChoices,
    ServiceStatusChoices,
    ServiceTierChoices,
    ServiceTypeChoices,
)

__all__ = (
    'Service',
    'ServiceAsset',
    'ServiceDependency',
)


class Service(PrimaryModel):
    """
    An IT service (application, platform, or business service) tracked for
    ITSM purposes and optionally mapped to underlying infrastructure.
    """
    name = models.CharField(
        verbose_name=_('name'),
        max_length=100,
        unique=True,
    )
    slug = models.SlugField(
        verbose_name=_('slug'),
        max_length=100,
        unique=True,
    )
    service_type = models.CharField(
        verbose_name=_('service type'),
        max_length=30,
        choices=ServiceTypeChoices,
        default=ServiceTypeChoices.TYPE_APPLICATION,
    )
    status = models.CharField(
        verbose_name=_('status'),
        max_length=30,
        choices=ServiceStatusChoices,
        default=ServiceStatusChoices.STATUS_ACTIVE,
    )
    health_status = models.CharField(
        verbose_name=_('health status'),
        max_length=30,
        choices=ServiceHealthChoices,
        default=ServiceHealthChoices.HEALTH_UNKNOWN,
    )
    tier_level = models.CharField(
        verbose_name=_('tier level'),
        max_length=30,
        choices=ServiceTierChoices,
        default=ServiceTierChoices.TIER_3,
    )
    sla_target = models.CharField(
        verbose_name=_('SLA target'),
        max_length=20,
        blank=True,
        help_text=_('e.g. 99.9%'),
    )
    owner_contact = models.CharField(
        verbose_name=_('owner contact'),
        max_length=200,
        blank=True,
    )
    escalation_contact = models.CharField(
        verbose_name=_('escalation contact'),
        max_length=200,
        blank=True,
    )

    # Override OwnerMixin's `owner` field to avoid a reverse-accessor clash with
    # ipam.Service, which is also named "Service" and also inherits OwnerMixin.
    owner = models.ForeignKey(
        to='users.Owner',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name='itsm_services',
    )

    dependencies = models.ManyToManyField(
        to='self',
        through='ServiceDependency',
        symmetrical=False,
        related_name='+',
        blank=True,
    )

    clone_fields = (
        'service_type', 'status', 'health_status', 'tier_level', 'sla_target', 'description',
    )

    class Meta:
        ordering = ('name',)
        verbose_name = _('service')
        verbose_name_plural = _('services')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('plugins:netbox_itsm:service', args=[self.pk])

    def get_status_color(self):
        return ServiceStatusChoices.colors.get(self.status)

    def get_health_status_color(self):
        return ServiceHealthChoices.colors.get(self.health_status)

    def get_tier_level_color(self):
        return ServiceTierChoices.colors.get(self.tier_level)

    def get_service_type_color(self):
        return ServiceTypeChoices.colors.get(self.service_type)


class ServiceDependency(PrimaryModel):
    """
    A directed dependency relationship between two Services.
    """
    service = models.ForeignKey(
        to=Service,
        on_delete=models.CASCADE,
        related_name='outbound_dependencies',
    )
    depends_on = models.ForeignKey(
        to=Service,
        on_delete=models.CASCADE,
        related_name='dependents',
    )
    relationship_type = models.CharField(
        verbose_name=_('relationship type'),
        max_length=30,
        choices=ServiceDependencyTypeChoices,
        default=ServiceDependencyTypeChoices.TYPE_HARD,
    )
    criticality = models.CharField(
        verbose_name=_('criticality'),
        max_length=30,
        choices=ServiceDependencyCriticalityChoices,
        default=ServiceDependencyCriticalityChoices.CRITICALITY_IMPORTANT,
    )

    clone_fields = ('service', 'relationship_type', 'criticality')

    class Meta:
        ordering = ('service', 'depends_on')
        verbose_name = _('service dependency')
        verbose_name_plural = _('service dependencies')
        constraints = (
            models.UniqueConstraint(
                fields=('service', 'depends_on'),
                name='%(app_label)s_%(class)s_unique_service_depends_on',
            ),
        )

    def __str__(self):
        return f'{self.service} → {self.depends_on}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_itsm:servicedependency', args=[self.pk])

    def clean(self):
        super().clean()
        if self.service_id and self.depends_on_id and self.service_id == self.depends_on_id:
            raise ValidationError({
                'depends_on': _('A service cannot depend on itself.'),
            })

    def get_relationship_type_color(self):
        return ServiceDependencyTypeChoices.colors.get(self.relationship_type)

    def get_criticality_color(self):
        return ServiceDependencyCriticalityChoices.colors.get(self.criticality)


class ServiceAsset(PrimaryModel):
    """
    Links a Service to an underlying NetBox infrastructure object (device,
    virtual machine, interface, circuit, module, etc.) via a generic
    foreign key.
    """
    service = models.ForeignKey(
        to=Service,
        on_delete=models.CASCADE,
        related_name='assets',
    )
    asset_type = models.ForeignKey(
        to='contenttypes.ContentType',
        on_delete=models.PROTECT,
        related_name='+',
        verbose_name=_('asset type'),
    )
    asset_id = models.PositiveBigIntegerField()
    asset = GenericForeignKey(
        ct_field='asset_type',
        fk_field='asset_id',
    )
    link_type = models.CharField(
        verbose_name=_('link type'),
        max_length=30,
        choices=ServiceAssetLinkTypeChoices,
        default=ServiceAssetLinkTypeChoices.LINK_RUNS_ON,
    )

    clone_fields = ('service', 'link_type')

    class Meta:
        ordering = ('service', 'asset_type', 'asset_id')
        verbose_name = _('service asset')
        verbose_name_plural = _('service assets')
        constraints = (
            models.UniqueConstraint(
                fields=('service', 'asset_type', 'asset_id', 'link_type'),
                name='%(app_label)s_%(class)s_unique_service_asset_link',
            ),
        )
        indexes = (
            models.Index(fields=('asset_type', 'asset_id')),
        )

    def __str__(self):
        return f'{self.service} → {self.asset}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_itsm:serviceasset', args=[self.pk])

    def get_link_type_color(self):
        return ServiceAssetLinkTypeChoices.colors.get(self.link_type)
