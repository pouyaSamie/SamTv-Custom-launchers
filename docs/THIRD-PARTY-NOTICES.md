# Third-party components in local installer packages

The Windows package contains the [Python 3.13.17 embeddable distribution](https://www.python.org/downloads/release/python-31317/) from Python.org. The source ZIP SHA-256 was `9e35319bffedab8b36ad44d8f377cb4f1733bcec257a0b6d04d94f01486ddb38`. Python is governed by the [Python Software Foundation License](https://docs.python.org/3/license.html).

The Windows and Linux packages use Android SDK Platform Tools from [Google's official download page](https://developer.android.com/tools/releases/platform-tools). The original `NOTICE.txt` is included under `tools/`. The downloaded Windows archive SHA-256 was `45f4d63113e895ebde0c90f194099a4676b6ac653bd28d54314a9e022bbc1a99`.

The four device-specific Android APKs are separate GitHub release assets, not Git-tracked source files. The current bridge and shortcut APKs were assembled from third-party templates; the virtual-key APK includes modified OEM code. The maintainer has confirmed that redistribution approval was obtained.

The installer downloads [Projectivy Launcher 4.73](https://github.com/spocky/miproja1/releases/tag/4.73) from Spocky's official release and [LTvLauncher v2026.10.27](https://github.com/leanbitlab-org/LtvLauncher/releases/tag/v2026.10.27) from LeanBitLab's official release when selected. LTvLauncher is licensed under [GPL-3.0](https://github.com/leanbitlab-org/LtvLauncher/blob/master/LICENSE); its corresponding source is available at that exact release tag. The APK SHA-256 values are pinned in `samtv.py` and listed in the release checksum manifest. These third-party components remain outside the scope of this project's MIT license.

The README embeds public example images hosted by the [Google Android TV Home listing](https://play.google.com/store/apps/details?id=com.google.android.tvlauncher), the [Projectivy Launcher listing](https://play.google.com/store/apps/details?id=com.spocky.projengmenu), and the [LTvLauncher repository](https://github.com/leanbitlab-org/LtvLauncher). These images remain hosted by their publishers and are not licensed under this project's MIT license.
