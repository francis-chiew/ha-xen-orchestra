"""API client for Xen Orchestra."""
from __future__ import annotations

import asyncio
import logging
from typing import Any, Dict, List

import aiohttp

_LOGGER = logging.getLogger(__name__)


class XenOrchestraAPI:
    """API client for Xen Orchestra."""

    def __init__(self, api_url: str, api_token: str, ssl_verify: bool = True) -> None:
        """Initialize the API client."""
        self._api_url = api_url.rstrip("/")
        self._api_token = api_token
        self._ssl_verify = ssl_verify
        self._session: aiohttp.ClientSession | None = None

    async def _ensureSession(self) -> aiohttp.ClientSession:
        """Ensure we have an active session with the auth cookie."""
        if self._session is None or self._session.closed:
            connector = aiohttp.TCPConnector(ssl=self._ssl_verify)
            cookies = {"authenticationToken": self._api_token}
            self._session = aiohttp.ClientSession(
                connector=connector, cookies=cookies
            )
        return self._session

    async def testAuthentication(self) -> bool:
        """Test authentication with the Xen Orchestra API."""
        try:
            await self.getVMs()
            return True
        except Exception as e:
            _LOGGER.error(f"Authentication test failed: {e}")
            raise

    async def _makeRequest(
        self, method: str, endpoint: str, data: Dict[str, Any] = None
    ) -> Any:
        """Make an authenticated request to the API."""
        session = await self._ensureSession()
        url = f"{self._api_url}/{endpoint}"

        try:
            # The cookie is now part of the session, no need to pass it here.
            async with session.request(method, url, json=data) as response:
                if str(response.url).endswith("/signin"):
                    raise Exception("Authentication failed, redirected to signin page.")

                if response.status in [200, 202]:  # 202 = Accepted (async operation)
                    if "application/json" in response.headers.get("Content-Type", ""):
                        return await response.json()
                    else:
                        # For 202 responses, the body is often just the task path
                        text = await response.text()
                        if response.status == 202:
                            _LOGGER.debug(f"Async operation started, task: {text}")
                            return {"task_id": text.strip('"/').split('/')[-1] if text else None}
                        else:
                            raise Exception(
                                f"Unexpected content type: {response.headers.get('Content-Type')}. Response: {text}"
                            )
                else:
                    response_text = await response.text()
                    raise Exception(
                        f"API request failed: {response.status} - {response_text}"
                    )
        except aiohttp.ClientError as e:
            _LOGGER.error(f"API request error: {e}")
            raise

    async def _fetch_details(self, paths: List[str]) -> List[Dict[str, Any]]:
        """Fetch full details for a list of API paths concurrently."""
        if not paths:
            _LOGGER.debug("No paths provided to _fetch_details")
            return []

        _LOGGER.debug(f"Fetching details for {len(paths)} paths: {paths[:3]}...")

        async def _get_detail(path: str):
            # The path from the API is already a complete endpoint path like "/rest/v0/vms/uuid"
            # We need to strip the leading slash if present
            endpoint = path.lstrip("/")
            _LOGGER.debug(f"Fetching detail for endpoint: {endpoint}")
            try:
                result = await self._makeRequest("GET", endpoint)
                _LOGGER.debug(f"Successfully fetched detail for {endpoint}")
                return result
            except Exception as e:
                _LOGGER.error(f"Failed to fetch detail for {endpoint}: {e}")
                return None

        tasks = [_get_detail(path) for path in paths]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Filter out any exceptions that may have occurred
        valid_results = [res for res in results if res is not None and not isinstance(res, Exception)]
        _LOGGER.debug(f"_fetch_details returning {len(valid_results)} valid results out of {len(results)} total")
        return valid_results

    async def getVMs(self) -> List[Dict[str, Any]]:
        """Get all virtual machines with their details."""
        _LOGGER.debug("Starting getVMs request")
        vm_paths = await self._makeRequest("GET", "rest/v0/vms")
        _LOGGER.debug(f"getVMs returned {len(vm_paths)} VM paths")
        result = await self._fetch_details(vm_paths)
        _LOGGER.debug(f"getVMs returning {len(result)} VM objects")
        return result

    async def getHosts(self) -> List[Dict[str, Any]]:
        """Get all hosts with their details."""
        _LOGGER.debug("Starting getHosts request")
        host_paths = await self._makeRequest("GET", "rest/v0/hosts")
        _LOGGER.debug(f"getHosts returned {len(host_paths)} host paths")
        result = await self._fetch_details(host_paths)
        _LOGGER.debug(f"getHosts returning {len(result)} host objects")
        return result

    async def getPools(self) -> List[Dict[str, Any]]:
        """Get all pools with their details."""
        _LOGGER.debug("Starting getPools request")
        pool_paths = await self._makeRequest("GET", "rest/v0/pools")
        _LOGGER.debug(f"getPools returned {len(pool_paths)} pool paths")
        result = await self._fetch_details(pool_paths)
        _LOGGER.debug(f"getPools returning {len(result)} pool objects")
        return result

    async def getHostStats(self, host_id: str) -> Dict[str, Any]:
        """Get host statistics."""
        try:
            _LOGGER.debug(f"Getting stats for host {host_id}")
            stats = await self._makeRequest("GET", f"rest/v0/hosts/{host_id}/stats")
            _LOGGER.debug(f"Host stats retrieved for {host_id}")
            return stats
        except Exception as e:
            _LOGGER.error(f"Failed to get host stats for {host_id}: {e}")
            return {}

    async def startVM(self, vm_id: str) -> None:
        """Start a VM."""
        try:
            response = await self._makeRequest("POST", f"rest/v0/vms/{vm_id}/actions/start")
            _LOGGER.debug(f"Started VM {vm_id}")
        except Exception as e:
            _LOGGER.error(f"Failed to start VM {vm_id}: {e}")
            raise

    async def stopVM(self, vm_id: str) -> None:
        """Stop a VM."""
        try:
            response = await self._makeRequest("POST", f"rest/v0/vms/{vm_id}/actions/clean_shutdown")
            _LOGGER.debug(f"Stopped VM {vm_id}")
        except Exception as e:
            _LOGGER.error(f"Failed to stop VM {vm_id}: {e}")
            raise

    async def hardShutdownVM(self, vm_id: str) -> None:
        """Hard shutdown a VM."""
        try:
            response = await self._makeRequest("POST", f"rest/v0/vms/{vm_id}/actions/hard_shutdown")
            _LOGGER.debug(f"Hard shutdown VM {vm_id}")
        except Exception as e:
            _LOGGER.error(f"Failed to hard shutdown VM {vm_id}: {e}")
            raise

    async def restartVM(self, vm_id: str) -> bool:
        """Restart a virtual machine."""
        try:
            await self._makeRequest(
                "POST", f"rest/v0/vms/{vm_id}/actions/clean_reboot", {}
            )
            return True
        except Exception as e:
            _LOGGER.error(f"Failed to restart VM {vm_id}: {e}")
            return False

    async def pauseVM(self, vm_id: str) -> bool:
        """Pause a virtual machine."""
        try:
            await self._makeRequest(
                "POST", f"rest/v0/vms/{vm_id}/actions/pause", {}
            )
            return True
        except Exception as e:
            _LOGGER.error(f"Failed to pause VM {vm_id}: {e}")
            return False

    async def unpauseVM(self, vm_id: str) -> bool:
        """Unpause a virtual machine."""
        try:
            await self._makeRequest(
                "POST", f"rest/v0/vms/{vm_id}/actions/unpause", {}
            )
            return True
        except Exception as e:
            _LOGGER.error(f"Failed to unpause VM {vm_id}: {e}")
            return False

    async def enableHost(self, host_id: str) -> bool:
        """Enable a host."""
        try:
            await self._makeRequest(
                "POST", f"rest/v0/hosts/{host_id}/enable", {}
            )
            return True
        except Exception as e:
            _LOGGER.error(f"Failed to enable host {host_id}: {e}")
            return False

    async def disableHost(self, host_id: str) -> bool:
        """Disable a host."""
        try:
            await self._makeRequest(
                "POST", f"rest/v0/hosts/{host_id}/disable", {}
            )
            return True
        except Exception as e:
            _LOGGER.error(f"Failed to disable host {host_id}: {e}")
            return False

    async def close(self) -> None:
        """Close the API session."""
        if self._session and not self._session.closed:
            await self._session.close()