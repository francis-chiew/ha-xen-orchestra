---
applyTo: "**"
---
# Home Assistant Xen Orchestra Integration - AI Coding Agent Instructions

## Architecture Overview
This is a Home Assistant custom integration for managing Xen Orchestra (XenServer/XCP-ng) environments. Key architectural patterns:
- **Cookie-based authentication**: XOA API requires `authenticationToken` cookie, NOT Bearer tokens
- **Two-tier device hierarchy**: Host devices contain VM devices via `via_device` relationships  
- **Coordinator pattern**: Single `XenOrchestraDataUpdateCoordinator` in `__init__.py` manages all API data fetching with 30-second intervals
- **Platform separation**: Entities split across `sensor.py`, `switch.py`, `binary_sensor.py`, `button.py`
- **Availability handling**: Entities become unavailable when hosts/VMs disappear from XOA, auto-recover when they return

## Critical Xen Orchestra API Patterns
- **Two-stage data fetching**: API returns URL paths first (e.g., `/rest/v0/vms/uuid`), then fetch individual objects via `_fetch_details()`
- **Session management**: Create persistent `aiohttp.ClientSession` with cookie in constructor, reuse for all requests
- **Authentication failures**: Redirects to `/signin` on failure - check `response.url` to detect auth issues
- **SSL handling**: Can disable verification via `CONF_SSL_VERIFY` for self-signed certificates
- **VM actions**: Use `rest/v0/vms/{id}/actions/*` endpoints, expect 202 responses for async operations

## Home Assistant Integration Patterns
- **Config flow**: Use `api.testAuthentication()` which calls `getVMs()` internally for validation
- **Device creation order**: Host devices MUST be created in `__init__.py` before VM entities reference them via `via_device`
- **Circular import avoidance**: Use `TYPE_CHECKING` blocks and string type hints for coordinator references
- **Dynamic device updates**: Coordinator calls `_update_host_devices()` on each refresh to sync device registry
- **Entity filtering**: Dashboard uses `device_model: Virtual Machine` to precisely target VM entities

## Entity Architecture & Availability
- **Base entity**: `XenOrchestraBaseEntity` in `entity.py` handles device linking, availability, and coordinator setup
- **Unique IDs**: Format as `{vm_uuid}_{entity_description.key}` (e.g., `a1b2c3d4-e5f6_power`)
- **Device linking**: VMs link to hosts via `via_device=(DOMAIN, host_id)` where `host_id` comes from `vm_data["$container"]`
- **Availability logic**: Entities check if VM/host exists in current `coordinator.data` and mark unavailable if missing
- **State lookup**: Always fetch fresh data from `coordinator.data` using UUID lookup, never cache stale data

## Dashboard Integration Patterns
- **Auto-discovery**: Uses `auto-entities` card with `device_model: Virtual Machine` filter for precise VM targeting
- **Safety exclusions**: Filters out critical VMs (`*xoa*`, `*home*`) from power controls to prevent accidents
- **Dependency requirements**: Dashboards require Mushroom Cards + Auto-entities (documented but not enforced as hard dependencies)
- **Template usage**: Complex Jinja2 templates calculate infrastructure summaries, use device model filtering for accuracy

## Testing & Debugging
- **PowerShell API testing**: Use `test.ps1` with proper cookie setup for manual API verification outside HA
- **Verbose logging**: Add `custom_components.xen_orchestra: debug` to HA logger config for detailed coordinator data
- **Common failures**: Authentication (check cookie format), SSL (toggle verify), entity unavailability (check coordinator data structure)
- **Host restart issues**: Fixed with availability handling - entities show unavailable when host down, auto-recover when back online

## Code Conventions & File Patterns
- **Naming**: `snake_case` for variables/functions, `PascalCase` for classes, constants follow `ACTION_*`, `CONF_*`, `ATTR_*` patterns
- **API methods**: Prefix private methods with underscore (e.g., `_makeRequest`, `_ensureSession`)
- **Logging**: Always use f-strings with contextual info (VM names, UUIDs, operation types)
- **File roles**:
  - `api.py`: Session persistence, cookie auth, endpoint management, error handling
  - `__init__.py`: Host device creation, coordinator setup, dynamic device updates, platform loading
  - `entity.py`: Base availability logic, device hierarchy setup, UUID-based state management
  - Platform files: Import coordinator via TYPE_CHECKING, use device model for filtering, implement availability checks

## Repository Specifics
- **Git repo**: `francis-chiew/ha-xen-orchestra` with HACS support via `hacs.json`
- **Dashboard files**: Pre-built examples in `dashboard-card-*.yaml` with dependency documentation
- **Documentation structure**: `docs/` folder for detailed setup, `DASHBOARD.md` for dashboard-specific guidance
- **Version management**: Follows semantic versioning, currently at 1.0.0 with HA 2023.11.0+ requirement

---
applyTo: "docs/**/*.md"
---
# Project documentation writing guidelines

## General Guidelines
- Write clear and concise documentation
- Use consistent terminology and style
- Include code examples where applicable

## Grammar
* Use present tense verbs (is, open) instead of past tense (was, opened)
* Write factual statements and direct commands. Avoid hypotheticals like "could" or "would"
* Use active voice where the subject performs the action
* Write in second person (you) to speak directly to readers

## Markdown Guidelines
- Use headings to organize content
- Use bullet points for lists
- Include links to related resources
- Use code blocks for code snippets
