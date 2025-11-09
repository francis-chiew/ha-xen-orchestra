# Installation Instructions for the Home Assistant Xen Orchestra Plugin

Follow these steps to install the Xen Orchestra plugin in your Home Assistant instance.

## 1. Obtain an API Token

Before you can use the integration, you need to generate an API token in Xen Orchestra.

1.  Log in to your Xen Orchestra web UI.
2.  Navigate to your user profile by clicking your username in the top-left corner.
3.  Select "My account" from the dropdown menu.
4.  In the "API tokens" section, click the "New token" button.
5.  Provide a descriptive name for the token (e.g., "Home Assistant") and click "Create".
6.  **Important:** Copy the generated token immediately. You will not be able to see it again.

## 2. Install the Plugin Files

1.  Connect to the machine running your Home Assistant instance.
2.  Navigate to the `custom_components` directory within your Home Assistant configuration folder. If this directory does not exist, create it.
3.  Copy the entire `xen_orchestra` directory from this project into the `custom_components` directory.

## 3. Restart Home Assistant

After copying the files, restart your Home Assistant instance to load the new integration. You can do this via **Settings > System > Restart**.

## 4. Configure the Integration

1.  Once Home Assistant is back online, navigate to **Settings > Devices & Services**.
2.  Click the **+ ADD INTEGRATION** button in the bottom-right corner.
3.  Search for "Xen Orchestra" and select it.
4.  In the configuration dialog, enter the following:
    *   **API URL**: The full URL to your Xen Orchestra instance (e.g., `http://xoa.your.domain`).
    *   **API Token**: The token you generated in Step 1.
    *   **SSL Verify**: Uncheck this box if your Xen Orchestra instance uses a self-signed SSL certificate.
5.  Click **Submit**.

## Verification

To verify that the plugin is installed correctly, check that new devices and entities for your Xen Orchestra VMs and hosts appear in the integration's device list.