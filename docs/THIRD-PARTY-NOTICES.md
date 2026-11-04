# Third-party components in local installer packages

The Windows package contains the [Python 3.13.17 embeddable distribution](https://www.python.org/downloads/release/python-31317/) from Python.org. The source ZIP SHA-256 was `9e35319bffedab8b36ad44d8f377cb4f1733bcec257a0b6d04d94f01486ddb38`. Python is governed by the [Python Software Foundation License](https://docs.python.org/3/license.html).

The Windows and Linux packages use Android SDK Platform Tools from [Google's official download page](https://developer.android.com/tools/releases/platform-tools). The original `NOTICE.txt` is included under `tools/`. The downloaded Windows archive SHA-256 was `45f4d63113e895ebde0c90f194099a4676b6ac653bd28d54314a9e022bbc1a99`.

The package also contains four device-specific Android APKs. Their SHA-256 values are in `dist/SHA256SUMS.local`. The current bridge and shortcut APKs were assembled from third-party templates; the virtual-key APK includes modified OEM code. Their public redistribution has not been cleared. The installation archives created from these inputs are local candidates and must not be posted as public GitHub release assets until that issue is resolved.

The README embeds public example images hosted by the [Google Android TV Home listing](https://play.google.com/store/apps/details?id=com.google.android.tvlauncher), the [Projectivy Launcher listing](https://play.google.com/store/apps/details?id=com.spocky.projengmenu), and the [LTvLauncher repository](https://github.com/leanbitlab-org/LtvLauncher). These images remain hosted by their publishers and are not licensed under this project's MIT license.
