#!/usr/bin/env python3
"""SAM TV Launcher 0.1.8 setup and recovery. Standard library only."""

from __future__ import annotations

import argparse
import hashlib
import ipaddress
import json
import os
from pathlib import Path
import select
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

VERSION = "0.1.8"
ROOT = Path(sys.executable).resolve().parent if getattr(sys, "frozen", False) else Path(__file__).resolve().parent
TESTED_REALTEK = "6b2939ee1e30f2c13534692022831f843aa4f587eeee6991e5fbcf6340cad652"
TESTED_VIRTUALKEY = "3fb39f1da8b17967dddedb7c3828178201e1f474fc7ed097fe3da4111b88e73e"
ORIGINAL_VIRTUALKEY_PATH = "/system_ext/app/Tl_VirtualKey/Tl_VirtualKey.apk"
APKS = {
    "bridge": "TVHomeBridge-v23.apk",
    "virtualkey": "Tl_VirtualKey-mapped.apk",
    "choose": "ChooseHomeShortcut.apk",
    "settings": "TVSettingsShortcut-v2.apk",
    "projectivy": "ProjectivyLauncher-4.73.apk",
    "ltv": "LTvLauncher-armeabi-v7a-release.apk",
}
RELEASE_REPOSITORY = "pouyaSamie/SamTv-Custom-launchers"
APK_SHA256 = {
    "bridge": "2c6bb6f7d87d475e5c8d03603627b7cb1a7a107a788b1169d9e466c23194edae",
    "virtualkey": "23424366a94ea0314669dd3fc264b803058ca20b96006f001d992f26f6f62cff",
    "choose": "6be9cc241817b9c0b16974893a67e4b8dd82352ae0f3cb85d8c9db7b4476bf30",
    "settings": "a0c537caf58860ad455f7501ecaa783be6a1cd9ec699e24ca953af287248c0d5",
    "projectivy": "74e33af1e5e13831a69a0669d2b68b02150bf9df1ae1df437dc67e3f8d52c790",
    "ltv": "99eedb0136bd5ea5b17a6fa955b693fc44093a53bfbf353cf37277f9a45ed710",
}
APK_URLS = {
    **{key: f"https://github.com/{RELEASE_REPOSITORY}/releases/download/v{VERSION}/{APKS[key]}"
       for key in ("bridge", "virtualkey", "choose", "settings")},
    "projectivy": "https://github.com/spocky/miproja1/releases/download/4.73/ProjectivyLauncher-4.73-c98-xda-release.apk",
    "ltv": "https://github.com/leanbitlab-org/LtvLauncher/releases/download/v2026.10.27/LTvLauncher-armeabi-v7a-release.apk",
}
HOME_RECEIVER = "com.realtek.tv/.receiver.HomeKeyReceiver"
PROJECTIVY_HOME = "com.spocky.projengmenu/com.spocky.projengmenu.ui.home.MainActivity"
LTV_HOME = "com.leanbitlab.ltvL/com.leanbitlab.ltvL.MainActivity"
BACKUP_PACKAGES = (
    "org.pouya.tvhomebridge",
    "org.pouya.tvhomeselectshortcut",
    "org.pouya.tvsettingsshortcut",
    "com.spocky.projengmenu",
    "com.leanbitlab.ltvL",
    "com.example.tl_virtualkey",
)


class SetupError(Exception):
    pass


PENDING_CHOICE_KEYS: list[str] = []


def tr(language: str, fa: str, en: str) -> str:
    return fa if language == "fa" else en


def say(language: str, fa: str, en: str) -> None:
    print(tr(language, fa, en), flush=True)


def adb_executable() -> str:
    overridden = os.environ.get("ADB")
    if overridden:
        return overridden
    bundled = ROOT / "tools" / ("adb.exe" if os.name == "nt" else "adb")
    if bundled.is_file():
        return str(bundled)
    found = shutil.which("adb")
    if found:
        return found
    raise SetupError("ADB is missing from the installer package.")


class Device:
    def __init__(self, serial: str):
        self.serial = serial
        self.adb = adb_executable()

    def run(self, *args: str, timeout: int = 90) -> str:
        command = [self.adb, "-s", self.serial, *args]
        try:
            result = subprocess.run(command, text=True, capture_output=True, timeout=timeout, check=False)
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise SetupError(f"ADB could not run: {exc}") from exc
        if result.returncode != 0:
            detail = (result.stderr or result.stdout).strip()
            if "INSTALL_FAILED_UPDATE_INCOMPATIBLE" in detail:
                raise SetupError("The TV rejected an app signature. If setup had already started, use Restore.")
            if "INSTALL_FAILED_INSUFFICIENT_STORAGE" in detail or "No space left" in detail:
                raise SetupError("The TV has too little free space.")
            if "device offline" in detail or "device not found" in detail or "unable to connect" in detail:
                raise SetupError("Connection to the TV was lost. Check the network and ADB permission.")
            raise SetupError(f"ADB failed: {' '.join(args)}\n{detail}")
        return result.stdout.strip()

    def connect(self) -> None:
        if ":" in self.serial:
            try:
                subprocess.run([self.adb, "connect", self.serial], capture_output=True,
                               text=True, timeout=20, check=False)
            except (OSError, subprocess.TimeoutExpired) as exc:
                raise SetupError(f"Could not connect to TV: {exc}") from exc
        try:
            state = self.run("get-state", timeout=20)
        except SetupError as exc:
            raise SetupError("TV connection failed. Check the IP, network, and ADB permission on the TV.") from exc
        if state != "device":
            raise SetupError("TV is unavailable or ADB permission was not accepted.")

    def shell(self, *args: str) -> str:
        return self.run("shell", *args)

    def pull_package(self, package: str, target: Path) -> None:
        paths = self.shell("pm", "path", package).splitlines()
        sources = [line.removeprefix("package:") for line in paths if line.startswith("package:")]
        if len(sources) != 1:
            raise SetupError(f"Required TV app is missing: {package}")
        self.run("pull", sources[0], str(target), timeout=180)

    def package_path(self, package: str) -> str | None:
        listed = self.shell("pm", "list", "packages", package).splitlines()
        if f"package:{package}" not in listed:
            return None
        paths = [line.removeprefix("package:") for line in
                 self.shell("pm", "path", package).splitlines() if line.startswith("package:")]
        if len(paths) > 1:
            raise SetupError(f"Cannot back up split APKs for {package}")
        return paths[0] if paths else None


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def check_compatibility(device: Device, working: Path,
                        experimental: bool = False) -> tuple[Path, Path]:
    model = device.shell("getprop", "ro.product.model")
    android = device.shell("getprop", "ro.build.version.release")
    hardware = device.shell("getprop", "ro.hardware")
    board = device.shell("getprop", "ro.product.board")
    print(f"TV: {model}, Android {android}, {hardware} / {board}")
    if android != "11":
        raise SetupError("This installer requires Android 11. Nothing was installed.")
    if not experimental and (model != "R4" or "2851" not in (hardware + board).lower()):
        raise SetupError("This TV version has not been verified. Nothing was installed.")
    realtek = working / "RtkLiveTv.apk"
    virtualkey = working / "Tl_VirtualKey.apk"
    device.pull_package("com.realtek.tv", realtek)
    # pm path may point to an installed update; this hash checks the active TV APK.
    # VirtualKey is read from its original system path below.
    if not device.shell("pm", "path", "com.example.tl_virtualkey").startswith("package:"):
        raise SetupError("Required TV app is missing: com.example.tl_virtualkey")
    device.run("pull", ORIGINAL_VIRTUALKEY_PATH, str(virtualkey), timeout=180)
    if not experimental and (sha256(realtek) != TESTED_REALTEK or
                             sha256(virtualkey) != TESTED_VIRTUALKEY):
        raise SetupError("The TV software differs from the tested version. Nothing was installed.")
    for package in ("com.realtek.menu", "com.google.android.tvlauncher"):
        if not device.shell("pm", "path", package).startswith("package:"):
            raise SetupError(f"Required TV app is missing: {package}")
    if "rtk-framework" not in device.shell("pm", "list", "libraries"):
        raise SetupError("Realtek framework is missing. Nothing was installed.")
    if "uid=0(root)" not in device.shell("su", "0", "id"):
        raise SetupError("This TV does not provide the root access needed for the Home receiver. Nothing was installed.")
    if experimental and "com.realtek.tv.receiver.HomeKeyReceiver" not in device.shell(
            "dumpsys", "package", "com.realtek.tv"):
        raise SetupError("The required Home receiver is missing. Nothing was installed.")
    return realtek, virtualkey


def inspect_device(device: Device, language: str) -> None:
    """Read candidate-TV capabilities without installing or changing settings."""
    properties = (
        ("Model", "ro.product.model"),
        ("Android", "ro.build.version.release"),
        ("Hardware", "ro.hardware"),
        ("Board", "ro.product.board"),
        ("Software", "ro.software.version_id"),
    )
    say(language, "مشخصات تلویزیون (هیچ تنظیمی تغییر نمی‌کند):",
        "TV information (no settings are changed):")
    for label, property_name in properties:
        print(f"{label}: {device.shell('getprop', property_name) or '—'}")
    for package in ("com.realtek.tv", "com.example.tl_virtualkey",
                    "com.realtek.menu", "com.google.android.tvlauncher"):
        path = device.package_path(package)
        print(f"{package}: {'present' if path else 'missing'}")
    libraries = device.shell("pm", "list", "libraries")
    print(f"rtk-framework: {'present' if 'rtk-framework' in libraries else 'missing'}")
    try:
        root = "uid=0(root)" in device.shell("su", "0", "id")
    except SetupError:
        root = False
    print(f"ADB root: {'available' if root else 'unavailable'}")
    say(language,
        "این فقط شناسایی اولیه است؛ Home و HDMI آزمایش نشده‌اند و نصب معمولی برای این مدل تأیید نشده است.",
        "This is discovery only. Home and HDMI were not tested; normal installation is not approved for this model.")


def required_apks(device: Device, choose: bool, settings: bool,
                  projectivy: bool, ltv: bool) -> list[str]:
    keys = ["bridge", "virtualkey"]
    if choose:
        keys.append("choose")
    if settings:
        keys.append("settings")
    if projectivy and not device.package_path("com.spocky.projengmenu"):
        keys.append("projectivy")
    if ltv and not device.package_path("com.leanbitlab.ltvL"):
        keys.append("ltv")
    return keys


def verify_bundle(apk_dir: Path, keys: list[str]) -> None:
    for key in keys:
        path = apk_dir / APKS[key]
        if not path.is_file():
            raise SetupError(f"Missing installation file: {path.name}")
        if sha256(path) != APK_SHA256[key]:
            raise SetupError(f"Checksum failed: {path.name}")


def download_apks(apk_dir: Path, keys: list[str]) -> None:
    apk_dir.mkdir(parents=True, exist_ok=True)
    for key in keys:
        target = apk_dir / APKS[key]
        if target.is_file() and sha256(target) == APK_SHA256[key]:
            continue
        url = APK_URLS[key]
        print(f"Downloading {target.name} ...", flush=True)
        temporary = target.with_name(target.name + ".part")
        try:
            request = urllib.request.Request(url, headers={"User-Agent": f"SAM-TV-Launcher/{VERSION}"})
            with urllib.request.urlopen(request, timeout=30) as response, temporary.open("wb") as output:
                if response.geturl().split(":", 1)[0] != "https":
                    raise SetupError(f"Insecure download redirect: {target.name}")
                digest = hashlib.sha256()
                total = 0
                while chunk := response.read(1024 * 1024):
                    total += len(chunk)
                    if total > 100 * 1024 * 1024:
                        raise SetupError(f"Download is unexpectedly large: {target.name}")
                    output.write(chunk)
                    digest.update(chunk)
            if digest.hexdigest() != APK_SHA256[key]:
                raise SetupError(f"Checksum failed: {target.name}")
            temporary.replace(target)
        except (OSError, urllib.error.URLError) as exc:
            raise SetupError(f"Could not download {target.name} from {url}: {exc}. Check the computer's internet connection.") from exc
        finally:
            temporary.unlink(missing_ok=True)
    verify_bundle(apk_dir, keys)


def device_identity(device: Device) -> str:
    android_id = device.shell("settings", "get", "secure", "android_id")
    if not android_id or android_id == "null":
        raise SetupError("Cannot identify this TV for a safe restore.")
    return hashlib.sha256(android_id.encode("utf-8")).hexdigest()


def home_receiver_state(device: Device) -> str:
    details = device.shell("dumpsys", "package", "com.realtek.tv")
    if "User 0:" not in details:
        raise SetupError("Cannot read the current Home receiver state.")
    group = "default"
    for line in details.split("User 0:", 1)[1].splitlines():
        entry = line.strip()
        if entry == "Queries:":
            break
        if entry in {"disabledComponents:", "enabledComponents:"}:
            group = "disabled" if entry.startswith("disabled") else "enabled"
        elif entry == "com.realtek.tv.receiver.HomeKeyReceiver":
            return group
    return "default"


def save_restore_point(device: Device, backup: Path) -> None:
    packages = {}
    package_dir = backup / "packages"
    package_dir.mkdir()
    for package in BACKUP_PACKAGES:
        source = device.package_path(package)
        is_system_virtualkey = package == "com.example.tl_virtualkey" and source == ORIGINAL_VIRTUALKEY_PATH
        filename = None
        digest = None
        if source and not is_system_virtualkey:
            filename = package + ".apk"
            target = package_dir / filename
            device.run("pull", source, str(target), timeout=180)
            digest = sha256(target)
        packages[package] = {"present": bool(source), "system_only": is_system_virtualkey,
                             "file": filename, "sha256": digest}
    home = device.shell("cmd", "package", "resolve-activity", "--brief",
                        "-a", "android.intent.action.MAIN", "-c", "android.intent.category.HOME")
    home = home.splitlines()[-1] if home else ""
    if "/" not in home or "ResolverActivity" in home:
        raise SetupError("Cannot identify the current default Home app.")
    state = {
        "schema": 2,
        "device_id_hash": device_identity(device),
        "home_activity": home,
        "home_receiver": home_receiver_state(device),
        "selected_launcher": device.shell("settings", "get", "global", "tv_home_bridge_home_component"),
        "color_action": device.shell("settings", "get", "global", "tv_home_bridge_color_action"),
        "packages": packages,
    }
    (backup / "state.json").write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")


def load_restore_point(device: Device) -> tuple[Path, dict]:
    backup_root = ROOT / "backups"
    identity = device_identity(device)
    for backup in sorted(backup_root.glob("*/state.json"),
                         key=lambda path: path.stat().st_mtime_ns, reverse=True):
        try:
            state = json.loads(backup.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if state.get("schema") != 2 or state.get("device_id_hash") != identity:
            continue
        directory = backup.parent
        records = state.get("packages")
        if (not isinstance(records, dict) or
                any(not isinstance(records.get(package), dict) for package in BACKUP_PACKAGES) or
                any(not isinstance(state.get(name), str) for name in
                    ("home_activity", "home_receiver", "selected_launcher", "color_action"))):
            raise SetupError(f"Recovery backup is invalid: {backup}")
        for package in BACKUP_PACKAGES:
            record = records[package]
            if (record.get("file") not in {None, package + ".apk"} or
                    not isinstance(record.get("present"), bool) or
                    not isinstance(record.get("system_only"), bool)):
                raise SetupError(f"Recovery backup is invalid: {backup}")
            if record["file"]:
                target = directory / "packages" / record["file"]
                if not target.is_file() or sha256(target) != record.get("sha256"):
                    raise SetupError(f"Recovery backup is incomplete or changed: {target}")
        return directory, state
    raise SetupError("No complete backup for this TV was found in this installer folder.")


def restore_setting(device: Device, name: str, value: str) -> None:
    if value == "null":
        device.shell("settings", "delete", "global", name)
    else:
        device.shell("settings", "put", "global", name, value)


def install(device: Device, language: str, choose: bool, settings: bool,
            projectivy: bool, ltv: bool, apk_dir: Path | None = None,
            experimental: bool = False) -> None:
    with tempfile.TemporaryDirectory(prefix="samtv-check-") as temporary:
        realtek, virtualkey = check_compatibility(device, Path(temporary), experimental=experimental)
        keys = required_apks(device, choose, settings, projectivy, ltv)
        if apk_dir is None:
            apk_dir = ROOT / "downloads"
            download_apks(apk_dir, keys)
        else:
            verify_bundle(apk_dir, keys)
        backup = ROOT / "backups" / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        backup.mkdir(parents=True, exist_ok=False)
        shutil.copy2(realtek, backup / realtek.name)
        shutil.copy2(virtualkey, backup / virtualkey.name)
        save_restore_point(device, backup)
        if experimental:
            verified_backup, _ = load_restore_point(device)
            if verified_backup != backup:
                raise SetupError("The recovery backup could not be verified. Nothing was installed.")
    say(language, f"نسخهٔ پشتیبان در {backup} ذخیره شد.", f"Recovery backup saved at {backup}.")
    try:
        device.run("install", "-r", str(apk_dir / APKS["bridge"]), timeout=180)
        if choose and not experimental:
            device.run("install", "-r", str(apk_dir / APKS["choose"]), timeout=180)
        if settings and not experimental:
            device.run("install", "-r", str(apk_dir / APKS["settings"]), timeout=180)
        device.run("install", "-r", str(apk_dir / APKS["virtualkey"]), timeout=180)
        for selected, package, filename in (
            (projectivy, "com.spocky.projengmenu", APKS["projectivy"]),
            (ltv, "com.leanbitlab.ltvL", APKS["ltv"]),
        ):
            if selected and not device.package_path(package):
                device.run("install", str(apk_dir / filename), timeout=180)
            if selected and not device.package_path(package):
                raise SetupError(f"Launcher was not installed: {package}")
        home_target = PROJECTIVY_HOME if projectivy else LTV_HOME if ltv else \
            "com.google.android.tvlauncher/com.google.android.tvlauncher.MainActivity"
        device.shell("settings", "put", "global", "tv_home_bridge_home_component",
                     home_target)
        device.shell("settings", "put", "global", "tv_home_bridge_color_action", "settings")
        device.shell("am", "start-foreground-service", "-n", "org.pouya.tvhomebridge/.KeyProbeService")
        device.shell("cmd", "package", "set-home-activity", "org.pouya.tvhomebridge/.LauncherRouterActivity")
        if home_receiver_state(device) != "disabled":
            device.shell("su", "0", "pm", "disable-user", "--user", "0", HOME_RECEIVER)
        if home_receiver_state(device) != "disabled":
            raise SetupError("Home receiver did not stay disabled.")
        if experimental:
            say(language,
                "آزمون موقت آماده است. با کنترل واقعی، Home، انتخاب HDMI با یک OK، دکمهٔ چهاررنگ، صدا و تصویر را امتحان کنید.",
                "Trial is ready. With the physical remote, test Home, HDMI selection with one OK, four-color, audio and picture.")
            if not prompt_yes(language,
                              "آیا همهٔ موارد درست کار کردند و می‌خواهید نصب کامل شود؟",
                              "Did everything work, and should installation continue?"):
                raise SetupError("The trial was not approved.")
            device.connect()
            if choose:
                device.run("install", "-r", str(apk_dir / APKS["choose"]), timeout=180)
            if settings:
                device.run("install", "-r", str(apk_dir / APKS["settings"]), timeout=180)
    except (SetupError, EOFError, KeyboardInterrupt) as exc:
        if experimental:
            try:
                restore(device, language)
            except SetupError as rollback_error:
                raise SetupError(
                    f"Trial failed: {exc}. Automatic restore also failed: {rollback_error}\n"
                    f"Recovery backup: {backup}") from exc
            raise SetupError(f"Trial stopped and previous setup was restored: {exc}\n"
                             f"Recovery backup: {backup}") from exc
        raise SetupError(f"Installation stopped: {exc}\nRecovery backup: {backup}") from exc
    say(language, "نصب با موفقیت انجام شد. حالا دکمه‌های Home، Source و چهاررنگ را امتحان کنید.",
        "Installation completed. Now test Home, Source/Input, and the four-color button.")


def restore(device: Device, language: str) -> None:
    backup, state = load_restore_point(device)
    packages = state["packages"]
    # Restore earlier versions before selecting an earlier Home component.
    for package in BACKUP_PACKAGES[:-1]:
        record = packages[package]
        if record["file"]:
            path = device.package_path(package)
            digest = device.shell("sha256sum", path).split() if path else []
            if not digest or digest[0] != record["sha256"]:
                device.run("install", "-r", "-d", str(backup / "packages" / record["file"]), timeout=180)
    restore_setting(device, "tv_home_bridge_home_component", state["selected_launcher"])
    restore_setting(device, "tv_home_bridge_color_action", state["color_action"])
    device.shell("cmd", "package", "set-home-activity", state["home_activity"])
    receiver = state["home_receiver"]
    if home_receiver_state(device) != receiver:
        command = {"disabled": "disable-user", "enabled": "enable", "default": "default-state"}[receiver]
        device.shell("su", "0", "pm", command, "--user", "0", HOME_RECEIVER)
    virtualkey = packages["com.example.tl_virtualkey"]
    if virtualkey["system_only"]:
        if device.package_path("com.example.tl_virtualkey") != ORIGINAL_VIRTUALKEY_PATH:
            device.shell("cmd", "package", "uninstall-system-updates", "com.example.tl_virtualkey")
    elif virtualkey["file"]:
        path = device.package_path("com.example.tl_virtualkey")
        digest = device.shell("sha256sum", path).split() if path else []
        if not digest or digest[0] != virtualkey["sha256"]:
            device.run("install", "-r", "-d", str(backup / "packages" / virtualkey["file"]), timeout=180)
    for package in BACKUP_PACKAGES[:-1]:
        if not packages[package]["present"] and device.package_path(package):
            device.shell("pm", "uninstall", package)
    current_home = device.shell("cmd", "package", "resolve-activity", "--brief",
                                "-a", "android.intent.action.MAIN", "-c", "android.intent.category.HOME")
    if not current_home.splitlines() or current_home.splitlines()[-1] != state["home_activity"]:
        raise SetupError("Restore is incomplete: the previous Home app is not selected.")
    if home_receiver_state(device) != receiver:
        raise SetupError("Restore is incomplete: the Home button receiver differs.")
    for name, previous in (("tv_home_bridge_home_component", state["selected_launcher"]),
                           ("tv_home_bridge_color_action", state["color_action"])):
        if device.shell("settings", "get", "global", name) != previous:
            raise SetupError(f"Restore is incomplete: {name} differs.")
    if virtualkey["system_only"] and device.package_path("com.example.tl_virtualkey") != ORIGINAL_VIRTUALKEY_PATH:
        raise SetupError("Restore is incomplete: the original virtual-key app is not active.")
    for package in BACKUP_PACKAGES[:-1]:
        path = device.package_path(package)
        if bool(path) != packages[package]["present"]:
            raise SetupError(f"Restore is incomplete: {package} differs.")
    for package, record in packages.items():
        if record["file"]:
            path = device.package_path(package)
            digest = device.shell("sha256sum", path).split() if path else []
            if not digest or digest[0] != record["sha256"]:
                raise SetupError(f"Restore is incomplete: {package} has the wrong version.")
    say(language, f"تنظیم قبلی از {backup} بازگردانده شد. تلویزیون را راه‌اندازی مجدد کنید.",
        f"Previous setup restored from {backup}. Restart the TV and test the buttons.")


def read_choice(prompt: str) -> str:
    if not sys.stdin.isatty():
        return input(prompt).strip().lower()
    if os.name == "nt":
        import msvcrt
        print(prompt, end="", flush=True)
        answer = PENDING_CHOICE_KEYS.pop(0) if PENDING_CHOICE_KEYS else msvcrt.getwch()
        if answer == "\x03":
            raise KeyboardInterrupt
        if answer.lower() in {"y", "n"}:
            until = time.monotonic() + 0.1
            while time.monotonic() < until:
                if msvcrt.kbhit():
                    trailing = msvcrt.getwch()
                    if trailing not in {"\r", "\n"}:
                        PENDING_CHOICE_KEYS.append(trailing)
                        break
                else:
                    time.sleep(0.01)
    else:
        import termios
        import tty
        descriptor = sys.stdin.fileno()
        previous = termios.tcgetattr(descriptor)
        try:
            tty.setcbreak(descriptor)
            print(prompt, end="", flush=True)
            answer = PENDING_CHOICE_KEYS.pop(0) if PENDING_CHOICE_KEYS else os.read(descriptor, 1).decode()
            if answer.lower() in {"y", "n"}:
                ready, _, _ = select.select([descriptor], [], [], 0.1)
                if ready:
                    trailing = os.read(descriptor, 1).decode()
                    if trailing not in {"\r", "\n"}:
                        PENDING_CHOICE_KEYS.append(trailing)
        finally:
            termios.tcsetattr(descriptor, termios.TCSADRAIN, previous)
    if not answer:
        raise EOFError
    print("Enter" if answer in {"\r", "\n"} else "Esc" if answer == "\x1b" else answer, flush=True)
    return answer.lower()


def prompt_yes(language: str, fa: str, en: str) -> bool:
    while True:
        prompt = tr(language, fa, en) + tr(language,
                                          " [Y/Enter: بله، N/Esc: نه] ",
                                          " [Y/Enter: yes, N/Esc: no] ")
        answer = read_choice(prompt)
        if answer in {"", "y", "\r", "\n"}:
            return True
        if answer in {"n", "\x1b", "esc"}:
            return False
        say(language, "برای تأیید y یا Enter؛ برای رد کردن n یا Esc را بزنید.",
            "Press y or Enter to accept, or n or Esc to decline.")


def setup(language: str) -> None:
    print(f"SAM TV Launcher {VERSION}")
    say(language, "تلویزیون و رایانه باید به یک شبکهٔ خانگی وصل باشند.",
        "Connect the TV and computer to the same home network.")
    if prompt_yes(language, "نصب معمولی روی مدل آزمایش‌شده انجام شود؟",
                  "Run the normal setup for the tested TV model?"):
        action = "install"
    elif prompt_yes(language, "می‌خواهید روی مدل بررسی‌نشده آزمون آزمایشی انجام دهید؟",
                    "Run an experimental trial on an unverified TV?"):
        action = "experimental"
    elif prompt_yes(language, "می‌خواهید تنظیم قبلی تلویزیون را بازیابی کنید؟",
                    "Restore the previous TV setup?"):
        action = "restore"
    else:
        action = "probe"
    address = input(tr(language, "آدرس IP تلویزیون: ", "TV IP address: ")).strip()
    try:
        ipaddress.ip_address(address)
    except ValueError as exc:
        raise SetupError("Enter a valid TV IP address.") from exc
    device = Device(f"{address}:5555")
    if action == "restore":
        if not prompt_yes(language, "بازیابی تنظیم قبلی شروع شود؟",
                          "Start restoring the previous setup?"):
            say(language, "بازیابی لغو شد.", "Restore cancelled.")
            return
        device.connect()
        restore(device, language)
        return
    if action in {"probe", "experimental"}:
        device.connect()
        inspect_device(device, language)
        if action == "probe":
            if not prompt_yes(language,
                              "فقط اگر خواستید بررسی سخت‌گیرانهٔ نصب را هم اجرا کنید. ادامه می‌دهید؟",
                              "Run the strict installation check too? Continue?"):
                return
            say(language,
                "ادامه فقط در صورت تطابق کامل با نسخهٔ آزمایش‌شده ممکن است؛ این بررسی هم چیزی نصب نمی‌کند.",
                "Installation can continue only if this TV exactly matches the tested profile; this check installs nothing.")
        else:
            say(language,
                "هشدار آزمون: این مسیر روی مدل شما تأیید نشده است. نصب موقت می‌تواند Home یا HDMI را از کار بیندازد. برنامه قبل از تغییر نسخهٔ پشتیبان می‌گیرد و اگر آزمون رد شود، بازیابی را امتحان می‌کند؛ ولی اگر تلویزیون روشن نشود یا ADB قطع شود، بازگشت خودکار ممکن نیست. هیچ پارتیشن فریمور تغییر نمی‌کند.",
                "Experimental warning: this TV has not been verified. The trial may break Home or HDMI. A backup is saved first and the installer attempts restore if the trial fails, but automatic restore cannot work if the TV stops booting or ADB becomes unreachable. Firmware partitions are not changed.")
            if not prompt_yes(language, "خطر را می‌پذیرید و می‌خواهید آزمون را شروع کنید؟",
                              "Do you accept the risk and want to start the trial?"):
                say(language, "آزمون لغو شد؛ چیزی نصب نشد.", "Trial cancelled; nothing was installed.")
                return
    say(language, "در حال اتصال و بررسی سازگاری. اگر پیامی روی تلویزیون آمد، اجازه دهید...",
        "Connecting and checking compatibility. Accept any TV authorization prompt...")
    device.connect()
    with tempfile.TemporaryDirectory(prefix="samtv-check-") as temporary:
        check_compatibility(device, Path(temporary), experimental=action == "experimental")
    if action == "experimental":
        say(language, "پیش‌نیازهای آزمون موجودند؛ سازگاری این مدل هنوز تأیید نشده و چیزی تغییر نکرده است.",
            "Trial prerequisites are present; this model is still unverified and nothing has changed yet.")
    else:
        say(language, "بررسی موفق بود؛ هنوز چیزی روی تلویزیون تغییر نکرده است.",
            "Compatibility check passed; no TV settings have changed yet.")
    choose = prompt_yes(language, "میان‌بر Choose Home نصب شود؟", "Install the Choose Home shortcut?")
    settings = prompt_yes(language, "میان‌بر TV Settings نصب شود؟", "Install the TV Settings shortcut?")
    projectivy = prompt_yes(language, "لانچر Projectivy نصب و پیش‌فرض شود؟ (پیشنهادی)",
                           "Install and select Projectivy Launcher? (recommended)")
    ltv = prompt_yes(language, "لانچر LTvLauncher هم نصب شود؟",
                     "Also install LTvLauncher?")
    say(language,
        "هشدار: نصب، تنظیم دکمه‌ها و صفحهٔ خانه را تغییر می‌دهد. نسخهٔ پشتیبان پیش از تغییر ذخیره می‌شود، اما بازیابی فقط تا زمانی ممکن است که تلویزیون روشن شود و ADB در دسترس باشد. اگر آزمون دکمه‌ها موفق نبود، از همین پوشه گزینهٔ بازیابی را اجرا کنید.",
        "Warning: installation changes Home and remote-button behavior. A backup is saved first, but restore requires the TV to boot and ADB to remain available. If the button test fails, run Restore from this folder.")
    if not prompt_yes(language, "نصب شروع شود؟", "Start installation?"):
        say(language, "نصب لغو شد؛ تغییری انجام نشد.", "Setup cancelled; nothing changed.")
        return
    install(device, language, choose, settings, projectivy, ltv,
            experimental=action == "experimental")


def main() -> int:
    if (getattr(sys, "frozen", False) and os.name != "nt" and len(sys.argv) == 1
            and not sys.stdin.isatty() and os.environ.get("DISPLAY")
            and not os.environ.get("SAMTV_FROM_GUI")):
        terminal = next((shutil.which(name) for name in
                         ("x-terminal-emulator", "gnome-terminal", "konsole", "xterm")
                         if shutil.which(name)), None)
        if terminal:
            environment = os.environ.copy()
            environment["SAMTV_FROM_GUI"] = "1"
            subprocess.Popen([terminal, "-e", sys.executable], env=environment,
                             stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL, start_new_session=True)
            return 0
    parser = argparse.ArgumentParser(description=f"SAM TV Launcher {VERSION}")
    parser.add_argument("command", nargs="?", choices=("setup", "probe", "check", "install", "restore"), default="setup")
    parser.add_argument("--serial", help="TV_IP:5555; required for probe/check/install/restore")
    parser.add_argument("--skip-choose-home", action="store_true")
    parser.add_argument("--skip-tv-settings", action="store_true")
    parser.add_argument("--skip-projectivy", action="store_true")
    parser.add_argument("--install-ltv", action="store_true")
    parser.add_argument("--experimental", action="store_true",
                        help="Run a reversible trial on an unverified Android 11 Realtek TV")
    parser.add_argument("--apk-dir", type=Path, help="Use local verified APKs instead of downloading")
    args = parser.parse_args()
    if args.experimental and args.command != "install":
        parser.error("--experimental is available only with the install command")
    language = "en"
    try:
        if args.command == "setup":
            setup(language)
            return 0
        if not args.serial:
            parser.error("--serial is required for this command")
        device = Device(args.serial)
        device.connect()
        if args.command == "probe":
            inspect_device(device, language)
        elif args.command == "check":
            with tempfile.TemporaryDirectory(prefix="samtv-check-") as temporary:
                check_compatibility(device, Path(temporary))
            say(language, "این تلویزیون برای این نسخه بررسی شد.", "Compatibility check passed.")
        elif args.command == "install":
            if args.experimental:
                say(language,
                    "این نصب آزمایشی ممکن است Home یا HDMI را مختل کند. بازگشت خودکار فقط با روشن‌بودن تلویزیون و اتصال ADB ممکن است.",
                    "This experimental install may disrupt Home or HDMI. Automatic restore needs a booting TV and working ADB.")
                if not prompt_yes(language, "خطر را می‌پذیرید و می‌خواهید ادامه دهید؟",
                                  "Do you accept the risk and want to continue?"):
                    say(language, "آزمون لغو شد.", "Trial cancelled.")
                    return 0
            install(device, language, not args.skip_choose_home, not args.skip_tv_settings,
                    not args.skip_projectivy, args.install_ltv, args.apk_dir,
                    experimental=args.experimental)
        else:
            if prompt_yes(language, "بازیابی تنظیم قبلی شروع شود؟",
                          "Start restoring the previous setup?"):
                restore(device, language)
            else:
                say(language, "بازیابی لغو شد.", "Restore cancelled.")
        return 0
    except (SetupError, EOFError, KeyboardInterrupt) as exc:
        say(language, "نصب کامل نشد. دلیل:", "Setup did not finish. Reason:")
        print(str(exc) or "Cancelled", file=sys.stderr)
        return 1


if __name__ == "__main__":
    result = main()
    if os.environ.get("SAMTV_FROM_GUI"):
        try:
            input("\nPress Enter to close this window: ")
        except EOFError:
            pass
    raise SystemExit(result)
