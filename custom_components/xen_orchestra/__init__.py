# File: /ha-xen-orchestra/ha-xen-orchestra/custom_components/xen_orchestra/__init__.py

"""The Xen Orchestra integration."""
from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import XenOrchestraAPI
from .const import CONF_API_TOKEN, CONF_API_URL, CONF_SSL_VERIFY, DOMAIN

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.SWITCH, Platform.BINARY_SENSOR, Platform.BUTTON]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Xen Orchestra from a config entry."""
    api = XenOrchestraAPI(
        api_url=entry.data[CONF_API_URL],
        api_token=entry.data[CONF_API_TOKEN],
        ssl_verify=entry.data.get(CONF_SSL_VERIFY, True),
    )
    
    coordinator = XenOrchestraDataUpdateCoordinator(hass, api)
    await coordinator.async_config_entry_first_refresh()
    
    # Store the config entry in coordinator for device updates
    coordinator.config_entry = entry

    device_registry = dr.async_get(hass)
    if coordinator.data:
        for host_data in coordinator.data.get("hosts", []):
            # Use 'uuid' for host identifier, which is standard for XOA API
            host_id = host_data.get("uuid", host_data.get("id"))
            if host_id:
                device_registry.async_get_or_create(
                    config_entry_id=entry.entry_id,
                    identifiers={(DOMAIN, host_id)},
                    name=host_data.get("name_label", "Unknown Host"),
                    manufacturer="Vates",
                    model="XenServer Host",
                    entry_type=DeviceEntryType.SERVICE,
                )

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "api": api,
        "coordinator": coordinator,
    }
    
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))
    
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        # Close the API session
        api = hass.data[DOMAIN][entry.entry_id]["api"]
        await api.close()
        
        # Remove the entry data
        hass.data[DOMAIN].pop(entry.entry_id)
    
    return unload_ok

async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle an options update."""
    await hass.config_entries.async_reload(entry.entry_id)


class XenOrchestraDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from Xen Orchestra API."""

    def __init__(self, hass: HomeAssistant, api: XenOrchestraAPI) -> None:
        """Initialize."""
        self.api = api
        self.hass = hass
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=30),
        )

    async def _async_update_data(self) -> dict:
        """Fetch data from API."""
        try:
            vms = await self.api.getVMs()
            hosts = await self.api.getHosts()
            host_stats = {}
            
            # Update host devices in device registry
            await self._update_host_devices(hosts)
            
            # Fetch host stats separately for easier access
            for host in hosts:
                host_id = host.get("uuid")
                if host_id:
                    try:
                        stats = await self.api.getHostStats(host_id)
                        host_stats[host_id] = stats
                        _LOGGER.debug(f"Fetched stats for host {host_id}: {type(stats)}")
                    except Exception as e:
                        _LOGGER.warning(f"Failed to fetch stats for host {host_id}: {e}")
                        host_stats[host_id] = {}
            
            _LOGGER.debug(f"Fetched {len(vms)} VMs and {len(hosts)} hosts")
            return {"vms": vms, "hosts": hosts, "host_stats": host_stats}
        except Exception as err:
            _LOGGER.error(f"Error communicating with API: {err}")
            raise UpdateFailed(f"Error communicating with API: {err}") from err

    async def _update_host_devices(self, hosts: list) -> None:
        """Update host devices in device registry."""
        device_registry = dr.async_get(self.hass)
        
        for host_data in hosts:
            host_id = host_data.get("uuid", host_data.get("id"))
            if host_id:
                # Get or create the device - this will update it if it exists
                device_registry.async_get_or_create(
                    config_entry_id=self.config_entry.entry_id,
                    identifiers={(DOMAIN, host_id)},
                    name=host_data.get("name_label", "Unknown Host"),
                    manufacturer="Vates",
                    model="XenServer Host",
                    entry_type=DeviceEntryType.SERVICE,
                )