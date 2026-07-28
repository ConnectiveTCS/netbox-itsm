from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from netbox.models import PrimaryModel

from django.core.validators import MaxValueValidator, MinValueValidator

from .choices import (
    ServiceAssetLinkTypeChoices,
    ServiceDependencyCriticalityChoices,
    ServiceDependencyTypeChoices,
    ServiceHealthChoices,
    ServicePortfolioMemberRoleChoices,
    ServicePortfolioStatusChoices,
    ServiceStatusChoices,
    ServiceTierChoices,
    ServiceTypeChoices,
)

__all__ = (
    'BusinessCapability',
    'Service',
    'ServiceAsset',
    'ServiceDependency',
    'ServicePortfolio',
    'ServicePortfolioMember',
)

#: Worst-to-best ordering used to derive a portfolio's aggregate health from
#: its member services (a portfolio is only as healthy as its worst member).
HEALTH_STATUS_SEVERITY = {
    ServiceHealthChoices.HEALTH_CRITICAL: 0,
    ServiceHealthChoices.HEALTH_DEGRADED: 1,
    ServiceHealthChoices.HEALTH_UNKNOWN: 2,
    ServiceHealthChoices.HEALTH_HEALTHY: 3,
}


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


class ServicePortfolio(PrimaryModel):
    """
    A business-aligned grouping of Services (e.g. by business domain), used
    to roll up SLA and health metrics across a set of related services.
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
    business_domain = models.CharField(
        verbose_name=_('business domain'),
        max_length=100,
        blank=True,
        help_text=_('e.g. Finance, HR, Engineering'),
    )
    status = models.CharField(
        verbose_name=_('status'),
        max_length=30,
        choices=ServicePortfolioStatusChoices,
        default=ServicePortfolioStatusChoices.STATUS_ACTIVE,
    )
    portfolio_owner_contact = models.CharField(
        verbose_name=_('portfolio owner contact'),
        max_length=200,
        blank=True,
    )

    services = models.ManyToManyField(
        to=Service,
        through='ServicePortfolioMember',
        related_name='portfolios',
        blank=True,
    )

    clone_fields = ('business_domain', 'status', 'description')

    class Meta:
        ordering = ('name',)
        verbose_name = _('service portfolio')
        verbose_name_plural = _('service portfolios')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('plugins:netbox_itsm:serviceportfolio', args=[self.pk])

    def get_status_color(self):
        return ServicePortfolioStatusChoices.colors.get(self.status)

    def get_aggregate_health_status(self):
        """
        The portfolio's health is the worst health status among its member
        services (an "AND" aggregation): a portfolio is only as healthy as
        its least healthy member.
        """
        statuses = self.services.values_list('health_status', flat=True)
        if not statuses:
            return None
        return min(statuses, key=lambda status: HEALTH_STATUS_SEVERITY.get(status, 2))

    def get_aggregate_health_status_color(self):
        return ServiceHealthChoices.colors.get(self.get_aggregate_health_status())

    def get_aggregate_health_status_display(self):
        value = self.get_aggregate_health_status()
        if value is None:
            return None
        return dict((choice[0], choice[1]) for choice in ServiceHealthChoices.CHOICES).get(value, value)

    def get_sla_compliance_summary(self):
        """
        A weighted average of member services' numeric SLA targets (e.g.
        "99.9%"), weighted by each membership's contribution_percentage.
        Non-numeric or missing SLA targets are excluded. Returns None if no
        member has a parseable SLA target.
        """
        total_weight = 0
        weighted_sum = 0.0
        for member in self.portfolio_memberships.select_related('service'):
            sla_target = member.service.sla_target
            if not sla_target:
                continue
            try:
                sla_value = float(sla_target.rstrip('%'))
            except ValueError:
                continue
            weight = member.contribution_percentage or 0
            weighted_sum += sla_value * weight
            total_weight += weight
        if not total_weight:
            return None
        return round(weighted_sum / total_weight, 3)


class ServicePortfolioMember(PrimaryModel):
    """
    Associates a Service with a ServicePortfolio, with a role and a
    contribution weighting used for SLA rollup calculations.
    """
    portfolio = models.ForeignKey(
        to=ServicePortfolio,
        on_delete=models.CASCADE,
        related_name='portfolio_memberships',
    )
    service = models.ForeignKey(
        to=Service,
        on_delete=models.CASCADE,
        related_name='portfolio_memberships',
    )
    role = models.CharField(
        verbose_name=_('role'),
        max_length=30,
        choices=ServicePortfolioMemberRoleChoices,
        default=ServicePortfolioMemberRoleChoices.ROLE_PRIMARY,
    )
    contribution_percentage = models.PositiveSmallIntegerField(
        verbose_name=_('contribution percentage'),
        default=100,
        validators=(MinValueValidator(0), MaxValueValidator(100)),
        help_text=_('Weighting used for portfolio-level SLA rollup (0-100).'),
    )

    clone_fields = ('portfolio', 'role', 'contribution_percentage')

    class Meta:
        ordering = ('portfolio', 'service')
        verbose_name = _('portfolio member')
        verbose_name_plural = _('portfolio members')
        constraints = (
            models.UniqueConstraint(
                fields=('portfolio', 'service'),
                name='%(app_label)s_%(class)s_unique_portfolio_service',
            ),
        )

    def __str__(self):
        return f'{self.portfolio} → {self.service}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_itsm:serviceportfoliomember', args=[self.pk])

    def get_role_color(self):
        return ServicePortfolioMemberRoleChoices.colors.get(self.role)


class BusinessCapability(PrimaryModel):
    """
    A business capability supported by one or more Services, optionally
    nested under a parent capability and scoped to a ServicePortfolio.
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
    portfolio = models.ForeignKey(
        to=ServicePortfolio,
        on_delete=models.CASCADE,
        related_name='capabilities',
    )
    parent_capability = models.ForeignKey(
        to='self',
        on_delete=models.SET_NULL,
        related_name='child_capabilities',
        blank=True,
        null=True,
    )
    supported_services = models.ManyToManyField(
        to=Service,
        related_name='business_capabilities',
        blank=True,
    )

    clone_fields = ('portfolio', 'parent_capability', 'description')

    class Meta:
        ordering = ('portfolio', 'name')
        verbose_name = _('business capability')
        verbose_name_plural = _('business capabilities')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('plugins:netbox_itsm:businesscapability', args=[self.pk])

    def clean(self):
        super().clean()
        if self.parent_capability_id and self.pk and self.parent_capability_id == self.pk:
            raise ValidationError({
                'parent_capability': _('A capability cannot be its own parent.'),
            })
