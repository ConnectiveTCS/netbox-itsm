# Contributing

## Development setup

```bash
source /opt/netbox/venv/bin/activate
pip install -e /path/to/netbox-itsm
# add 'netbox_itsm' to PLUGINS in configuration.py, set DEVELOPER = True
python manage.py makemigrations netbox_itsm
python manage.py migrate netbox_itsm
```

## Commit messages — Conventional Commits

Every commit subject line follows [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <short summary, imperative mood, no trailing period>

<body — the "why", wrapped at ~72 chars, optional but preferred for anything
non-trivial. Explain the motivation and effect, not a restatement of the diff.>

<footer — optional. BREAKING CHANGE: ..., Fixes #123, Refs #456>
```

**Types:**

| Type       | Use for |
|------------|---------|
| `feat`     | A new model, view, API endpoint, or user-facing capability |
| `fix`      | A bug fix |
| `docs`     | Documentation only (README, CHANGELOG, docstrings) |
| `refactor` | Code change that neither fixes a bug nor adds a feature |
| `test`     | Adding or correcting tests |
| `chore`    | Tooling, dependency bumps, repo maintenance |
| `build`    | Packaging (`pyproject.toml`, migrations scaffolding) |
| `perf`     | Performance improvement |
| `revert`   | Reverts a previous commit |

**Scope** is the affected module/area: `models`, `api`, `views`, `forms`,
`tables`, `filtersets`, `navigation`, `templates`, `migrations`, `docs`,
`release`. Omit it only when a change is truly repo-wide.

**Breaking changes**: add a `BREAKING CHANGE:` footer describing the impact
(e.g. a model field renamed/removed, an API field renamed) and what
downstream users must do. Any commit with a `BREAKING CHANGE:` footer, or a
`!` after the type/scope (`feat(models)!: ...`), forces a MAJOR version bump.

**Examples:**

```
feat(models): add ServicePortfolio and ServicePortfolioMember

Groups services into business-aligned domains and enables SLA rollup
across member services, per Phase 2 of the roadmap.
```

```
fix(navigation): correct bulk-import menu link names

PluginMenuButton links referenced `service_import`, but the view is
registered under the name `bulk_import`, producing `service_bulk_import`.
Fixes NoReverseMatch on the Services list page.
```

```
docs(changelog): record 0.1.0 release
```

## Versioning

This project uses [Semantic Versioning](https://semver.org/) (`MAJOR.MINOR.PATCH`),
independent of NetBox's own version number. Compatibility with NetBox releases
is tracked separately in [COMPATIBILITY.md](COMPATIBILITY.md).

- **MAJOR** — a breaking change: a model field or model is renamed/removed, an
  API field/endpoint changes shape or is removed, a migration requires manual
  data intervention, or the minimum supported NetBox version jumps to a new
  major/minor line in a way that drops support for previously-supported
  versions.
- **MINOR** — backward-compatible additions: a new model, a new field
  (nullable/blank or with a sane default), a new view, a new API endpoint, a
  new roadmap phase feature.
- **PATCH** — backward-compatible bug fixes: template errors, incorrect URL
  names, filter/form bugs, migration fixes that don't change the schema's
  external shape.

While the plugin is pre-1.0 (`0.x.y`), MINOR bumps may still include small
breaking changes per SemVer convention, but this should be avoided where
practical — prefer holding breaking changes for a deliberate `1.0.0` unless
there's a strong reason to break earlier.

### Where the version lives

The version string must be kept in sync in exactly these two places:

1. `pyproject.toml` → `[project].version`
2. `netbox_itsm/__init__.py` → `NetBoxITSMConfig.version`

## Release process

1. Ensure `CHANGELOG.md`'s `[Unreleased]` section accurately reflects every
   user-facing change since the last release.
2. Bump the version in `pyproject.toml` and `netbox_itsm/__init__.py` (see above).
3. Move the `[Unreleased]` entries into a new dated section, e.g. `## [0.2.0] - 2026-08-15`,
   and leave `[Unreleased]` empty above it.
4. Update `COMPATIBILITY.md` if the supported NetBox version range changed for
   this release.
5. Commit: `chore(release): vX.Y.Z` (body: one-line summary of the release theme).
6. Tag: an **annotated** tag named `vX.Y.Z` (the `v` prefix is required —
   GitHub/GitLab release tooling and the compatibility table both assume it).

   ```bash
   git tag -a vX.Y.Z -m "vX.Y.Z"
   git push origin main --tags
   ```

7. Cut a GitHub/GitLab release from the tag, with the release notes being the
   corresponding `CHANGELOG.md` section (copy-paste, don't paraphrase — the
   changelog is the source of truth).

Never move or force-push an existing tag. If a release was cut in error, yank
it (delete the release, leave the tag or mark it deprecated) and cut a new
PATCH release with the fix — don't rewrite history that may already be
referenced by users' lockfiles.
