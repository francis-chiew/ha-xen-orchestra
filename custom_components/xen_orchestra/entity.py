"""Base entity for the Xen Orchestra integration."""
from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

if TYPE_CHECKING:
    from . import XenOrchestraDataUpdateCoordinator


class XenOrchestraBaseEntity(CoordinatorEntity["XenOrchestraDataUpdateCoordinator"]):
    """Defines a base entity for Xen Orchestra."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: "XenOrchestraDataUpdateCoordinator",
        vm_data: dict,
    ) -> None:
        """Initialize the entity."""
        super().__init__(coordinator)
        self._vm_data = vm_data
        self._attr_unique_id = f"{self._vm_data['uuid']}_{self.entity_description.key}"

        # Link the VM entity to the host device it runs on
        host_id = self._vm_data.get("$container")
        via_device = (DOMAIN, host_id) if host_id else None

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._vm_data["uuid"])},
            name=self._vm_data["name_label"],
            manufacturer="Vates",
            model="Virtual Machine",
            via_device=via_device,
        )

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        if not self.coordinator.last_update_success:
            return False
            
        # Check if the VM still exists in the coordinator data
        vms = self.coordinator.data.get("vms", [])
        vm_uuid = self._vm_data["uuid"]
        
        # Find this VM in the current data
        current_vm = next((vm for vm in vms if vm.get("uuid") == vm_uuid), None)
        
        if not current_vm:
            # VM no longer exists in XOA
            return False
            
        return True

    def _get_current_vm_data(self) -> dict | None:
        """Get current VM data from coordinator."""
        vms = self.coordinator.data.get("vms", [])
        vm_uuid = self._vm_data["uuid"]
        return next((vm for vm in vms if vm.get("uuid") == vm_uuid), None)