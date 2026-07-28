from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from core.models import ObjectType
from netbox.api.fields import ContentTypeField
from netbox.api.gfk_fields import GFKSerializerField
from netbox.api.serializers import PrimaryModelSerializer

from ..models import (
    BusinessCapability,
    Service,
    ServiceAsset,
    ServiceDependency,
    ServicePortfolio,
    ServicePortfolioMember,
)

__all__ = (
    'BusinessCapabilitySerializer',
    'ServiceSerializer',
    'ServiceAssetSerializer',
    'ServiceDependencySerializer',
    'ServicePortfolioSerializer',
    'ServicePortfolioMemberSerializer',
)


class ServiceSerializer(PrimaryModelSerializer):
    dependency_count = serializers.IntegerField(read_only=True, required=False)
    asset_count = serializers.IntegerField(read_only=True, required=False)

    class Meta:
        model = Service
        fields = (
            'id', 'url', 'display', 'name', 'slug', 'service_type', 'status', 'health_status', 'tier_level',
            'sla_target', 'owner_contact', 'escalation_contact', 'owner', 'description', 'comments', 'tags',
            'custom_fields', 'created', 'last_updated', 'dependency_count', 'asset_count',
        )
        brief_fields = ('id', 'url', 'display', 'name', 'service_type', 'status', 'health_status')


class ServiceDependencySerializer(PrimaryModelSerializer):
    service = ServiceSerializer(nested=True)
    depends_on = ServiceSerializer(nested=True)

    class Meta:
        model = ServiceDependency
        fields = (
            'id', 'url', 'display', 'service', 'depends_on', 'relationship_type', 'criticality', 'owner',
            'description', 'comments', 'tags', 'custom_fields', 'created', 'last_updated',
        )
        brief_fields = ('id', 'url', 'display', 'service', 'depends_on', 'relationship_type')


class ServiceAssetSerializer(PrimaryModelSerializer):
    service = ServiceSerializer(nested=True)
    asset_type = ContentTypeField(queryset=ObjectType.objects.all())
    asset = GFKSerializerField(read_only=True)

    class Meta:
        model = ServiceAsset
        fields = (
            'id', 'url', 'display', 'service', 'asset_type', 'asset_id', 'asset', 'link_type', 'owner',
            'description', 'comments', 'tags', 'custom_fields', 'created', 'last_updated',
        )
        brief_fields = ('id', 'url', 'display', 'service', 'asset', 'link_type')

    def validate(self, data):
        if 'asset_type' in data and 'asset_id' in data:
            try:
                data['asset_type'].get_object_for_this_type(id=data['asset_id'])
            except ObjectDoesNotExist:
                raise serializers.ValidationError(
                    f"Invalid asset: {data['asset_type']} ID {data['asset_id']}"
                )
        return super().validate(data)


class ServicePortfolioSerializer(PrimaryModelSerializer):
    member_count = serializers.IntegerField(read_only=True, required=False)
    aggregate_health_status = serializers.SerializerMethodField(read_only=True)
    sla_compliance_summary = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ServicePortfolio
        fields = (
            'id', 'url', 'display', 'name', 'slug', 'business_domain', 'status', 'portfolio_owner_contact',
            'owner', 'description', 'comments', 'tags', 'custom_fields', 'created', 'last_updated',
            'member_count', 'aggregate_health_status', 'sla_compliance_summary',
        )
        brief_fields = ('id', 'url', 'display', 'name', 'business_domain', 'status')

    def get_aggregate_health_status(self, obj):
        return obj.get_aggregate_health_status()

    def get_sla_compliance_summary(self, obj):
        return obj.get_sla_compliance_summary()


class ServicePortfolioMemberSerializer(PrimaryModelSerializer):
    portfolio = ServicePortfolioSerializer(nested=True)
    service = ServiceSerializer(nested=True)

    class Meta:
        model = ServicePortfolioMember
        fields = (
            'id', 'url', 'display', 'portfolio', 'service', 'role', 'contribution_percentage', 'owner',
            'description', 'comments', 'tags', 'custom_fields', 'created', 'last_updated',
        )
        brief_fields = ('id', 'url', 'display', 'portfolio', 'service', 'role')


class BusinessCapabilitySerializer(PrimaryModelSerializer):
    portfolio = ServicePortfolioSerializer(nested=True)
    parent_capability = serializers.PrimaryKeyRelatedField(
        queryset=BusinessCapability.objects.all(), required=False, allow_null=True,
    )
    supported_service_count = serializers.IntegerField(read_only=True, required=False)

    class Meta:
        model = BusinessCapability
        fields = (
            'id', 'url', 'display', 'name', 'slug', 'portfolio', 'parent_capability', 'supported_services',
            'owner', 'description', 'comments', 'tags', 'custom_fields', 'created', 'last_updated',
            'supported_service_count',
        )
        brief_fields = ('id', 'url', 'display', 'name', 'portfolio')
