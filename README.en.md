# Change the Home screen and remote buttons on SAM TV

[فارسی](README.md) · Version **0.1.6**

One frustration with SAM TVs is how little you can change the Home screen and app ribbon. Even with capable hardware, that makes everyday use more cumbersome.

This project lets you choose your TV's Home screen and add the features you find useful.

<img src="https://play-lh.googleusercontent.com/U1hhfK4bw9Q9C-qbj1AfReA-lpDqrovDLZxfl99V1UdBnCcijmNCXEcj9MFDkC00eTF6mt2-b072VYjbUsGJwA=w1052-h592" width="480" alt="Example of the Projectivy Home screen">

*An example of [Projectivy](https://play.google.com/store/apps/details?id=com.spocky.projengmenu). Your apps and background will look different.*

## Will it work on my TV?

This version was tested on **one SAM R4 running Android 11**. The installer checks your TV before installation, and it may reject another R4 for the normal setup.

If you have a different model, you can start with **Read-only discovery**, which installs nothing. The installer also offers an **Experimental trial** to try the setup on another model.

This trial has not yet been tested on another model. It proceeds only on **Android 11** TVs with the required software and access. The installer makes a backup before the trial. If you reject the result, it attempts to restore the previous setup. For that to work, the TV must still boot and remain connected to the computer. Read the [trial and recovery guide](docs/INSTALL.en.md) before choosing this option.

To install, you need the TV remote and a **64-bit Windows or Linux computer with an Intel/AMD processor**. The computer needs internet access, and the TV and computer must be on the **same home network**. Keep the TV on until installation finishes.

## Install, step by step

1. **Install Activity Launcher on the TV.** Get it from [F-Droid](https://f-droid.org/en/packages/de.szalkowski.activitylauncher/). Skip this step if it is already installed. [The detailed guide](docs/INSTALL.en.md) explains how to use the TV browser or a USB drive.
2. **Turn on two settings.** In Activity Launcher, search for `DevelopmentActivity` and open the result named `system.development.developmentActivity`. Turn on **Developer Mode** and **USB Debugging**. Leave the other developer settings alone.
3. **Write down the TV's IP address.** Find it in the TV's network settings. It may look like `192.168.1.50`; use the address shown on *your* TV.
4. **Download the computer installer.** Choose [Windows](https://github.com/pouyaSamie/SamTv-Custom-launchers/releases/download/v0.1.6/SAM-TV-v0.1.6-windows.zip) or [Linux](https://github.com/pouyaSamie/SamTv-Custom-launchers/releases/download/v0.1.6/SAM-TV-v0.1.6-linux.tar.gz), then extract the downloaded file. Do not run the installer from inside the ZIP or TAR.GZ file.
5. **Run it on the computer.** On Windows, double-click `Install-SAM-TV.cmd` in the extracted folder. On Linux, run `Install-SAM-TV` from that folder. If Linux does not offer a Run option, see [the detailed guide](docs/INSTALL.en.md).
6. **Answer the prompts.** Press **`n`** for English, then **Enter** for normal installation and again to skip the experimental trial. Enter the TV's IP address. If the TV asks for permission, select **Allow** with the remote.
7. **Choose what to install.** After the TV check, press **Enter** at each of the four questions for the recommended setup. This installs Projectivy, Choose Home, and TV Settings; LTvLauncher is optional.
8. **Start and check the installation.** Read the warning, then press **`y`** to install; Enter cancels. Once you see the success message, Home should open Projectivy. Follow the [post-installation checks](docs/INSTALL.en.md).

Keep the extracted installer folder. It contains a backup of your TV's previous setup, which you need for recovery. Keep this folder private. You do not need to download the TV apps separately.

**If you have another model:** Follow the steps in the [trial and recovery guide](docs/INSTALL.en.md).

## Change your choices later

Open **Choose Home** from the TV's apps to change your Home screen. We recommend **Projectivy**, which the normal setup selects by default. **Android TV Home** and **LTvLauncher** were also tested. Android TV Home appears only if it is already installed on your TV; you can add LTvLauncher during setup. To look for more launchers, select **Install new launcher** in Choose Home to open a Play Store search.

<img src="https://play-lh.googleusercontent.com/kmvrlAqiL1m2HV91XvR5lP8g7h9AXx1VB2jPIWdpVUIRo2F93o5nSyJ65naRBsXvl-M3z-H5kM6mnh5Dadpx=w1052-h592" width="360" alt="Example of Google Android TV Home"> <img src="https://raw.githubusercontent.com/leanbitlab-org/LtvLauncher/master/docs/images/screenshot_1.png" width="360" alt="Example of LTvLauncher">

*Examples of [Google Android TV Home](https://play.google.com/store/apps/details?id=com.google.android.tvlauncher) and [LTvLauncher](https://github.com/leanbitlab-org/LtvLauncher). The appearance on your TV may differ.*

See the [installation guide](docs/INSTALL.en.md) to change what the remote buttons do and review the recommended settings.

## If something goes wrong

If the installer says the TV is incompatible, it has not started installation. If installation stops midway or something does not work afterward, reopen the installer from the **same extracted folder** and choose restore. Follow the [recovery steps](docs/INSTALL.en.md#if-something-goes-wrong).

## Download and project details

From the [v0.1.6 release](https://github.com/pouyaSamie/SamTv-Custom-launchers/releases/tag/v0.1.6), download only the installer for your computer. It downloads the TV files for you.

The original code and documentation in this project use the [MIT License](LICENSE). Other components have their own terms; see [third-party notices](NOTICE.md).
