# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

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

[Unreleased]: https://github.com/<org>/netbox-itsm/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/<org>/netbox-itsm/releases/tag/v0.1.0

<!-- Replace <org> above with the actual GitHub/GitLab org or user once a remote exists. -->
