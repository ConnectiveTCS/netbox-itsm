# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [0.2.0] - 2026-07-28

### Added

- Phase 2 of the roadmap: service groups and portfolios.
- `ServicePortfolio` model — business-aligned grouping of services with business domain,
  status, and owner contact, plus aggregate health and SLA-compliance rollup calculations.
- `ServicePortfolioMember` model — associates a `Service` with a `ServicePortfolio`, with a
  role and a contribution-percentage weighting used for SLA rollup.
- `BusinessCapability` model — a business capability supported by one or more services,
  optionally nested under a parent capability and scoped to a portfolio.
- Web UI: list, detail, add/edit, delete, and bulk import/edit/delete views for all three
  models, plus Members and Capabilities tabs on the Portfolio detail page.
- REST API endpoints for all three models under `/api/plugins/itsm/`.
- Django admin registration for all three models.
- New "Portfolios & Capabilities" navigation group.

## [0.1.0] - 2026-07-28

### Added

- Initial v1 release: ITSM service catalog.
- `Service` model — name, slug, service type, status, health status, tier level,
  SLA target, owner/escalation contacts.
- `ServiceDependency` model — directed service-to-service dependency relationships
  with relationship type and criticality.
- `ServiceAsset` model — generic link from a `Service` to any NetBox infrastructure
  object (device, interface, module, virtual machine, circuit) via content type.
- Web UI: list, detail, add/edit, delete, and bulk import/edit/delete views for
  all three models, plus dedicated Dependencies/Assets tabs on the Service detail
  page.
- Full REST API at `/api/plugins/itsm/` for all three models.
- Django admin registration for all three models.
- `ITSM` navigation menu with Services, Dependencies, and Asset Links.

[Unreleased]: https://github.com/ConnectiveTCS/netbox-itsm/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/ConnectiveTCS/netbox-itsm/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/ConnectiveTCS/netbox-itsm/releases/tag/v0.1.0
