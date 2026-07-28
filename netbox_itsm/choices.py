from utilities.choices import ChoiceSet


class ServiceTypeChoices(ChoiceSet):
    key = 'Service.service_type'

    TYPE_APPLICATION = 'application'
    TYPE_PLATFORM = 'platform'
    TYPE_BUSINESS_SERVICE = 'business-service'
    TYPE_INFRASTRUCTURE_SERVICE = 'infrastructure-service'

    CHOICES = [
        (TYPE_APPLICATION, 'Application', 'blue'),
        (TYPE_PLATFORM, 'Platform', 'purple'),
        (TYPE_BUSINESS_SERVICE, 'Business Service', 'cyan'),
        (TYPE_INFRASTRUCTURE_SERVICE, 'Infrastructure Service', 'gray'),
    ]


class ServiceStatusChoices(ChoiceSet):
    key = 'Service.status'

    STATUS_ACTIVE = 'active'
    STATUS_PLANNED = 'planned'
    STATUS_MAINTENANCE = 'maintenance'
    STATUS_DEPRECATED = 'deprecated'

    CHOICES = [
        (STATUS_ACTIVE, 'Active', 'green'),
        (STATUS_PLANNED, 'Planned', 'cyan'),
        (STATUS_MAINTENANCE, 'Maintenance', 'amber'),
        (STATUS_DEPRECATED, 'Deprecated', 'red'),
    ]


class ServiceHealthChoices(ChoiceSet):
    key = 'Service.health_status'

    HEALTH_HEALTHY = 'healthy'
    HEALTH_DEGRADED = 'degraded'
    HEALTH_CRITICAL = 'critical'
    HEALTH_UNKNOWN = 'unknown'

    CHOICES = [
        (HEALTH_HEALTHY, 'Healthy', 'green'),
        (HEALTH_DEGRADED, 'Degraded', 'amber'),
        (HEALTH_CRITICAL, 'Critical', 'red'),
        (HEALTH_UNKNOWN, 'Unknown', 'gray'),
    ]


class ServiceTierChoices(ChoiceSet):
    key = 'Service.tier_level'

    TIER_1 = 'tier-1'
    TIER_2 = 'tier-2'
    TIER_3 = 'tier-3'
    TIER_4 = 'tier-4'

    CHOICES = [
        (TIER_1, 'Tier 1 - Mission Critical', 'red'),
        (TIER_2, 'Tier 2 - Business Critical', 'orange'),
        (TIER_3, 'Tier 3 - Business Operational', 'blue'),
        (TIER_4, 'Tier 4 - Administrative', 'gray'),
    ]


class ServiceDependencyTypeChoices(ChoiceSet):
    key = 'ServiceDependency.relationship_type'

    TYPE_HARD = 'hard-dependency'
    TYPE_SOFT = 'soft-dependency'
    TYPE_RECOMMENDS = 'recommends'

    CHOICES = [
        (TYPE_HARD, 'Hard Dependency', 'red'),
        (TYPE_SOFT, 'Soft Dependency', 'amber'),
        (TYPE_RECOMMENDS, 'Recommends', 'gray'),
    ]


class ServiceDependencyCriticalityChoices(ChoiceSet):
    key = 'ServiceDependency.criticality'

    CRITICALITY_CRITICAL = 'critical'
    CRITICALITY_IMPORTANT = 'important'
    CRITICALITY_OPTIONAL = 'optional'

    CHOICES = [
        (CRITICALITY_CRITICAL, 'Critical', 'red'),
        (CRITICALITY_IMPORTANT, 'Important', 'amber'),
        (CRITICALITY_OPTIONAL, 'Optional', 'gray'),
    ]


class ServiceAssetLinkTypeChoices(ChoiceSet):
    key = 'ServiceAsset.link_type'

    LINK_RUNS_ON = 'runs-on'
    LINK_DEPENDS_ON = 'depends-on'
    LINK_MANAGES = 'manages'
    LINK_MONITORS = 'monitors'

    CHOICES = [
        (LINK_RUNS_ON, 'Runs On', 'blue'),
        (LINK_DEPENDS_ON, 'Depends On', 'amber'),
        (LINK_MANAGES, 'Manages', 'purple'),
        (LINK_MONITORS, 'Monitors', 'cyan'),
    ]
