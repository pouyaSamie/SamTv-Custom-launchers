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
2. Install [**Activity Launcher from F-Droid**](https://f-droid.org/en/packages/de.szalkowski.activitylauncher/) on the TV. Open `DevelopmentActivity` (`system.development.developmentActivity`) and turn on **Developer Mode** and **USB Debugging**. Those are the only two settings needed on the tested TV. Note its IP address in network settings. See the [installation guide](docs/INSTALL.en.md) for more detail.
3. On Windows, double-click **`Install-SAM-TV.cmd`**. On Linux, run **`Install-SAM-TV`**.
4. Choose your language and Install, enter the TV IP, and accept the connection prompt on the TV if one appears. The installer checks compatibility first. Press **Enter** to include both optional shortcuts, then type `INSTALL` to begin.
5. After setup, test **Home**, **Source/Input** and an HDMI selection, and the **four-color** button. Open **Choose Home** to pick your launcher.

If the compatibility check stops, do not force installation. If a button does not work after setup, follow the [recovery steps](docs/INSTALL.en.md).

## Tested launchers

**[Projectivy Launcher](https://play.google.com/store/apps/details?id=com.spocky.projengmenu) — tested and recommended.** It has a tidier home screen. Projectivy is not bundled; install it separately, then select it in **Choose Home**.

<img src="https://play-lh.googleusercontent.com/U1hhfK4bw9Q9C-qbj1AfReA-lpDqrovDLZxfl99V1UdBnCcijmNCXEcj9MFDkC00eTF6mt2-b072VYjbUsGJwA=w1052-h592" width="520" alt="Official Projectivy Launcher preview from Google Play">

*Example image from [Projectivy on Google Play](https://play.google.com/store/apps/details?id=com.spocky.projengmenu); your apps and wallpaper may look different.*

**[Google Android TV Home](https://play.google.com/store/apps/details?id=com.google.android.tvlauncher) — tested.** It was already installed on the test TV.

<img src="https://play-lh.googleusercontent.com/kmvrlAqiL1m2HV91XvR5lP8g7h9AXx1VB2jPIWdpVUIRo2F93o5nSyJ65naRBsXvl-M3z-H5kM6mnh5Dadpx=w1052-h592" width="520" alt="Official Android TV Home preview from Google Play">

*Example image from [Android TV Home on Google Play](https://play.google.com/store/apps/details?id=com.google.android.tvlauncher).*

**[LTvLauncher](https://github.com/leanbitlab-org/LtvLauncher) — tested.** Install it separately if you want to use it.

<img src="https://raw.githubusercontent.com/leanbitlab-org/LtvLauncher/master/docs/images/screenshot_1.png" width="520" alt="LTvLauncher preview from its official repository">

*Example image from the [LTvLauncher project](https://github.com/leanbitlab-org/LtvLauncher).*

**Choose Home** lists compatible installed launchers. Its **Install new launcher** tile searches the TV's Play Store.

Read the [full installation and recovery guide](docs/INSTALL.en.md) for details. The [Persian guide](docs/INSTALL.fa.md) is also included.

The project's original code and documentation are available under the [MIT License](LICENSE). Third-party files have separate terms; see the [license scope notice](NOTICE.md).
