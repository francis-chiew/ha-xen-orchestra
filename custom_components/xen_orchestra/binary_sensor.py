"""Binary sensor platform for Xen Orchestra."""
from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, VM_STATE_RUNNING
from .entity import XenOrchestraBaseEntity

if TYPE_CHECKING:
    from . import XenOrchestraDataUpdateCoordinator


BINARY_SENSORS: tuple[BinarySensorEntityDescription, ...] = (
    BinarySensorEntityDescription(
        key="running",
        name="Running",
        device_class=BinarySensorDeviceClass.POWER,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the binary sensors."""
    coordinator: "XenOrchestraDataUpdateCoordinator" = hass.data[DOMAIN][
        entry.entry_id
    ]["coordinator"]

    entities = []
    if coordinator.data:
        for vm_data in coordinator.data.get("vms", []):
            for description in BINARY_SENSORS:
                entities.append(
                    XenOrchestraVMRunningSensor(coordinator, vm_data, description)
                )

    async_add_entities(entities)


class XenOrchestraVMRunningSensor(XenOrchestraBaseEntity, BinarySensorEntity):
    """Defines a Xen Orchestra VM Running Sensor."""

    def __init__(
        self,
        coordinator: "XenOrchestraDataUpdateCoordinator",
        vm_data: dict,
        description: BinarySensorEntityDescription,
    ) -> None:
        """Initialize the binary sensor."""
        self.entity_description = description
        super().__init__(coordinator, vm_data)

    @property
    def is_on(self) -> bool:
        """Return the state of the sensor."""
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