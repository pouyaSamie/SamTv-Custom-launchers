# SAM TV Launcher: Home screen and remote buttons

Version **0.1.4** · [فارسی](README.fa.md)

If the Sambazar ribbon gets in your way, this package lets the **Home** button open a launcher you choose while keeping the TV's HDMI input controls. You can also make the remote's four-color button open TV Settings, an app such as VLC, or the original Sambazar ribbon.

Version 0.1.4 was tested on a **SAM R4 running Android 11**. Other SAM models may work, but they have not been tested. The installer checks the TV before changing anything and stops when it cannot confirm compatibility.

## What's included

- **Remote Buttons** lets you choose what the four-color button does. The package also handles Home and Source/Input.
- **Choose Home** lets you pick the launcher opened by Home. Its shortcut is selected by default during setup, but you can skip it.
- **TV Settings** is a shortcut to the TV's picture, sound, and other settings. It is also selected by default.
- **Projectivy Launcher** is the recommended Home screen and selected by default. **LTvLauncher** is another optional choice. The installer downloads either launcher from its official GitHub release only when you select it and it is not already installed. Google Android TV Home is already on the tested TV.

The remote's colored-dots button (four-color key) opens **TV Settings** by default. We recommend keeping that mapping; you can change it in Remote Buttons.

The original TV app stays in place for HDMI and hardware features. Setup does not erase your apps or personal data.

The four project APKs are [separate release assets](https://github.com/pouyaSamie/SamTv-Custom-launchers/releases/tag/v0.1.4): [Remote Buttons and Home bridge](https://github.com/pouyaSamie/SamTv-Custom-launchers/releases/download/v0.1.4/TVHomeBridge-v23.apk), [virtual-key update](https://github.com/pouyaSamie/SamTv-Custom-launchers/releases/download/v0.1.4/Tl_VirtualKey-mapped.apk), [Choose Home shortcut](https://github.com/pouyaSamie/SamTv-Custom-launchers/releases/download/v0.1.4/ChooseHomeShortcut.apk), and [TV Settings shortcut](https://github.com/pouyaSamie/SamTv-Custom-launchers/releases/download/v0.1.4/TVSettingsShortcut-v2.apk). The installer downloads the selected files automatically; you do not need to open these links yourself.

## Install

There are separate bundles for **64-bit Windows** and **64-bit Linux**. The TV and computer must be on the same home network. Your computer also needs internet access during setup to download the selected APKs. The installer checks each download before changing the TV.
You do not need to run ADB commands or transfer APKs yourself. You do need to open the TV's hidden Developer screen once and enable the two options below.

1. Download [**`SAM-TV-v0.1.4-windows.zip`**](https://github.com/pouyaSamie/SamTv-Custom-launchers/releases/download/v0.1.4/SAM-TV-v0.1.4-windows.zip) or [**`SAM-TV-v0.1.4-linux.tar.gz`**](https://github.com/pouyaSamie/SamTv-Custom-launchers/releases/download/v0.1.4/SAM-TV-v0.1.4-linux.tar.gz) and extract it.
2. Install [**Activity Launcher from F-Droid**](https://f-droid.org/en/packages/de.szalkowski.activitylauncher/) on the TV. Open `DevelopmentActivity` (`system.development.developmentActivity`) and turn on **Developer Mode** and **USB Debugging**. Those are the only two settings needed on the tested TV. Note its IP address in network settings. See the [installation guide](docs/INSTALL.en.md) for more detail.
3. On Windows, double-click **`Install-SAM-TV.cmd`**. On Linux, run **`Install-SAM-TV`**.
4. Choose your language and Install, enter the TV IP, and accept the connection prompt on the TV if one appears. The installer checks compatibility first. Press **Enter** to include Choose Home, TV Settings, and Projectivy. LTvLauncher is optional and off by default. Type `INSTALL` to begin.
5. After setup, test **Home** (Projectivy by default), **Source/Input** and an HDMI selection, and the **colored-dots** button (TV Settings by default). Open **Choose Home** to switch launchers later.

If the compatibility check stops, do not force installation. If a button does not work after setup, follow the [recovery steps](docs/INSTALL.en.md).

## Tested launchers

**[Projectivy Launcher](https://github.com/spocky/miproja1/releases/tag/4.73) — tested and recommended.** If selected during setup, the installer downloads version 4.73 from its [official APK release](https://github.com/spocky/miproja1/releases/download/4.73/ProjectivyLauncher-4.73-c98-xda-release.apk), installs it when needed, and makes it the default Home screen.

<img src="https://play-lh.googleusercontent.com/U1hhfK4bw9Q9C-qbj1AfReA-lpDqrovDLZxfl99V1UdBnCcijmNCXEcj9MFDkC00eTF6mt2-b072VYjbUsGJwA=w1052-h592" width="520" alt="Official Projectivy Launcher preview from Google Play">

*Example image from [Projectivy on Google Play](https://play.google.com/store/apps/details?id=com.spocky.projengmenu); your apps and wallpaper may look different.*

**[Google Android TV Home](https://play.google.com/store/apps/details?id=com.google.android.tvlauncher) — tested.** It was already installed on the test TV.

<img src="https://play-lh.googleusercontent.com/kmvrlAqiL1m2HV91XvR5lP8g7h9AXx1VB2jPIWdpVUIRo2F93o5nSyJ65naRBsXvl-M3z-H5kM6mnh5Dadpx=w1052-h592" width="520" alt="Official Android TV Home preview from Google Play">

*Example image from [Android TV Home on Google Play](https://play.google.com/store/apps/details?id=com.google.android.tvlauncher).*

**[LTvLauncher](https://github.com/leanbitlab-org/LtvLauncher/releases/tag/v2026.10.27) — tested.** Select it during setup if you want the [official ARMv7 APK](https://github.com/leanbitlab-org/LtvLauncher/releases/download/v2026.10.27/LTvLauncher-armeabi-v7a-release.apk) downloaded and installed; it is off by default.

<img src="https://raw.githubusercontent.com/leanbitlab-org/LtvLauncher/master/docs/images/screenshot_1.png" width="520" alt="LTvLauncher preview from its official repository">

*Example image from the [LTvLauncher project](https://github.com/leanbitlab-org/LtvLauncher).*

**Choose Home** lists compatible installed launchers. Its **Install new launcher** tile searches the TV's Play Store.

Read the [full installation and recovery guide](docs/INSTALL.en.md) for details. The [Persian guide](docs/INSTALL.fa.md) is also included.

The project's original code and documentation are available under the [MIT License](LICENSE). Third-party files have separate terms; see the [license scope notice](NOTICE.md).
