# Change the Home screen and remote buttons on SAM TV

[فارسی](README.md) · Version **0.1.6**

One frustration with SAM TVs is how little you can change the Home screen and app ribbon. Even with capable hardware, that makes everyday use more cumbersome.

This project lets you choose your TV's Home screen and add the features you find useful.

<img src="https://play-lh.googleusercontent.com/U1hhfK4bw9Q9C-qbj1AfReA-lpDqrovDLZxfl99V1UdBnCcijmNCXEcj9MFDkC00eTF6mt2-b072VYjbUsGJwA=w1052-h592" width="480" alt="Example of the Projectivy Home screen">

*An example of [Projectivy](https://play.google.com/store/apps/details?id=com.spocky.projengmenu). Your apps and background will look different.*

## Will it work on my TV?

We tested the package on one **SAM R4 running Android 11**. The installer checks the TV's software as well as its model name. Another R4 may still fail the normal installation check.

If you have another model or board, start with **Read-only discovery**. It shows the TV's basic details without installing anything. To check whether this setup works on your TV, choose **Experimental trial**. Failing the normal check does not mean this approach cannot work on your TV.

The experimental trial in **0.1.6** has not been field-tested on another model. It proceeds only on **Android 11** TVs with the required apps and access. The installer saves a backup, then asks you to check several TV functions with the physical remote. Press **`y`** to continue if everything works; **`n`** or Enter starts restore. **Automatic restore requires the TV to boot and ADB to remain available.** The [installation guide](docs/INSTALL.en.md) explains the checks and recovery steps.

You can share the TV model and Android version in [Issues](https://github.com/pouyaSamie/SamTv-Custom-launchers/issues); do not share backups or personal data.

To install, you need the TV and its remote, a **64-bit Windows or Linux PC with an Intel/AMD processor**, and internet access on the computer. Connect both devices to the **same home network** and keep the TV on. The TV also needs internet if you use its browser to get Activity Launcher.

## Install, step by step

1. **Install Activity Launcher on the TV.** Get it from [F-Droid](https://f-droid.org/en/packages/de.szalkowski.activitylauncher/). Skip this step if it is already installed. [The detailed guide](docs/INSTALL.en.md) explains how to use the TV browser or a USB drive.
2. **Turn on two settings.** In Activity Launcher, search for `DevelopmentActivity` and open the result named `system.development.developmentActivity`. Turn on **Developer Mode** and **USB Debugging**. Leave the other developer settings alone.
3. **Write down the TV's IP address.** Find it in the TV's network settings. It may look like `192.168.1.50`; use the address shown on *your* TV.
4. **Download the computer installer.** Choose [Windows](https://github.com/pouyaSamie/SamTv-Custom-launchers/releases/download/v0.1.6/SAM-TV-v0.1.6-windows.zip) or [Linux](https://github.com/pouyaSamie/SamTv-Custom-launchers/releases/download/v0.1.6/SAM-TV-v0.1.6-linux.tar.gz), then extract the downloaded file. Do not run the installer from inside the ZIP or TAR.GZ file.
5. **Run it on the computer.** On Windows, double-click `Install-SAM-TV.cmd` in the extracted folder. On Linux, run `Install-SAM-TV` from that folder. If Linux does not offer a Run option, see [the detailed guide](docs/INSTALL.en.md).
6. **Answer the prompts.** Press **`n`** for English, then **Enter** for normal installation and again to skip the experimental trial. Enter the TV's IP address. If the TV asks for permission, select **Allow** with the remote. After the compatibility check, press **Enter** at each of the four app questions. This installs Choose Home, TV Settings, and Projectivy, and skips LTvLauncher. Read the warning and press **`y`** to start installation. Enter at this question cancels it.
7. **Check the result.** Home should open Projectivy. Then follow the [post-installation checks](docs/INSTALL.en.md).

Keep the extracted installer folder. Its `backups` folder is needed if you want to restore your previous setup. It contains information from your TV, so keep it private. You do not need to download or transfer APK files yourself.

**If you have another model:** Press **Enter** when asked about installation, then **`y`** when asked about an unverified TV. Read the warning and press **`y`** again only if you accept the risk. When the trial is ready, check the functions it asks you to test. If everything works, **`y`** continues installation; **`n`** or Enter starts restore. Read the [trial and recovery guide](docs/INSTALL.en.md) first.

## Change your choices later

Open **Choose Home** from the TV's apps to select another installed Home screen. We recommend **Projectivy**, which the installer selects by default. **Google Android TV Home** was already on the tested TV. You can also choose to install **LTvLauncher** during setup. These three launchers were tested on the TV used for this release. The **Install new launcher** tile in Choose Home opens a Play Store search on the TV.

<img src="https://play-lh.googleusercontent.com/kmvrlAqiL1m2HV91XvR5lP8g7h9AXx1VB2jPIWdpVUIRo2F93o5nSyJ65naRBsXvl-M3z-H5kM6mnh5Dadpx=w1052-h592" width="360" alt="Example of Google Android TV Home"> <img src="https://raw.githubusercontent.com/leanbitlab-org/LtvLauncher/master/docs/images/screenshot_1.png" width="360" alt="Example of LTvLauncher">

*Examples of [Google Android TV Home](https://play.google.com/store/apps/details?id=com.google.android.tvlauncher) and [LTvLauncher](https://github.com/leanbitlab-org/LtvLauncher). The appearance on your TV may differ.*

See the [installation guide](docs/INSTALL.en.md) to change what the remote buttons do and review the recommended settings.

## If something goes wrong

If the installer says the TV is incompatible, it has not installed anything. If normal installation stops after making a backup or a remote button no longer works, reopen the installer from the **same extracted folder**. Press **`n`** for installation, then **`y`** twice for restore. In the experimental trial, rejecting the result starts a restore attempt. See the [recovery steps](docs/INSTALL.en.md#if-something-goes-wrong) for details.

## Downloads and project details

The [v0.1.6 release](https://github.com/pouyaSamie/SamTv-Custom-launchers/releases/tag/v0.1.6) contains the computer installers, four TV app APKs, and a checksum file. The installer gets the TV apps from that release and downloads [Projectivy](https://github.com/spocky/miproja1/releases/tag/4.73) or [LTvLauncher](https://github.com/leanbitlab-org/LtvLauncher/releases/tag/v2026.10.27) from their official releases when selected. You only need the **Windows or Linux installer**; the individual APKs are there for reference.

Individual TV files: [Remote Buttons and Home bridge](https://github.com/pouyaSamie/SamTv-Custom-launchers/releases/download/v0.1.6/TVHomeBridge-v23.apk), [virtual-key update](https://github.com/pouyaSamie/SamTv-Custom-launchers/releases/download/v0.1.6/Tl_VirtualKey-mapped.apk), [Choose Home shortcut](https://github.com/pouyaSamie/SamTv-Custom-launchers/releases/download/v0.1.6/ChooseHomeShortcut.apk), and [TV Settings shortcut](https://github.com/pouyaSamie/SamTv-Custom-launchers/releases/download/v0.1.6/TVSettingsShortcut-v2.apk). The installer handles these automatically.

The original code and documentation in this project use the [MIT License](LICENSE). Other components have their own terms; see [third-party notices](NOTICE.md).
