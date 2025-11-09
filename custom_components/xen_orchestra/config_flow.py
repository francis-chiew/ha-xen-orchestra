"""Config flow for Xen Orchestra."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import XenOrchestraAPI
from .const import CONF_API_TOKEN, CONF_API_URL, CONF_SSL_VERIFY, DOMAIN

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_API_URL): str,
        vol.Required(CONF_API_TOKEN): str,
        vol.Optional(CONF_SSL_VERIFY, default=True): bool,
    }
)

async def validateInput(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect."""
    api = XenOrchestraAPI(
        api_url=data[CONF_API_URL],
        api_token=data[CONF_API_TOKEN],
        ssl_verify=data[CONF_SSL_VERIFY],
    )

    try:
        await api.testAuthentication()
    except Exception as e:
        _LOGGER.error("Error connecting to Xen Orchestra API: %s", e)
        raise CannotConnect from e
    finally:
        await api.close()

    return {"title": "Xen Orchestra"}


class XenOrchestraConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Xen Orchestra."""

    VERSION = 1

    async def async_step_user(
        self, userInput: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        if userInput is not None:
            try:
                info = await validateInput(self.hass, userInput)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(title=info["title"], data=userInput)

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""