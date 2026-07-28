# netbox-itsm — instructions for Claude Code

A NetBox plugin (Django app) providing ITSM service mapping: a `Service`
catalog, `ServiceDependency` relationships, and `ServiceAsset` links from a
service to any NetBox infrastructure object. See [README.md](README.md) for
user-facing docs and [CONTRIBUTING.md](CONTRIBUTING.md) for the full
commit/versioning/release conventions — this file is the short operational
playbook for working in this repo specifically.

## Environment

- Plugin source lives at `C:\Users\KyleM\Claude_Code\netbox-itsm` on Windows,
  visible from WSL at `/mnt/c/Users/KyleM/Claude_Code/netbox-itsm`.
- The target NetBox install is inside WSL at `/opt/netbox`, owned by `root`.
  Editing files there from the Windows side (`\\wsl.localhost\...`) can hit
  `EPERM` on write — prefer having the user run commands in their WSL
  terminal, or use `wsl.exe -- bash -lc "..."` for read-only inspection.
- The plugin is installed **editable** (`pip install -e`), so source edits
  here take effect immediately — but the running gunicorn workers cache
  imports, so **any Python code change requires `systemctl restart netbox
  netbox-rq`** in WSL before it's visible. Template-only changes do not need
  a restart in dev (`DEBUG`-dependent), but restart if unsure.
- `DEVELOPER = True` is set in the NetBox `configuration.py` to permit
  `makemigrations`. Don't remove it without checking with the user first —
  it's also relied on for any future schema changes.
- `netbox_diode_plugin` is also installed in this NetBox instance. Don't
  remove it from `PLUGINS` or otherwise touch its config when editing
  `configuration.py`.

## Known footguns already hit in this repo (don't reintroduce)

- **`owner` field collision**: NetBox core already has an unrelated
  `ipam.Service` model. Any model here named identically to a core NetBox
  model that also uses `OwnerMixin`/`PrimaryModel` needs an explicit
  `related_name` on the `owner` FK to avoid `fields.E304` reverse-accessor
  clashes. `Service.owner` already overrides this with `related_name=
  'itsm_services'` — keep that pattern if adding more `owner`-bearing models
  that might collide by name.
- **`urls.py` must `from . import views`** at the top (even though nothing
  else in the file references `views` directly). `get_model_urls()` reads a
  runtime registry that's only populated once `views.py`'s
  `@register_model_view` decorators have executed — without the import,
  Django's URL resolver ends up with missing or empty list-view patterns,
  producing 404s that are otherwise very confusing to debug.
- **Menu/template URL names must match `register_model_view` names exactly**:
  a view registered with `@register_model_view(Model, 'bulk_import', ...)`
  produces the URL name `<model>_bulk_import`, not `<model>_import`. Grep for
  `plugins:netbox_itsm:` before changing a view's registered `name=` to catch
  every reference (`navigation.py`, `tables.py`'s `TagColumn(url_name=...)`,
  templates, `models.py`'s `get_absolute_url`).

## When asked to make code changes

Just make them — no special ceremony beyond the repo's normal engineering
practice. Reuse existing patterns (`choices.py` ChoiceSets, `PrimaryModel`
base classes, `register_model_view` + `get_model_urls`) rather than inventing
new ones. If a change adds a model, it needs the full stack: model → admin →
forms → tables → filtersets → views → urls → navigation → API
serializer/view/url → template — check the existing `Service`/
`ServiceDependency`/`ServiceAsset` trio as the reference implementation for
each layer.

## When asked to commit

Follow [CONTRIBUTING.md](CONTRIBUTING.md)'s Conventional Commits format
exactly: `<type>(<scope>): <summary>`. Do not commit unless explicitly asked,
per standard practice — this applies here with no exception. Stage specific
files, never `git add -A`/`.` blindly; review `git status` output before
committing.

## When asked to bump the version

1. Decide MAJOR/MINOR/PATCH using the rules in
   [CONTRIBUTING.md § Versioning](CONTRIBUTING.md#versioning). If it's
   ambiguous whether a change is breaking, ask rather than guess.
2. Update the version string in **both**:
   - `pyproject.toml` → `[project].version`
   - `netbox_itsm/__init__.py` → `NetBoxITSMConfig.version`
   These must always match. If asked to check the current version, read both
   and flag it as a bug if they've drifted.
3. Move `CHANGELOG.md`'s `[Unreleased]` section into a new dated
   `## [X.Y.Z] - YYYY-MM-DD` section (use the current date), and update the
   comparison links at the bottom of the file.
4. Update `COMPATIBILITY.md` only if the supported NetBox version range
   actually changed for this release — don't touch it otherwise.

## When asked to tag or release

Only do this when explicitly asked — never as a side effect of a version
bump or commit request. Follow [CONTRIBUTING.md § Release
process](CONTRIBUTING.md#release-process): annotated tag, `v` prefix
(`vX.Y.Z`), never force-push or move an existing tag. Pushing tags/commits to
a remote requires the same explicit confirmation as any other `git push`.

## Testing changes

There is no CI yet and `netbox_itsm/tests/` is currently just a stub
(`__init__.py`). Until real tests exist, verification means: restart the
NetBox service, and either curl the relevant URL for a status code sanity
check, or have the user check the page in their own browser (the sandboxed
Browser tool here cannot reach the WSL-hosted instance directly — don't
assume it can). A `NoReverseMatch` or `Server Error` page pasted back by the
user is the primary signal something's broken; read the traceback fully
before proposing a fix.
