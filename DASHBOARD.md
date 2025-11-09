# 🎛️ Xen Orchestra Dashboard Cards

This document provides multiple dashboard card options for your Xen Orchestra integration in Home Assistant.

## 📋 Prerequisites

Before setting up the dashboard cards, ensure you have:

1. ✅ Xen Orchestra integration working properly
2. ✅ Host CPU and Memory sensors populated with data  
3. ✅ VM power switches functioning correctly
4. ✅ Hard shutdown buttons available

## 🎨 Dashboard Options

### Option 1: Advanced Dynamic Card (Recommended)

**Requirements**: 
- `mushroom` custom cards
- `auto-entities` custom card

**Features**:
- ✨ Automatic discovery of all hosts and VMs
- 📊 Real-time CPU/Memory usage with color coding
- 🚦 VM status indicators (Green=On, Red=Off)
- 🚨 Emergency hard shutdown with confirmation
- 📈 Summary statistics

**Installation**: Copy `dashboard-card-example.yaml` content into your dashboard

### Option 2: Simple Static Card

**Requirements**: None (uses built-in Home Assistant cards)

**Features**:
- 📊 Host statistics display
- 🔘 VM power controls in grid layout
- 🚨 Emergency controls section
- 📈 Gauge charts for resource monitoring

**Installation**: Copy `dashboard-card-simple.yaml` and manually add your entity IDs

## 🎯 Card Features Explained

### 🖥️ Host Information
- **CPU Usage**: Shows current CPU percentage with color coding:
  - 🟢 Green (0-60%): Normal operation
  - 🟡 Orange (60-80%): High usage warning  
  - 🔴 Red (80%+): Critical usage alert
  
- **Memory Usage**: Shows RAM utilization with similar color coding:
  - 🟢 Green (0-70%): Normal operation
  - 🟡 Orange (70-85%): High usage warning
  - 🔴 Red (85%+): Critical usage alert

### 💻 VM Controls
- **Power Switch**: Toggle VM on/off with visual feedback
  - 🟢 Green Server Icon: VM is running
  - 🔴 Red Server-Off Icon: VM is stopped
  
- **Hard Shutdown Button**: Emergency power-off for unresponsive VMs
  - ⚠️ Requires confirmation to prevent accidental shutdowns
  - 🔴 Red power-off icon for clear identification

### 📊 Statistics Summary
- **Running VMs**: Shows count of active VMs vs total
- **Average CPU**: Aggregated CPU usage across all hosts
- **Average Memory**: Aggregated memory usage across all hosts

## 🛠️ Customization Guide

### Adding Your Entity IDs

For the simple card, replace these placeholders with your actual entity IDs:

```yaml
# Example entity ID format:
sensor.your_host_name_cpu_usage
sensor.your_host_name_memory_usage
switch.your_vm_name_power
button.your_vm_name_hard_shutdown
```

### Color Theme Customization

You can modify the color thresholds in the templates:

```yaml
# CPU Color Thresholds
{% if cpu > 80 %}
  red
{% elif cpu > 60 %}
  orange  
{% else %}
  green
{% endif %}
```

### Icon Customization

Change icons by modifying the icon fields:

```yaml
icon: mdi:server          # Running VM
icon: mdi:server-off      # Stopped VM
icon: mdi:cpu-64-bit      # CPU usage
icon: mdi:memory          # Memory usage
icon: mdi:power-off       # Hard shutdown
```

## 🔧 Troubleshooting

### Cards Not Showing Data
1. Verify integration is working: Check **Developer Tools > States**
2. Confirm entity IDs match your actual entities
3. Check for typos in entity_id references

### Custom Cards Not Loading  
1. Install required custom cards via HACS:
   - `mushroom` 
   - `auto-entities`
2. Clear browser cache after installation
3. Restart Home Assistant frontend

### Statistics Not Calculating
1. Ensure multiple hosts exist for averages
2. Check that sensors have valid numeric states
3. Verify integration attribute matches exactly

## 🎨 Visual Examples

### Host Status Colors:
- 🟢 **Normal**: CPU < 60%, Memory < 70%
- 🟡 **Warning**: CPU 60-80%, Memory 70-85%  
- 🔴 **Critical**: CPU > 80%, Memory > 85%

### VM Status Indicators:
- 🟢 **Running**: Green server icon, toggle switch on
- 🔴 **Stopped**: Red server-off icon, toggle switch off
- 🔴 **Emergency**: Red power-off button for hard shutdown

## 📱 Mobile Optimization

Both card layouts are responsive and work well on mobile devices:
- Grid layouts adapt to screen size
- Touch-friendly button sizes
- Readable text at smaller resolutions
- Swipe-friendly card arrangements

## 🔄 Auto-Refresh

Cards automatically update when:
- VM states change (on/off)
- Host resource usage changes
- New VMs or hosts are added
- Integration data refreshes (every 30 seconds)

---

**Need Help?** Check the integration logs in **Settings > System > Logs** for any issues with entity discovery or data collection.