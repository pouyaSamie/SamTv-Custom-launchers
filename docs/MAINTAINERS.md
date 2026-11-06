# Maintainer notes and release gate (0.1.4)

Back to [English README](../README.en.md).

## Current architecture

The bridge is an Android 11 app using the TV's `rtk-framework` `KeyEventManager` to intercept Home (3), Source (137), and four-color (138). The OEM `com.realtek.tv` remains responsible for HDMI. A data-installed update to `com.example.tl_virtualkey` suppresses the conflicting source/number strip. The `Choose Home` and `TV Settings` APKs are thin shortcut apps; the actual launcher selector and Remote Buttons screen are in `org.pouya.tvhomebridge`.

The `src/smali/` directory contains only the custom bridge and shortcut classes extracted from the working prototype. It cannot produce an APK by itself. The prototype APK and both shortcut APKs were assembled using an existing app template with many unused resources; the virtual-key APK is a modified OEM package. The maintainer has confirmed redistribution approval. Do **not** present these as reproducible open-source builds.

## Exact tested package

The local `dist/` directory contains the four device-specific APKs plus the official Projectivy 4.73 and LTvLauncher v2026.10.27 APKs. It is Git ignored. Their SHA-256 values are in `dist/SHA256SUMS.local`; the owner can verify with `cd dist && sha256sum -c SHA256SUMS.local`. The owner's backups, `.private/signing/`, diagnostic files, APK experiments, and ADB keys stay outside this repository.

The bridge requires `START_ACTIVITIES_FROM_BACKGROUND` and `WRITE_SECURE_SETTINGS` to open its Home target and store launcher mappings on this firmware. It also uses `rtk-framework`, which is not part of the public Android SDK. The current APK was signed using a locally held AOSP platform test key matching this TV. That key must never be committed. A different TV firmware may use a different platform certificate, so an APK that works here may fail to install or to obtain required privileges elsewhere. Do not bypass a signature mismatch by removing the OEM TV app.

## Compatibility gate for 0.1.4

The current installer has no list of retail SAM model names. Its `check_compatibility` function accepts a device only when **all** of these conditions pass:

1. `ro.product.model` is exactly `R4`, `ro.build.version.release` is exactly `11`, and either `ro.hardware` or `ro.product.board` contains `2851` (case insensitive).
2. The installed `com.realtek.tv` APK returned by `pm path` has SHA-256 `6b2939ee1e30f2c13534692022831f843aa4f587eeee6991e5fbcf6340cad652`. The original `/system_ext/app/Tl_VirtualKey/Tl_VirtualKey.apk` has SHA-256 `3fb39f1da8b17967dddedb7c3828178201e1f474fc7ed097fe3da4111b88e73e`.
3. `com.example.tl_virtualkey`, `com.realtek.menu`, and `com.google.android.tvlauncher` exist; `pm list libraries` contains `rtk-framework`; and `su 0 id` reports `uid=0(root)`.

The code does **not** compare `ro.software.version_id` or check the SAM brand name. A successful check only establishes that these preconditions match; it does not prove the remote, HDMI switching, APK signature, or restore behavior on another physical TV. Installation also needs a readable Android ID and a resolvable current Home app so the backup can be tied to that TV. Adding another device requires a separate review of its firmware and a tested recovery path, not simply loosening these predicates.

For a read-only check, prepare ADB on the candidate TV and run `python3 samtv.py check --serial TV_IP:5555` from a source checkout. This reads properties and installed packages and copies the two APKs into a temporary computer directory for hashing; it does not install anything on the TV. The normal setup wizard performs the same compatibility check before its final `INSTALL` prompt. For public issue reports, request the model, Android version, and concise check result, never the APK files or a full trace.

## Trial flow for other models (not implemented in 0.1.4)

An unfamiliar model must be able to reach a **read-only discovery result** without being rejected merely because its model or board name differs. This result is evidence for deciding whether an adapter can be built; it is not a working Home/HDMI test. Do not expose an `ignore compatibility` switch that runs the R4 installation sequence on another board.

A future guided trial needs these separate gates:

1. **Discover:** read Android version, board, active TV and key packages, framework libraries, signatures, Home handlers, and available ADB privileges. Keep the diagnostic report on the user's computer. Redact device identifiers before any issue report.
2. **Prepare recovery:** save the current Home choice, component enabled states, relevant settings, and every APK that a trial may update. Verify backup hashes and that the original Home/Source path can still be invoked. If the proposed adapter needs an unbacked system change, stop here.
3. **Preview:** install only a separately signed user app and launch it without changing default Home or disabling any vendor component. Verify it opens and can be exited. Removing that app is the rollback for this stage. This does **not** validate remote interception or HDMI switching.
4. **Adapter trial:** offer this only for a reviewed firmware profile with a matching signing and recovery strategy. Apply one change at a time. After each step, verify ADB, Home, Source/HDMI, and settings. On a failed check, run the saved rollback and verify the original state before reporting failure. Do not continue to the next step after a failed rollback.
5. **User confirmation:** show the exact observed results and remaining limits. Continue to full installation only after the user confirms that the TV's physical remote and HDMI picture work, including after a reboot.

Automatic rollback is possible only while the TV boots and ADB remains reachable. No installer can promise an unconditional return from a boot failure or loss of ADB. The trial therefore must not write firmware partitions, change verified boot, or remove the TV core. The current `restore` command is user initiated and does not yet implement the automatic rollback in step 4; do not advertise this trial as available in the public 0.1.4 installers.

## Release checklist

1. Keep the project's MIT license and third-party notices accurate. The four device-specific release APKs are currently not reproducible from the tracked source; do not claim otherwise.
2. Keep proprietary framework binaries out of the tracked source tree.
3. Confirm each firmware's signing and compatibility requirements before widening support.
4. Replace the publisher Play Store screenshots embedded in the prototype selector with artwork that can legally be redistributed, or obtain permission. The public repo currently has no copied publisher screenshots.
5. Sign release APKs with a release key appropriate for the target firmware; document certificate fingerprints and the exact firmware compatibility list. Do not publish the local platform signing key.
6. Run `python3 samtv.py check --serial TV_IP:5555` on every candidate firmware before installing. On the exact test TV, validate installation, optional launcher selection, Home from HDMI, Source/one OK, four-color mappings, reboot persistence, and the explicit restore path.
7. Audit `git status --ignored`, `git ls-files`, and the release ZIP before publication for private backups, device addresses, logs, keys, third-party APKs, and accidentally copied OEM code.

## Public issue reports

Ask for the model, Android version, chipset properties, the compatibility check result, and concise reproduction steps. Never request an APK dump or full `logcat` in a public issue. Make it clear that only TVs matching the two verified APK hashes and the other conditions above are eligible for this release.

## Installer and platform bundles

`samtv.py` is the shared installer for Windows and Linux and uses only Python's standard library. The setup wizard handles both installation and user-initiated restore. It checks the model, Android version, chipset string, the active Realtek TV APK hash, the original system VirtualKey APK hash, and required packages before changing TV settings. It saves APK copies, the pre-install active APK versions, and Home/button settings under an ignored `backups/` directory. Restore selects the newest complete backup matching a hash of this TV's Android ID. It never automatically runs restore after a partial installation failure.

The Windows package contains the [official Python 3.13.17 embeddable x64 package](https://www.python.org/downloads/release/python-31317/) and Android SDK Platform Tools for Windows. The Python archive SHA-256 was `9e35319bffedab8b36ad44d8f377cb4f1733bcec257a0b6d04d94f01486ddb38`. The Platform Tools Windows archive SHA-256 downloaded for this build was `45f4d63113e895ebde0c90f194099a4676b6ac653bd28d54314a9e022bbc1a99`. `Install-SAM-TV.cmd` launches the bundled `runtime/python.exe`; `tools/adb.exe` and its DLLs provide ADB. The Linux package contains a PyInstaller 6.22.3 x86-64 executable made from the same `samtv.py`, plus the existing Linux ADB binary. Neither computer archive contains APKs. The four device-specific APKs are uploaded as separate release assets; the installer downloads them from the versioned GitHub release. Selected launchers come directly from their official GitHub releases. All six expected SHA-256 values are pinned in `samtv.py`.

These SDK/Python executables are local build inputs and are not Git tracked. Keep their notices in the platform packages. Linux uses `tar.gz` to retain the installer's executable permission after extraction.
