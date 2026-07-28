# NetBox ITSM Service Mapping

A [NetBox](https://github.com/netbox-community/netbox) plugin that adds an IT
service catalog to NetBox and lets you map each service to the infrastructure
that supports it — turning NetBox into a source of truth for both *what you
run* and *what it runs on*.

## Contents

- [Features](#features)
- [Data model](#data-model)
- [Compatibility](#compatibility)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [REST API](#rest-api)
- [Permissions](#permissions)
- [Roadmap](#roadmap)
- [Development](#development)
- [License](#license)

## Features

- **Service catalog** — track applications, platforms, business services, and
  infrastructure services with a type, lifecycle status, health status, tier
  level, SLA target, and owner/escalation contacts.
- **Service dependencies** — model directed relationships between services
  (hard dependency / soft dependency / recommends), each with a criticality
  rating, so you can see what a service needs to function and who depends on
  it in turn.
- **Service-to-asset links** — link a service to *any* NetBox infrastructure
  object — device, interface, module, virtual machine, or circuit — via a
  generic relationship, with a link type (runs on / depends on / manages /
  monitors).
- **Service portfolios** — group services into business-aligned domains
  (e.g. Finance, Engineering), with a role and contribution-percentage
  weighting per member service, and computed portfolio-level aggregate
  health and SLA-compliance rollups.
- **Business capabilities** — model the business capabilities a portfolio's
  services support, optionally nested under a parent capability.
- Bulk import (CSV), bulk edit, and bulk delete for every model.
- Full REST API.
- Tags, custom fields, comments, ownership, and change logging on every
  model — inherited for free from NetBox's standard plugin model features,
  so services participate in NetBox's existing search, journaling, and (if
  installed) branching workflows like any core object.
- Standard NetBox object-level permissions apply to every model and every API
  endpoint.

## Data model

```
Service
 ├─ outbound_dependencies ──▶ ServiceDependency ──▶ depends_on (Service)
 ├─ dependents          ◀── ServiceDependency ◀── (other Service.service)
 ├─ assets ──▶ ServiceAsset ──▶ asset (any NetBox object, via ContentType)
 └─ portfolio_memberships ──▶ ServicePortfolioMember ──▶ portfolio (ServicePortfolio)

ServicePortfolio
 ├─ portfolio_memberships ──▶ ServicePortfolioMember ──▶ service (Service)
 └─ capabilities ──▶ BusinessCapability ──▶ supported_services (Service, M2M)
                                          └─▶ parent_capability (self, optional)
```

| Model | Purpose | Key fields |
|---|---|---|
| `Service` | An IT service | `name`, `service_type`, `status`, `health_status`, `tier_level`, `sla_target`, `owner_contact`, `escalation_contact` |
| `ServiceDependency` | A directed edge between two services | `service`, `depends_on`, `relationship_type`, `criticality` |
| `ServiceAsset` | A link from a service to an infrastructure object | `service`, `asset_type`, `asset_id` (→ `asset`), `link_type` |
| `ServicePortfolio` | A business-aligned grouping of services | `name`, `business_domain`, `status`, `portfolio_owner_contact` |
| `ServicePortfolioMember` | A service's membership in a portfolio | `portfolio`, `service`, `role`, `contribution_percentage` |
| `BusinessCapability` | A business capability a portfolio's services support | `name`, `portfolio`, `parent_capability`, `supported_services` |

All six inherit from NetBox's `PrimaryModel`, so each also has `description`,
`comments`, `owner`, `tags`, and custom fields.

`ServicePortfolio` exposes two computed rollups, both available on the detail
page and via the API:

- **Aggregate health** — the worst `health_status` among the portfolio's
  member services (a portfolio is only as healthy as its least healthy
  member).
- **SLA compliance summary** — a weighted average of member services'
  numeric `sla_target` values, weighted by each membership's
  `contribution_percentage`.

## Compatibility

See [COMPATIBILITY.md](COMPATIBILITY.md) for the full matrix. Current release:

| NetBox Version | Plugin Version |
|-----------------|----------------|
| 4.6.x            | 0.2.0          |

## Installation

Activate your NetBox virtual environment and install the plugin:

```bash
source /opt/netbox/venv/bin/activate
pip install /path/to/netbox-itsm
```

Or, for development, as an editable install (source edits take effect
immediately, though a running server still needs a restart to pick up
Python changes — see [Development](#development)):

```bash
pip install -e /path/to/netbox-itsm
```

Enable the plugin in `configuration.py` (typically
`/opt/netbox/netbox/netbox/configuration.py`), alongside any other plugins
you already have installed:

```python
PLUGINS = [
    'netbox_itsm',
]
```

If you're installing from source rather than a released package, NetBox
needs `DEVELOPER = True` in `configuration.py` in order to generate the
initial migration:

```bash
cd /opt/netbox/netbox
python manage.py makemigrations netbox_itsm
python manage.py migrate netbox_itsm
python manage.py collectstatic --no-input
sudo systemctl restart netbox netbox-rq
```

If you installed a released package with migrations already included, skip
`makemigrations` and just run `migrate`.

## Configuration

The plugin works out of the box with no required settings — there's nothing
to add to `PLUGINS_CONFIG` for a basic install.

## Usage

Once enabled, an **ITSM** menu appears in the NetBox navigation with:

- **Services** — the service catalog. Use **Add** to create a service, or
  **Import** to bulk-load from CSV.
- **Dependencies** — service-to-service relationships. Create one by picking
  a `Service` and the `Service` it `depends_on`.
- **Asset Links** — service-to-infrastructure mappings. Create one by picking
  a `Service`, an asset type (e.g. `dcim | device`), and the numeric ID of
  the specific object.
- **Portfolios** — business-aligned groupings of services. Create one, then
  add member services via **Portfolio Members** with a role and
  contribution percentage.
- **Portfolio Members** — the service-to-portfolio join, with role and
  SLA-rollup weighting.
- **Business Capabilities** — capabilities a portfolio's services support,
  optionally nested under a parent capability.

From a service's detail page, the **Dependencies** and **Assets** tabs show
everything linked to that service, each with a link back to the full,
filterable list. From a portfolio's detail page, the **Members** and
**Capabilities** tabs do the same, alongside the computed aggregate health
and SLA-compliance rollups.

## REST API

Available at `/api/plugins/itsm/`:

| Endpoint | Description |
|---|---|
| `/api/plugins/itsm/services/` | Service CRUD, with `dependency_count` and `asset_count` annotations |
| `/api/plugins/itsm/service-dependencies/` | Dependency CRUD, with nested `service`/`depends_on` |
| `/api/plugins/itsm/service-assets/` | Asset-link CRUD, with the linked object exposed read-only under `asset` |
| `/api/plugins/itsm/portfolios/` | Portfolio CRUD, with `member_count`, `aggregate_health_status`, and `sla_compliance_summary` |
| `/api/plugins/itsm/portfolio-members/` | Portfolio membership CRUD, with nested `portfolio`/`service` |
| `/api/plugins/itsm/business-capabilities/` | Business capability CRUD, with `supported_service_count` |

Example — create a service:

```bash
curl -s https://netbox.example.com/api/plugins/itsm/services/ \
  -H "Authorization: Token $NETBOX_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
        "name": "checkout-api",
        "service_type": "application",
        "status": "active",
        "tier_level": "tier-1",
        "sla_target": "99.95%"
      }'
```

Example — link that service to a device:

```bash
curl -s https://netbox.example.com/api/plugins/itsm/service-assets/ \
  -H "Authorization: Token $NETBOX_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
        "service": 1,
        "asset_type": "dcim.device",
        "asset_id": 42,
        "link_type": "runs-on"
      }'
```

Filtering, bulk operations, and standard NetBox pagination all work the same
way they do for core NetBox endpoints.

## Permissions

Standard Django/NetBox object permissions apply per model and action:

```
netbox_itsm.view_service      netbox_itsm.add_service      netbox_itsm.change_service      netbox_itsm.delete_service
netbox_itsm.view_servicedependency  ...
netbox_itsm.view_serviceasset       ...
netbox_itsm.view_serviceportfolio       ...
netbox_itsm.view_serviceportfoliomember ...
netbox_itsm.view_businesscapability     ...
```

These are assignable through NetBox's normal Users & Permissions UI, and are
enforced identically across the web UI and the REST API.

## Roadmap

v1 shipped the service catalog, dependency graph, and asset linking needed to
make NetBox useful as an ITSM source of truth. Phase 2 added service
portfolios and business capabilities. Later phases (not yet implemented) are
expected to add, roughly in order:

1. **External ITSM integration** — sync with ServiceNow/Jira, incident
   linking, webhooks.
2. **Health monitoring** — pull real metrics from Prometheus/Datadog and
   infer health from linked infrastructure status.
3. **Change management** — change requests, approval workflows, impact
   analysis, audit trail.
4. **Reporting & analytics** — inventory/health/SLA reports, an interactive
   dependency graph.
5. **Capacity planning** — capacity forecasting and cost projection.
6. **Advanced relationships** — contracts, documentation, team ownership,
   on-call rotation, composite services.

See [CHANGELOG.md](CHANGELOG.md) for what's actually shipped so far.

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for commit message conventions,
versioning policy, and the release process. See
[COMPATIBILITY.md](COMPATIBILITY.md) for the NetBox version support matrix.

## License

Apache 2.0
