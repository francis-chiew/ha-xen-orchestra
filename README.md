# 🖥️ Home Assistant Xen Orchestra Integration

[![GitHub release](https://img.shields.io/github/release/francis-chiew/ha-xen-orchestra.svg)](https://github.com/francis-chiew/ha-xen-orchestra/releases)
[![License](https://img.shields.io/github/license/francis-chiew/ha-xen-orchestra.svg)](LICENSE)

A comprehensive Home Assistant custom integration for managing Xen Orchestra (XenServer/XCP-ng) environments with beautiful dashboards and complete VM/host control.

## ✨ Features

### 🖥️ **Virtual Machine Management**
- 🔄 **Power Control**: Start/stop VMs with visual feedback
- 🚨 **Emergency Shutdown**: Hard shutdown buttons for unresponsive VMs
- 📊 **Status Monitoring**: Real-time VM state tracking
- 🎨 **Dynamic Icons**: Green/red server icons based on VM state

### 🏢 **Host Infrastructure Monitoring**  
- 💻 **CPU Usage**: Real-time percentage with color-coded alerts
- 🧠 **Memory Usage**: RAM utilization monitoring with thresholds
- 🖥️ **Host Discovery**: Automatic detection of all XenServer hosts
- 📈 **Resource Trending**: Historical data for capacity planning

### 🎛️ **Beautiful Dashboard Cards**
- 🎨 **Dynamic Layouts**: Auto-discovering hosts and VMs
- 🚦 **Color-Coded Status**: Green/orange/red indicators for quick health assessment
- 📱 **Mobile Optimized**: Responsive design for all screen sizes
- ⚡ **Real-Time Updates**: 30-second refresh intervals

### 🔧 **Easy Configuration**
- 🔐 **Token Authentication**: Secure API token-based authentication
- 🔒 **SSL Support**: Works with self-signed certificates
- ⚙️ **Configuration Flow**: GUI-based setup through Home Assistant
- 🔄 **Auto-Discovery**: Finds all VMs and hosts automatically

## 🚀 Quick Start

### Prerequisites
- Home Assistant 2023.1.0 or later
- Xen Orchestra with REST API access
- Valid API token from XOA

### Dashboard Requirements (Optional)
For the included beautiful dashboard cards, install these HACS plugins:
- **[Mushroom Cards](https://github.com/piitaya/lovelace-mushroom)** - Modern dashboard cards
- **[Auto-entities](https://github.com/thomasloven/lovelace-auto-entities)** - Dynamic entity discovery

> ℹ️ **Note**: The integration works perfectly without these plugins. They're only needed for the pre-built dashboard examples.

### Installation

1. **Install Dashboard Dependencies (Optional)**
   ```bash
   # Via HACS:
   # 1. Go to HACS → Frontend
   # 2. Search and install "Mushroom" 
   # 3. Search and install "Auto-entities"
   # 4. Restart Home Assistant
   ```

2. **Download the Integration**
   ```bash
   # Method 1: HACS (Recommended)
   Add this repository to HACS custom repositories
   
   # Method 2: Manual Installation  
   Download and extract to config/custom_components/xen_orchestra/
   ```

3. **Add Integration**
   - Go to **Settings** → **Devices & Services**
   - Click **Add Integration**
   - Search for "**Xen Orchestra**"
   - Follow the configuration flow

4. **Configure Connection**
   - **URL**: Your XOA URL (e.g., `https://xoa.domain.com`)
   - **API Token**: Generate from XOA Settings → API
   - **SSL Verify**: Disable for self-signed certificates

## 📊 Dashboard Setup

### Quick Dashboard (Copy & Paste)

Choose your preferred dashboard style:

#### 🎨 Advanced Dynamic Dashboard
```yaml
# Requires: Mushroom Cards + Auto-entities (install via HACS first!)
# Features: Auto-discovery, color coding, emergency controls  
# Copy content from: dashboard-card-portable.yaml
```

#### 📋 Simple Static Dashboard  
```yaml
# Requires: Built-in HA cards only
# Features: Manual configuration, basic entity lists
# Copy content from: dashboard-card-simple.yaml
```

**📖 Full Setup Guide**: See [DASHBOARD.md](DASHBOARD.md) for detailed instructions

### Dashboard Features

| Feature | Dynamic Card | Simple Card |
|---------|--------------|-------------|
| Auto-discovery | ✅ | ❌ |
| Color coding | ✅ | ✅ |
| Emergency controls | ✅ | ✅ |
| Mobile optimized | ✅ | ✅ |
| Setup complexity | Medium | Easy |

## 🎯 Available Entities

### 💻 **VM Entities** (per Virtual Machine)
| Entity Type | Name | Description |
|-------------|------|-------------|
| `switch` | `{vm_name}_power` | Start/stop VM control |
| `sensor` | `{vm_name}_status` | Current power state |
| `binary_sensor` | `{vm_name}_running` | On/off status indicator |
| `button` | `{vm_name}_hard_shutdown` | Emergency shutdown |

### 🖥️ **Host Entities** (per XenServer Host)
| Entity Type | Name | Description |
|-------------|------|-------------|
| `sensor` | `{host_name}_cpu_usage` | CPU percentage (0-100%) |
| `sensor` | `{host_name}_memory_usage` | Memory percentage (0-100%) |

## 🎨 Visual Indicators

### Status Colors
- 🟢 **Green**: Normal operation (CPU <60%, Memory <70%)
- 🟡 **Orange**: Warning levels (CPU 60-80%, Memory 70-85%) 
- 🔴 **Red**: Critical levels (CPU >80%, Memory >85%)

### VM Icons
- 🟢 **`mdi:server`**: VM is running
- 🔴 **`mdi:server-off`**: VM is stopped
- 🔴 **`mdi:power-off`**: Hard shutdown button

### Host Icons  
- 💻 **`mdi:cpu-64-bit`**: CPU usage sensor
- 🧠 **`mdi:memory`**: Memory usage sensor
- 🖥️ **`mdi:server-network`**: Host device

## 🔧 Configuration Options

### Integration Settings
```yaml
# Basic Configuration
xen_orchestra:
  url: "https://xoa.yourdomain.com"
  api_token: "your_api_token_here"
  ssl_verify: false  # For self-signed certificates
  update_interval: 30  # Seconds (default)
```

### Entity Customization
```yaml
# Customize entity names and icons
customize:
  switch.vm_webserver_power:
    friendly_name: "Web Server"
    icon: mdi:web
  sensor.host1_cpu_usage:
    friendly_name: "Hypervisor CPU"
```

## 🛠️ API Endpoints Used

| Endpoint | Purpose | Method |
|----------|---------|--------|
| `/rest/v0/vms` | List VMs | GET |
| `/rest/v0/hosts` | List hosts | GET |
| `/rest/v0/vms/{id}/actions/start` | Start VM | POST |
| `/rest/v0/vms/{id}/actions/clean_shutdown` | Stop VM | POST |
| `/rest/v0/vms/{id}/actions/hard_shutdown` | Force shutdown | POST |
| `/rest/v0/hosts/{id}/stats` | Host statistics | GET |

## 🔍 Troubleshooting

### Common Issues

#### ❌ **Authentication Failed**
```
Solution: 
1. Verify API token is correct
2. Check XOA URL format (include https://)
3. Ensure token has proper permissions
```

#### ❌ **SSL Certificate Errors**
```
Solution:
1. Set "SSL Verify" to disabled
2. Add certificate to Home Assistant trust store
3. Use HTTP instead of HTTPS (not recommended)
```

#### ❌ **No Entities Created**
```
Solution:
1. Check integration logs in HA
2. Verify XOA API is accessible
3. Ensure VMs/hosts exist in XOA
4. Restart Home Assistant after setup
```

#### ❌ **Host Stats Not Updating**
```
Solution:
1. Verify hosts are powered on
2. Check XOA has statistics enabled
3. Wait for next update cycle (30 seconds)
```

### Debug Logging
```yaml
# Enable debug logging in configuration.yaml
logger:
  default: warning
  logs:
    custom_components.xen_orchestra: debug
```

## 🤝 Contributing

We welcome contributions! Please see our [contributing guidelines](CONTRIBUTING.md) for details.

### Development Setup
```bash
# Clone repository
git clone https://github.com/francis-chiew/ha-xen-orchestra.git

# Install dependencies  
pip install -r requirements.txt

# Run tests
python -m pytest tests/
```

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- 📚 **Documentation**: Check [docs/](docs/) folder
- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/francis-chiew/ha-xen-orchestra/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/francis-chiew/ha-xen-orchestra/discussions)
- 🗨️ **Community**: [Home Assistant Community Forum](https://community.home-assistant.io/)

## 🙏 Acknowledgments

- [Xen Orchestra](https://xen-orchestra.com/) team for the excellent virtualization management platform
- [Home Assistant](https://www.home-assistant.io/) community for the amazing home automation platform
- All contributors who helped improve this integration

---

**⭐ If this integration helps you, please consider starring the repository!**