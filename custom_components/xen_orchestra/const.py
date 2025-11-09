"""Constants for the Xen Orchestra integration."""

DOMAIN = "xen_orchestra"

# API endpoints
API_ENDPOINT_VMS = "rest/v0/vms"
API_ENDPOINT_HOSTS = "rest/v0/hosts"
API_ENDPOINT_POOLS = "rest/v0/pools"

# VM States
VM_STATE_RUNNING = "Running"
VM_STATE_HALTED = "Halted"
VM_STATE_PAUSED = "Paused"
VM_STATE_SUSPENDED = "Suspended"

# Host States
HOST_STATE_ENABLED = "Enabled"
HOST_STATE_DISABLED = "Disabled"
HOST_STATE_MAINTENANCE = "Maintenance"

# Actions
ACTION_START_VM = "start"
ACTION_STOP_VM = "stop"
ACTION_RESTART_VM = "restart"
ACTION_PAUSE_VM = "pause"
ACTION_UNPAUSE_VM = "unpause"
ACTION_SUSPEND_VM = "suspend"

ACTION_ENABLE_HOST = "enable"
ACTION_DISABLE_HOST = "disable"

# Icons
ICON_VM_RUNNING = "mdi:server"
ICON_VM_STOPPED = "mdi:server-off"
ICON_VM_PAUSED = "mdi:pause-circle"
ICON_VM_SUSPENDED = "mdi:sleep"
ICON_VM_POWER = "mdi:power"
ICON_VM_HARD_SHUTDOWN = "mdi:power-off"

ICON_HOST = "mdi:server-network"
ICON_HOST_CPU = "mdi:cpu-64-bit"
ICON_HOST_MEMORY = "mdi:memory"
ICON_HOST_ENABLED = "mdi:server-network"
ICON_HOST_DISABLED = "mdi:server-network-off"
ICON_HOST_MAINTENANCE = "mdi:wrench"

ICON_POOL = "mdi:server-network-outline"
ICON_INTEGRATION = "mdi:application-outline"
ACTION_REBOOT_HOST = "reboot"
ACTION_SHUTDOWN_HOST = "shutdown"
ACTION_RESTART_TOOLSTACK = "restart_toolstack"
ACTION_ENTER_MAINTENANCE = "enterMaintenance"
ACTION_EXIT_MAINTENANCE = "exitMaintenance"

# Config Flow
CONF_API_URL = "api_url"
CONF_API_TOKEN = "api_token"
CONF_SSL_VERIFY = "ssl_verify"

# Attributes
ATTR_VM_ID = "vm_id"
ATTR_HOST_ID = "host_id"
ATTR_POOL_ID = "pool_id"
ATTR_MEMORY_USAGE = "memory_usage"
ATTR_CPU_USAGE = "cpu_usage"
ATTR_POWER_STATE = "power_state"
ATTR_TOOLS_VERSION = "tools_version"
ATTR_IP_ADDRESS = "ip_address"
ATTR_UPTIME = "uptime"