# Install SAM TV Launcher

[README](../README.en.md) · [راهنمای فارسی](INSTALL.fa.md)

Follow this guide on the TV and a computer. With the recommended choices, **Home** opens Projectivy, **Source/Input** still switches HDMI, and the remote's **four colored dots** open the TV settings menu.

Version **0.1.5** is prepared for the tested **SAM R4 running Android 11** and its matching TV software. The name R4 alone is not enough; the installer checks required software too. On a different model or board, you can run **Read-only discovery** first and then choose **Experimental trial** if you accept the risk. This path has not been field-tested on another model. The [exact conditions](MAINTAINERS.md#compatibility-gate-for-015) are in the technical notes.

## 1. Prepare the TV

Keep the TV on. Connect it and your computer to the **same home network**. The computer needs internet access to download the apps during installation. The TV also needs internet if you use its browser to get Activity Launcher.

### Open the hidden developer settings

On the tested SAM TV, the developer settings are hidden. **Activity Launcher** opens that screen for you.

1. If Activity Launcher is already on the TV, open it and continue to step 4.
2. Otherwise, open [the Activity Launcher page on F-Droid](https://f-droid.org/en/packages/de.szalkowski.activitylauncher/) in the TV's browser. Under **Versions**, choose **Download APK** for the suggested version. Open the downloaded file and select **Install**. If the TV asks for permission to install from the browser, allow it for this download.
3. If the TV has no usable browser but has a file manager, open the same F-Droid page on your computer, download the APK, copy it to a USB drive, and plug the drive into the TV. Open the APK with the TV's file manager and select **Install**. If neither method is available on your TV, stop here rather than guessing through other settings.
4. Open **Activity Launcher** on the TV. Search for `DevelopmentActivity`. Open the result whose full name is `system.development.developmentActivity`.
5. Turn on **Developer Mode** and **USB Debugging**. You do not need to change any other developer settings. USB Debugging is the name of the setting even though the installer will connect over your home network.

If you cannot find `DevelopmentActivity` or USB Debugging, stop. The installer cannot connect until those options are available.

### Write down the TV's address

In the TV's settings, open **Network**, **Wi-Fi**, or **Ethernet**, depending on how it is connected. Find the **IP address** and write it down. For example, it might look like `192.168.1.50`. Enter the address shown on *your* TV, not this example. Keep this screen or the TV nearby: it may ask you to approve the computer's connection.

## 2. Run the installer on your computer

1. Download **one** file for your computer from the [v0.1.5 release](https://github.com/pouyaSamie/SamTv-Custom-launchers/releases/tag/v0.1.5): [Windows ZIP](https://github.com/pouyaSamie/SamTv-Custom-launchers/releases/download/v0.1.5/SAM-TV-v0.1.5-windows.zip) or [Linux TAR.GZ](https://github.com/pouyaSamie/SamTv-Custom-launchers/releases/download/v0.1.5/SAM-TV-v0.1.5-linux.tar.gz). You do not need the individual APK files.
2. **Extract** the downloaded file. Do not run the installer while it is still inside the archive.
3. On **Windows**, open the extracted folder and double-click `Install-SAM-TV.cmd`. On **Linux**, open the extracted folder and run `Install-SAM-TV`. If your Linux file manager does not offer **Run**, open a terminal in that folder and enter `./Install-SAM-TV`.
4. Choose your language. Press **Enter** or type `1` for **Install**. Type `3` for **Read-only discovery**, or `4` for **Experimental trial**. Enter the TV's IP address when asked.
5. Watch the TV. If it asks whether to allow **USB debugging** from this computer, choose **Allow** with the remote. The installer checks the TV's compatibility before it changes anything. If it reports that the model or software is not supported, stop.
6. For the recommended setup, press **Enter** at each of the next four questions. This includes **Choose Home**, **TV Settings**, and **Projectivy**; it skips optional **LTvLauncher**. **Remote Buttons** is installed automatically. Read the warning. If you want to proceed, type `INSTALL` and press Enter.
7. Wait for **“Installation completed”**. The installer downloads and checks the selected apps, saves a copy of the previous setup, and then installs them. If it reports an error, read [If something goes wrong](#if-something-goes-wrong) before trying again.

**Keep the entire extracted folder.** The installer saves the recovery copy in its `backups` folder. You need that same folder if you later restore your previous setup. The backup belongs to your TV, so do not share it.

If you chose `3`, the installer shows the TV information and asks whether to run the **strict normal-install check**. The default answer is **No**. Answering **Yes** still installs nothing; normal installation prompts appear only if the TV matches the tested profile. To try another model, start again and choose `4`.

### Trial on another model

This section applies only to option `4`. The model, board, and original APK hashes may differ from the tested R4, but **Android 11, the required Realtek apps, and ADB root** must be present. Without them, the installer stops before changing the TV.

1. After entering the IP address, read the displayed TV information and warning. Type `EXPERIMENT` only if you want to proceed. Any other answer exits without installing anything.
2. The installer downloads and verifies its files, then saves and checks a **recovery backup before any change**. It activates the core pieces for a trial.
3. At **“Trial is ready,”** use the physical remote to test Home, Source/Input and selecting a connected HDMI input with one OK press, the four-color button, audio, and picture.
4. If **all** work, type `PASS` on the computer. The installer then adds your selected shortcuts. If anything fails or you want to stop, enter anything else. The installer runs restore and checks the previous setup. Restart the TV after restore and test the buttons again.

This trial cannot guarantee recovery under every failure. **If the TV stops booting or ADB is unavailable, automatic restore cannot run.** Firmware partitions are not modified. Keep the installer folder and its `backups` directory.

## 3. Check the result

Use the TV's physical remote:

1. Press **Home**. Projectivy should appear without the Sambazar ribbon if you kept the recommended choices.
2. Press **Source/Input**. Choose an HDMI input and press **OK once**. The TV should switch to that input.
3. Press the **four colored dots**. The TV menu with **Picture**, **Sound**, and other settings should open.
4. Restart the TV and check the three buttons again.

To choose another Home screen later, open **Choose Home** from the TV's apps. To change the four-color button, open **Remote Buttons**. We recommend leaving it set to **TV Settings** so Picture and Sound remain easy to reach.

## If something goes wrong

- **The installer says the TV is incompatible:** It has not installed anything. Do not force the installation on this version of the TV.
- **The computer cannot connect:** Check that the TV is on, both devices use the same home network, the IP address has not changed, and USB Debugging is still on. Accept any connection prompt on the TV, then try again.
- **A download fails:** Check the computer's internet connection and run the installer again. Downloads are checked before the installer changes the TV.
- **Normal installation stopped after a backup, or Home/Source no longer works:** Open the installer from the **same extracted folder**. Choose **Restore previous setup** (`2`), enter the TV's IP address, and type `RESTORE` when asked. The installer checks the backup and restores the previous Home choice, button settings, and app versions. Restart the TV afterward and test the buttons. In experimental mode, the installer attempts restore automatically if the trial fails.

If Restore cannot connect to the TV, it cannot complete. Check the network and USB Debugging first. If the TV remains unreachable, use the recovery instructions for your TV model. This package does not contain a TV firmware image.
