from django.contrib import admin

from .models import (
    BusinessCapability,
    Service,
    ServiceAsset,
    ServiceDependency,
    ServicePortfolio,
    ServicePortfolioMember,
)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'service_type', 'status', 'health_status', 'tier_level', 'sla_target', 'owner')
    list_filter = ('service_type', 'status', 'health_status', 'tier_level')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(ServiceDependency)
class ServiceDependencyAdmin(admin.ModelAdmin):
    list_display = ('service', 'depends_on', 'relationship_type', 'criticality')
    list_filter = ('relationship_type', 'criticality')
    search_fields = ('service__name', 'depends_on__name')


@admin.register(ServiceAsset)
class ServiceAssetAdmin(admin.ModelAdmin):
    list_display = ('service', 'asset_type', 'asset_id', 'link_type')
    list_filter = ('link_type', 'asset_type')
    search_fields = ('service__name',)


@admin.register(ServicePortfolio)
class ServicePortfolioAdmin(admin.ModelAdmin):
    list_display = ('name', 'business_domain', 'status', 'portfolio_owner_contact')
    list_filter = ('status',)
    search_fields = ('name', 'business_domain', 'description')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(ServicePortfolioMember)
class ServicePortfolioMemberAdmin(admin.ModelAdmin):
    list_display = ('portfolio', 'service', 'role', 'contribution_percentage')
    list_filter = ('role',)
    search_fields = ('portfolio__name', 'service__name')


@admin.register(BusinessCapability)
class BusinessCapabilityAdmin(admin.ModelAdmin):
    list_display = ('name', 'portfolio', 'parent_capability')
    list_filter = ('portfolio',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
