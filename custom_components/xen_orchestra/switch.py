"""Switch platform for Xen Orchestra."""
from __future__ import annotations

from typing import Any, TYPE_CHECKING

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, ICON_VM_POWER, ICON_VM_RUNNING, ICON_VM_STOPPED, VM_STATE_RUNNING
from .entity import XenOrchestraBaseEntity

if TYPE_CHECKING:
    from . import XenOrchestraDataUpdateCoordinator


SWITCHES: tuple[SwitchEntityDescription, ...] = (
    SwitchEntityDescription(
        key="power",
        name="Power",
        icon=ICON_VM_POWER,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the switches."""
    coordinator: "XenOrchestraDataUpdateCoordinator" = hass.data[DOMAIN][
        entry.entry_id
    ]["coordinator"]

    entities = []
    if coordinator.data:
        for vm_data in coordinator.data.get("vms", []):
            for description in SWITCHES:
                entities.append(
                    XenOrchestraVMPowerSwitch(coordinator, vm_data, description)
                )

    async_add_entities(entities)


class XenOrchestraVMPowerSwitch(XenOrchestraBaseEntity, SwitchEntity):
    """Defines a Xen Orchestra VM Power Switch."""

    def __init__(
        self,
        coordinator: "XenOrchestraDataUpdateCoordinator",
        vm_data: dict,
        description: SwitchEntityDescription,
    ) -> None:
        """Initialize the switch."""
        self.entity_description = description
        super().__init__(coordinator, vm_data)

    @property
    def is_on(self) -> bool:
        """Return the state of the switch."""
        vm_uuid = self._vm_data["uuid"]
        vm_info = next(
            (
                vm
                for vm in self.coordinator.data.get("vms", [])
                if vm["uuid"] == vm_uuid
            ),
            None,
        )
        return vm_info.get("power_state") == VM_STATE_RUNNING if vm_info else False

    @property
    def icon(self) -> str:
        """Return the icon to use for the switch."""
        if self.is_on:
            return ICON_VM_RUNNING
        else:
            return ICON_VM_STOPPED

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on the switch."""
        api = self.coordinator.api
        await api.startVM(self._vm_data["uuid"])
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off the switch."""
        api = self.coordinator.api
        await api.stopVM(self._vm_data["uuid"])
        await self.coordinator.async_request_refresh()