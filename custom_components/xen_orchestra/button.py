"""Button platform for Xen Orchestra."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from homeassistant.components.button import ButtonEntity, ButtonEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, ICON_VM_HARD_SHUTDOWN
from .entity import XenOrchestraBaseEntity

if TYPE_CHECKING:
    from . import XenOrchestraDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

VM_BUTTONS: tuple[ButtonEntityDescription, ...] = (
    ButtonEntityDescription(
        key="hard_shutdown",
        name="Hard Shutdown",
        icon=ICON_VM_HARD_SHUTDOWN,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the buttons."""
    coordinator: "XenOrchestraDataUpdateCoordinator" = hass.data[DOMAIN][
        entry.entry_id
    ]["coordinator"]

    entities = []
    _LOGGER.debug(f"Button platform setup - Coordinator data: {coordinator.data}")
    
    if coordinator.data:
        vms = coordinator.data.get("vms", [])
        _LOGGER.debug(f"Button platform setup - Found {len(vms)} VMs")
        
        # Create VM action buttons
        for vm_data in vms:
            _LOGGER.debug(f"Creating buttons for VM: {vm_data.get('name_label', 'Unknown')} ({vm_data.get('uuid', 'No UUID')})")
            for description in VM_BUTTONS:
                entities.append(
                    XenOrchestraVMActionButton(coordinator, vm_data, description)
                )
    else:
        _LOGGER.warning("Button platform setup - No coordinator data available")

    # Note: Host power management actions are not available in XOA REST API v0
    _LOGGER.info(f"Adding {len(entities)} VM button entities")
    async_add_entities(entities)


class XenOrchestraVMActionButton(XenOrchestraBaseEntity, ButtonEntity):
    """Defines a Xen Orchestra VM Action Button."""

    def __init__(
        self,
        coordinator: "XenOrchestraDataUpdateCoordinator",
        vm_data: dict,
        description: ButtonEntityDescription,
    ) -> None:
        """Initialize the button."""
        self.entity_description = description
        self._vm_data = vm_data
        super().__init__(coordinator, vm_data)

    async def async_press(self) -> None:
        """Handle the button press."""
        api = self.coordinator.api
        vm_id = self._vm_data["uuid"]
        
        if self.entity_description.key == "hard_shutdown":
            await api.hardShutdownVM(vm_id)
        
        # Request a coordinator refresh to update states
        await self.coordinator.async_request_refresh()