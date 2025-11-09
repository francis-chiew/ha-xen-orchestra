---
applyTo: "**"
---
# Home Assistant Xen Orchestra Integration - AI Coding Agent Instructions

## Architecture Overview
This is a Home Assistant custom integration for managing Xen Orchestra (XenServer) environments. Key architectural patterns:
- **Cookie-based authentication**: XOA API requires `authenticationToken` cookie, NOT Bearer tokens
- **Two-tier device hierarchy**: Host devices contain VM devices via `via_device` relationships
- **Coordinator pattern**: Single `XenOrchestraDataUpdateCoordinator` in `__init__.py` manages all API data fetching
- **Platform separation**: Entities split across `sensor.py`, `switch.py`, `binary_sensor.py`

## Critical Xen Orchestra API Patterns
- API returns URL paths first (e.g., `/rest/v0/vms/uuid`), then fetch individual objects via `_fetch_details()`
- Session management in `api.py`: Create session with cookie in constructor, reuse for all requests
- Authentication redirects to `/signin` on failure - check `response.url` to detect auth issues
- SSL verification can be disabled via `CONF_SSL_VERIFY` for self-signed certificates

## Home Assistant Integration Patterns
- **Config flow authentication**: Use `api.testAuthentication()` which calls `getVMs()` internally
- **Device creation**: Host devices MUST be created in `__init__.py` before VM entities reference them
- **Circular import avoidance**: Use `TYPE_CHECKING` blocks and string type hints for coordinator references
- **Quick reload support**: `entry.add_update_listener(async_reload_entry)` enables config changes without restart

## Entity Architecture
- **Base entity**: `XenOrchestraBaseEntity` in `entity.py` handles device linking and coordinator setup
- **Unique IDs**: Format as `{vm_uuid}_{entity_description.key}`
- **Device linking**: VMs link to hosts via `via_device=(DOMAIN, host_id)` where `host_id` comes from `vm_data["$container"]`
- **State lookup**: Always fetch fresh data from `coordinator.data` using VM UUID lookup

## Testing & Debugging
- **PowerShell API testing**: Use `test.ps1` with proper cookie setup for manual API verification
- **Verbose logging**: Add `custom_components.xen_orchestra: debug` to HA logger config
- **Common failures**: Authentication (check cookie format), SSL (toggle verify), circular imports (use TYPE_CHECKING)

## Code Conventions
- Use `snake_case` for variables/functions, `PascalCase` for classes
- Prefix private API methods with underscore (e.g., `_makeRequest`)
- Always use f-strings for logging with contextual info
- Constants in `const.py` follow `ACTION_*`, `CONF_*`, `ATTR_*` patterns
- No public code blocks to avoid copyright issues

## File-Specific Patterns
- `api.py`: Session persistence, cookie auth, two-stage data fetching
- `__init__.py`: Host device creation, coordinator setup, reload handling
- `entity.py`: Device hierarchy setup, coordinator typing patterns
- Platform files: Import coordinator via TYPE_CHECKING, create entities from coordinator data

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
