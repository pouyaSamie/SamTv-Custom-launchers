#!/usr/bin/env python3
"""SAM TV Home Bridge 0.1.4 setup and recovery. Standard library only."""

from __future__ import annotations

import argparse
import hashlib
import ipaddress
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone

VERSION = "0.1.4"
ROOT = Path(sys.executable).resolve().parent if getattr(sys, "frozen", False) else Path(__file__).resolve().parent
TESTED_REALTEK = "6b2939ee1e30f2c13534692022831f843aa4f587eeee6991e5fbcf6340cad652"
TESTED_VIRTUALKEY = "3fb39f1da8b17967dddedb7c3828178201e1f474fc7ed097fe3da4111b88e73e"
ORIGINAL_VIRTUALKEY_PATH = "/system_ext/app/Tl_VirtualKey/Tl_VirtualKey.apk"
APKS = {
    "bridge": "TVHomeBridge-v23.apk",
    "virtualkey": "Tl_VirtualKey-mapped.apk",
    "choose": "ChooseHomeShortcut.apk",
    "settings": "TVSettingsShortcut-v2.apk",
}
HOME_RECEIVER = "com.realtek.tv/.receiver.HomeKeyReceiver"
BACKUP_PACKAGES = (
    "org.pouya.tvhomebridge",
    "org.pouya.tvhomeselectshortcut",
    "org.pouya.tvsettingsshortcut",
    "com.example.tl_virtualkey",
)


class SetupError(Exception):
    pass


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
    raise SetupError("ADB is missing. / ابزار ADB در بسته پیدا نشد.")


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
                raise SetupError("The TV rejected an app signature. Nothing else should be changed; use Restore if setup had already started. / امضای برنامه با تلویزیون سازگار نیست؛ اگر نصب شروع شده بود، گزینهٔ بازیابی را اجرا کنید.")
            if "INSTALL_FAILED_INSUFFICIENT_STORAGE" in detail or "No space left" in detail:
                raise SetupError("The TV has too little free space. / فضای خالی تلویزیون کافی نیست.")
            if "device offline" in detail or "device not found" in detail or "unable to connect" in detail:
                raise SetupError("Connection to the TV was lost. Check the network and ADB permission. / اتصال تلویزیون قطع شد؛ شبکه و اجازهٔ ADB را بررسی کنید.")
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
            raise SetupError("TV connection failed. Check the IP, network, and ADB permission on the TV. / اتصال برقرار نشد؛ IP، شبکه و اجازهٔ ADB را بررسی کنید.") from exc
        if state != "device":
            raise SetupError("TV is unavailable or ADB permission was not accepted. / اتصال تلویزیون یا اجازهٔ ADB برقرار نیست.")

    def shell(self, *args: str) -> str:
        return self.run("shell", *args)

    def pull_package(self, package: str, target: Path) -> None:
        paths = self.shell("pm", "path", package).splitlines()
        sources = [line.removeprefix("package:") for line in paths if line.startswith("package:")]
        if len(sources) != 1:
            raise SetupError(f"Required TV app is missing: {package}")
        self.run("pull", sources[0], str(target), timeout=180)

    def package_path(self, package: str) -> str | None:
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


def check_compatibility(device: Device, working: Path) -> tuple[Path, Path]:
    model = device.shell("getprop", "ro.product.model")
    android = device.shell("getprop", "ro.build.version.release")
    hardware = device.shell("getprop", "ro.hardware")
    board = device.shell("getprop", "ro.product.board")
    print(f"TV: {model}, Android {android}, {hardware} / {board}")
    if model != "R4" or android != "11" or "2851" not in (hardware + board).lower():
        raise SetupError("This TV version has not been verified. Nothing was installed. / این مدل هنوز بررسی نشده و چیزی نصب نشد.")
    realtek = working / "RtkLiveTv.apk"
    virtualkey = working / "Tl_VirtualKey.apk"
    device.pull_package("com.realtek.tv", realtek)
    # pm path points at an installed update when one exists. Compare the
    # untouched system APK so a previously configured TV remains eligible.
    if not device.shell("pm", "path", "com.example.tl_virtualkey").startswith("package:"):
        raise SetupError("Required TV app is missing: com.example.tl_virtualkey")
    device.run("pull", ORIGINAL_VIRTUALKEY_PATH, str(virtualkey), timeout=180)
    if sha256(realtek) != TESTED_REALTEK or sha256(virtualkey) != TESTED_VIRTUALKEY:
        raise SetupError("The TV software differs from the tested version. Nothing was installed. / نرم‌افزار تلویزیون با نسخهٔ آزمایش‌شده فرق دارد؛ چیزی نصب نشد.")
    for package in ("com.realtek.menu", "com.google.android.tvlauncher"):
        if not device.shell("pm", "path", package).startswith("package:"):
            raise SetupError(f"Required TV app is missing: {package}")
    if "rtk-framework" not in device.shell("pm", "list", "libraries"):
        raise SetupError("Realtek framework is missing. Nothing was installed.")
    if "uid=0(root)" not in device.shell("su", "0", "id"):
        raise SetupError("This TV does not provide the root access needed for the Home receiver. Nothing was installed.")
    return realtek, virtualkey


def verify_bundle(apk_dir: Path, choose: bool, settings: bool) -> None:
    names = [APKS["bridge"], APKS["virtualkey"]]
    if choose:
        names.append(APKS["choose"])
    if settings:
        names.append(APKS["settings"])
    for name in names:
        if not (apk_dir / name).is_file():
            raise SetupError(f"The setup package is incomplete: {name} / فایل نصب ناقص است.")
    checksum_file = apk_dir / "SHA256SUMS.local"
    if checksum_file.is_file():
        for line in checksum_file.read_text(encoding="utf-8").splitlines():
            expected, filename = line.split(maxsplit=1)
            filename = filename.lstrip("*")
            if Path(filename).name != filename or sha256(apk_dir / filename) != expected:
                raise SetupError(f"The installation file failed its checksum: {filename}")


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
        "schema": 1,
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
        if state.get("schema") != 1 or state.get("device_id_hash") != identity:
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


def install(device: Device, language: str, choose: bool, settings: bool, apk_dir: Path) -> None:
    verify_bundle(apk_dir, choose, settings)
    with tempfile.TemporaryDirectory(prefix="samtv-check-") as temporary:
        realtek, virtualkey = check_compatibility(device, Path(temporary))
        backup = ROOT / "backups" / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        backup.mkdir(parents=True, exist_ok=False)
        shutil.copy2(realtek, backup / realtek.name)
        shutil.copy2(virtualkey, backup / virtualkey.name)
        save_restore_point(device, backup)
    say(language, f"نسخهٔ پشتیبان در {backup} ذخیره شد.", f"Recovery backup saved at {backup}.")
    try:
        device.run("install", "-r", str(apk_dir / APKS["bridge"]), timeout=180)
        if choose:
            device.run("install", "-r", str(apk_dir / APKS["choose"]), timeout=180)
        if settings:
            device.run("install", "-r", str(apk_dir / APKS["settings"]), timeout=180)
        device.run("install", "-r", str(apk_dir / APKS["virtualkey"]), timeout=180)
        device.shell("settings", "put", "global", "tv_home_bridge_home_component",
                     "com.google.android.tvlauncher/com.google.android.tvlauncher.MainActivity")
        device.shell("settings", "put", "global", "tv_home_bridge_color_action", "settings")
        device.shell("am", "start-foreground-service", "-n", "org.pouya.tvhomebridge/.KeyProbeService")
        device.shell("cmd", "package", "set-home-activity", "org.pouya.tvhomebridge/.LauncherRouterActivity")
        if home_receiver_state(device) != "disabled":
            device.shell("su", "0", "pm", "disable-user", "--user", "0", HOME_RECEIVER)
        if home_receiver_state(device) != "disabled":
            raise SetupError("Home receiver did not stay disabled.")
    except SetupError as exc:
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


def prompt_yes(language: str, fa: str, en: str) -> bool:
    answer = input(tr(language, fa, en) + " [Y/n] ").strip().lower()
    return answer not in {"n", "no", "خیر", "نه"}


def setup(language: str) -> None:
    print(f"SAM TV Home Bridge {VERSION}")
    say(language, "تلویزیون و رایانه باید به یک شبکهٔ خانگی وصل باشند.",
        "Connect the TV and computer to the same home network.")
    action = input(tr(language, "کار مورد نظر: [1] نصب  [2] بازگرداندن تنظیم قبلی (Enter = نصب): ",
                      "Choose: [1] Install  [2] Restore previous setup (Enter = Install): ")).strip()
    address = input(tr(language, "آدرس IP تلویزیون: ", "TV IP address: ")).strip()
    try:
        ipaddress.ip_address(address)
    except ValueError as exc:
        raise SetupError("Enter a valid TV IP address. / آدرس IP معتبر وارد کنید.") from exc
    device = Device(f"{address}:5555")
    if action == "2":
        confirmation = input(tr(language, "برای بازیابی، «بازیابی» یا RESTORE را بنویسید: ",
                                "Type RESTORE to continue: ")).strip()
        if confirmation not in {"RESTORE", "بازیابی"}:
            say(language, "بازیابی لغو شد.", "Restore cancelled.")
            return
        device.connect()
        restore(device, language)
        return
    say(language, "در حال اتصال و بررسی سازگاری. اگر پیامی روی تلویزیون آمد، اجازه دهید...",
        "Connecting and checking compatibility. Accept any TV authorization prompt...")
    device.connect()
    with tempfile.TemporaryDirectory(prefix="samtv-check-") as temporary:
        check_compatibility(device, Path(temporary))
    say(language, "بررسی موفق بود؛ هنوز چیزی روی تلویزیون تغییر نکرده است.",
        "Compatibility check passed; no TV settings have changed yet.")
    choose = prompt_yes(language, "میان‌بر Choose Home نصب شود؟", "Install the Choose Home shortcut?")
    settings = prompt_yes(language, "میان‌بر TV Settings نصب شود؟", "Install the TV Settings shortcut?")
    verify_bundle(ROOT / "dist", choose, settings)
    confirmation = input(tr(language, "برای شروع نصب، «نصب» یا INSTALL را بنویسید: ",
                            "Type INSTALL to begin: ")).strip()
    if confirmation not in {"INSTALL", "نصب"}:
        say(language, "نصب لغو شد؛ تغییری انجام نشد.", "Setup cancelled; nothing changed.")
        return
    install(device, language, choose, settings, ROOT / "dist")


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
    parser = argparse.ArgumentParser(description=f"SAM TV Home Bridge {VERSION}")
    parser.add_argument("command", nargs="?", choices=("setup", "check", "install", "restore"), default="setup")
    parser.add_argument("--serial", help="TV_IP:5555; required for check/install/restore")
    parser.add_argument("--language", choices=("fa", "en"))
    parser.add_argument("--skip-choose-home", action="store_true")
    parser.add_argument("--skip-tv-settings", action="store_true")
    parser.add_argument("--apk-dir", type=Path, default=ROOT / "dist")
    args = parser.parse_args()
    language = args.language or ("fa" if args.command == "setup" else "en")
    try:
        if args.command == "setup":
            if args.language is None:
                selection = input("زبان / Language: [1] فارسی  [2] English (Enter = فارسی): ").strip()
                language = "en" if selection == "2" else "fa"
            setup(language)
            return 0
        if not args.serial:
            parser.error("--serial is required for this command")
        device = Device(args.serial)
        device.connect()
        if args.command == "check":
            with tempfile.TemporaryDirectory(prefix="samtv-check-") as temporary:
                check_compatibility(device, Path(temporary))
            say(language, "این تلویزیون برای این نسخه بررسی شد.", "Compatibility check passed.")
        elif args.command == "install":
            install(device, language, not args.skip_choose_home, not args.skip_tv_settings, args.apk_dir)
        else:
            confirmation = input(tr(language, "برای بازیابی، «بازیابی» یا RESTORE را بنویسید: ",
                                    "Type RESTORE to continue: ")).strip()
            if confirmation in {"RESTORE", "بازیابی"}:
                restore(device, language)
            else:
                say(language, "بازیابی لغو شد.", "Restore cancelled.")
        return 0
    except (SetupError, EOFError, KeyboardInterrupt) as exc:
        say(language, "نصب کامل نشد. دلیل:", "Setup did not finish. Reason:")
        print(str(exc) or "Cancelled / لغو شد", file=sys.stderr)
        return 1


if __name__ == "__main__":
    result = main()
    if os.environ.get("SAMTV_FROM_GUI"):
        try:
            input("\nEnter / ورود برای بستن پنجره: ")
        except EOFError:
            pass
    raise SystemExit(result)
