from django.contrib import admin

from .models import Service, ServiceAsset, ServiceDependency


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
