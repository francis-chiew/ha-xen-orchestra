"""Sensor platform for Xen Orchestra."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, ICON_VM_RUNNING, ICON_HOST_CPU, ICON_HOST_MEMORY
from .entity import XenOrchestraBaseEntity

if TYPE_CHECKING:
    from . import XenOrchestraDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


SENSORS: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key="power_state",
        name="Status",
        icon=ICON_VM_RUNNING,
    ),
)

HOST_SENSORS: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key="cpu_usage",
        name="CPU Usage",
        icon=ICON_HOST_CPU,
        native_unit_of_measurement="%",
    ),
    SensorEntityDescription(
        key="memory_usage",
        name="Memory Usage", 
        icon=ICON_HOST_MEMORY,
        native_unit_of_measurement="%",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensors."""
    coordinator: "XenOrchestraDataUpdateCoordinator" = hass.data[DOMAIN][
        entry.entry_id
    ]["coordinator"]

    entities = []
    _LOGGER.debug(f"Sensor platform setup - Coordinator data: {coordinator.data}")
    
    if coordinator.data:
        vms = coordinator.data.get("vms", [])
        hosts = coordinator.data.get("hosts", [])
        _LOGGER.debug(f"Sensor platform setup - Found {len(vms)} VMs and {len(hosts)} hosts")
        
        # Create VM entities
        for vm_data in vms:
            _LOGGER.debug(f"Creating sensor for VM: {vm_data.get('name_label', 'Unknown')} ({vm_data.get('uuid', 'No UUID')})")
            for description in SENSORS:
                entities.append(
                    XenOrchestraVMStatusSensor(coordinator, vm_data, description)
                )
        
        # Create host sensors
        for host_data in hosts:
            _LOGGER.debug(f"Creating sensors for host: {host_data.get('name_label', 'Unknown')} ({host_data.get('uuid', 'No UUID')})")
            for description in HOST_SENSORS:
                entities.append(
                    XenOrchestraHostSensor(coordinator, host_data, description)
                )
    else:
        _LOGGER.warning("Sensor platform setup - No coordinator data available")

    _LOGGER.debug(f"Adding {len(entities)} sensor entities")
    async_add_entities(entities)


class XenOrchestraVMStatusSensor(XenOrchestraBaseEntity, SensorEntity):
    """Defines a Xen Orchestra VM Status Sensor."""

    def __init__(
        self,
        coordinator: "XenOrchestraDataUpdateCoordinator",
        vm_data: dict,
        description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        self.entity_description = description
        super().__init__(coordinator, vm_data)

    @property
    def native_value(self) -> str | None:
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
        return vm_info.get("power_state") if vm_info else None


class XenOrchestraHostSensor(CoordinatorEntity, SensorEntity):
    """Defines a Xen Orchestra Host Sensor."""

    def __init__(
        self,
        coordinator: "XenOrchestraDataUpdateCoordinator",
        host_data: dict,
        description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        self.entity_description = description
        self._host_data = host_data
        super().__init__(coordinator)
        
        # Set device info for host entities
        self._attr_device_info = {
            "identifiers": {(DOMAIN, self._host_data["uuid"])},
            "name": self._host_data.get("name_label", "Unknown Host"),
            "manufacturer": "Vates",
            "model": "XenServer Host",
        }
        
        # Set unique ID for host entities
        self._attr_unique_id = f"{self._host_data['uuid']}_{self.entity_description.key}"
        self._attr_has_entity_name = True

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        if not self.coordinator.last_update_success:
            return False
            
        # Check if the host still exists in the coordinator data
        hosts = self.coordinator.data.get("hosts", [])
        host_uuid = self._host_data["uuid"]
        
        # Find this host in the current data
        current_host = next((host for host in hosts if host.get("uuid") == host_uuid), None)
        
        if not current_host:
            _LOGGER.debug(f"Host {host_uuid} not found in current data - marking unavailable")
            return False
            
        # Check if we can get host stats (indicates host is responding)
        host_stats = self.coordinator.data.get("host_stats", {}).get(host_uuid)
        if not host_stats:
            _LOGGER.debug(f"No stats available for host {host_uuid} - marking unavailable")
            return False
            
        return True

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        host_uuid = self._host_data["uuid"]
        
        # Get host stats from coordinator data
        host_stats = self.coordinator.data.get("host_stats", {}).get(host_uuid)
        
        if not host_stats:
            return None
            
        stats = host_stats.get("stats", {})
        
        if self.entity_description.key == "cpu_usage":
            # Calculate average CPU usage across all cores
            cpus = stats.get("cpus", {})
            if isinstance(cpus, dict):
                total_usage = 0
                core_count = 0
                
                # Iterate through CPU cores (like "0", "1", "2", etc.)
                for core_id, usage_array in cpus.items():
                    if isinstance(usage_array, list) and usage_array:
                        # Use the last (most recent) value from the array
                        total_usage += usage_array[-1]
                        core_count += 1
                
                if core_count > 0:
                    avg_usage = total_usage / core_count
                    return round(avg_usage, 2)
            return None
            
        elif self.entity_description.key == "memory_usage":
            # Calculate memory usage percentage
            memory_array = stats.get("memory", [])
            memory_free_array = stats.get("memoryFree", [])
            
            if (isinstance(memory_array, list) and memory_array and 
                isinstance(memory_free_array, list) and memory_free_array):
                # Use the last (most recent) values from the arrays
                total_memory = memory_array[-1]
                free_memory = memory_free_array[-1]
                
                if total_memory > 0:
                    used_memory = total_memory - free_memory
                    usage_percent = (used_memory / total_memory) * 100
                    return round(usage_percent, 2)
            return None