# A custom Home and remote for SAM TV

Version **0.1.4** · [فارسی](README.fa.md)

If the Sambazar ribbon gets in your way, this package lets the **Home** button open a launcher you choose while keeping the TV's HDMI input controls. You can also make the remote's four-color button open TV Settings, an app such as VLC, or the original Sambazar ribbon.

Version 0.1.4 was tested on a **SAM R4 running Android 11**. Other SAM models may work, but they have not been tested. The installer checks the TV before changing anything and stops when it cannot confirm compatibility.

## What's included

- **Remote Buttons** lets you choose what the four-color button does. The package also handles Home and Source/Input.
- **Choose Home** lets you pick the launcher opened by Home. Its shortcut is selected by default during setup, but you can skip it.
- **TV Settings** is a shortcut to the TV's picture, sound, and other settings. It is also selected by default.

The original TV app stays in place for HDMI and hardware features. Setup does not erase your apps or personal data.

## Install

There are separate bundles for **64-bit Windows** and **64-bit Linux**. The TV and computer must be on the same home network.

1. Download **`SAM-TV-v0.1.4-windows.zip`** or **`SAM-TV-v0.1.4-linux.tar.gz`** from Releases and extract it.
2. Install [**Activity Launcher from F-Droid**](https://f-droid.org/en/packages/de.szalkowski.activitylauncher/) on the TV. Open `DevelopmentActivity` (`system.development.developmentActivity`) and enable network ADB debugging. Note the TV's IP address in network settings. See the [installation guide](docs/INSTALL.en.md) for more detail.
3. On Windows, double-click **`Install-SAM-TV.cmd`**. On Linux, run **`Install-SAM-TV`**.
4. Choose your language and Install, enter the TV IP, and accept the connection prompt on the TV if one appears. The installer checks compatibility first. Press **Enter** to include both optional shortcuts, then type `INSTALL` to begin.
5. After setup, test **Home**, **Source/Input** and an HDMI selection, and the **four-color** button. Open **Choose Home** to pick your launcher.

If the compatibility check stops, do not force installation. If a button does not work after setup, follow the [recovery steps](docs/INSTALL.en.md).

## Choose another launcher

**Choose Home** lists installed launchers. Its **Install new launcher** tile searches the TV's Play Store. Projectivy is not bundled; install it separately through the TV store if you want it, then select it in Choose Home.

Read the [full installation and recovery guide](docs/INSTALL.en.md) for details. The [Persian guide](docs/INSTALL.fa.md) is also included.
