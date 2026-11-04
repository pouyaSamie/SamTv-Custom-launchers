# Installation and recovery

[Back to README](../README.md) · [فارسی](INSTALL.fa.md)

This guide is for version **0.1.4**. It was tested on a SAM R4 running Android 11. Setup checks compatibility before changing the TV. If the check fails, it installs nothing.

## 1. Prepare the TV

Connect the TV and computer to the same home network and keep the TV on.

On the SAM TV we tested, Developer options are hidden from the normal Settings menu. To open them:

1. Install and open [**Activity Launcher from F-Droid**](https://f-droid.org/en/packages/de.szalkowski.activitylauncher/) on the TV. Do not confuse it with TV Launcher or similarly named apps.
2. Search for **`DevelopmentActivity`**. Its identifier is **`system.development.developmentActivity`**. Open that entry.
3. Turn on **Developer Mode** and **USB Debugging**. Those were the only two settings needed for the connection on the TV we tested.
4. Find and note the TV's **IP address** in network settings. An example is `192.168.1.50`.

Activity Launcher only opens the hidden settings screen; it does not turn options on for you. If `DevelopmentActivity` or **USB Debugging** is missing, stop and report your TV model instead of trying this installer.

## 2. Install from your computer

Download the package for your computer from **Releases** and unzip it:

- **64-bit Windows:** `SAM-TV-v0.1.4-windows.zip`; double-click **`Install-SAM-TV.cmd`**.
- **64-bit Linux:** `SAM-TV-v0.1.4-linux.tar.gz`; run **`Install-SAM-TV`**. If your file manager asks, choose to run the file.

If double-clicking does not open the Linux installer, open a terminal in the extracted folder and run `./Install-SAM-TV`.

In the installer, select your language and Install. Enter the TV IP address. Accept any connection authorization prompt on the TV. Setup checks compatibility first and does not change the TV during that check.

The **Choose Home** and **TV Settings** shortcuts are selected by default; press Enter to include both. **Remote Buttons** is part of the required package and is always installed. Finally, type `INSTALL` to confirm. Before changing TV settings, setup saves a recovery copy under `backups` in the extracted package. Keep that folder private.

## 3. Check the result

Use the physical TV remote:

1. From an HDMI picture, press **Home**. Android TV Home should open without the Sambazar ribbon.
2. Press **Source/Input**, select an HDMI port, and press **OK once**. The picture from that input should appear.
3. Press the **four-color** button. TV Settings should open. You can later change this button in **Remote Buttons**.

Open **Choose Home** to pick another launcher. We recommend **Projectivy Launcher**; see its [official Google Play page](https://play.google.com/store/apps/details?id=com.spocky.projengmenu) and example image in the [README](../README.md#tested-launchers). Install it separately and then select it in Choose Home. Repeat the three button checks after restarting the TV.

## If setup fails or you want to undo it

If you see “This TV version has not been verified” or “The TV software differs,” nothing was installed. Do not force the installation.

If Home or Source/Input fails after setup, run the same installer again and choose **Restore previous setup**. Enter the TV IP and confirm. Restore does not erase your personal apps or their data. After it reports success, restart the TV and test the buttons.

If restore cannot reach the TV, check the network and ADB setting. If the TV remains unreachable, use the manufacturer's recovery process for your model. This package does not contain a TV firmware image.
