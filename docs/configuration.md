# Configuration for the Home Assistant Xen Orchestra Plugin

This document explains how to configure the Xen Orchestra plugin for Home Assistant. Follow the steps below to set up the integration properly.

## Required Settings

To configure the Xen Orchestra plugin, you need to provide the following settings:

- **API URL**: The base URL of your Xen Orchestra instance (e.g., `https://your-xen-orchestra-url`).
- **Username**: The username for authenticating with the Xen Orchestra API.
- **Password**: The password for the specified username.

## Configuration Steps

1. **Access Home Assistant**: Open your Home Assistant instance in a web browser.
2. **Navigate to Integrations**: Go to `Configuration` > `Integrations`.
3. **Add Xen Orchestra Integration**: Click on the `+` button to add a new integration and search for "Xen Orchestra".
4. **Enter Configuration Details**: Fill in the required fields:
   - API URL
   - Username
   - Password
5. **Submit Configuration**: Click on the `Submit` button to save your configuration.

## Optional Settings

You can also configure the following optional settings:

- **Polling Interval**: Set the interval (in seconds) for how often the plugin should poll the Xen Orchestra API for updates. The default value is `60` seconds.
- **Enable Debug Logging**: If you want to enable debug logging for troubleshooting, set this option to `true`.

## Example Configuration

Here is an example of how your configuration might look:

```yaml
xen_orchestra:
  api_url: "https://your-xen-orchestra-url"
  username: "your_username"
  password: "your_password"
  polling_interval: 30
  debug_logging: true
```

## Additional Resources

- [Xen Orchestra API Documentation](https://xen-orchestra.com/docs/api.html)
- [Home Assistant Documentation](https://www.home-assistant.io/docs/)

For further assistance, refer to the troubleshooting guide or seek help from the community forums.