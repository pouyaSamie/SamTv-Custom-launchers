#!/usr/bin/env python3
"""SAM TV Home Bridge 0.1.4 setup and recovery. Standard library only."""

from __future__ import annotations

import argparse
import hashlib
import ipaddress
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
APKS = {
    "bridge": "TVHomeBridge-v23.apk",
    "virtualkey": "Tl_VirtualKey-mapped.apk",
    "choose": "ChooseHomeShortcut.apk",
    "settings": "TVSettingsShortcut-v2.apk",
}


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
        source = next((line.removeprefix("package:") for line in paths if line.startswith("package:")), None)
        if not source:
            raise SetupError(f"Required TV app is missing: {package}")
        self.run("pull", source, str(target), timeout=180)


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
    device.pull_package("com.example.tl_virtualkey", virtualkey)
    if sha256(realtek) != TESTED_REALTEK or sha256(virtualkey) != TESTED_VIRTUALKEY:
        raise SetupError("The TV software differs from the tested version. Nothing was installed. / نرم‌افزار تلویزیون با نسخهٔ آزمایش‌شده فرق دارد؛ چیزی نصب نشد.")
    for package in ("com.realtek.menu", "com.google.android.tvlauncher"):
        if not device.shell("pm", "path", package).startswith("package:"):
            raise SetupError(f"Required TV app is missing: {package}")
    if "rtk-framework" not in device.shell("pm", "list", "libraries"):
        raise SetupError("Realtek framework is missing. Nothing was installed.")
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


def install(device: Device, language: str, choose: bool, settings: bool, apk_dir: Path) -> None:
    verify_bundle(apk_dir, choose, settings)
    with tempfile.TemporaryDirectory(prefix="samtv-check-") as temporary:
        realtek, virtualkey = check_compatibility(device, Path(temporary))
        backup = ROOT / "backups" / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        backup.mkdir(parents=True, exist_ok=False)
        shutil.copy2(realtek, backup / realtek.name)
        shutil.copy2(virtualkey, backup / virtualkey.name)
        for filename, command in (
            ("selected-launcher.txt", ("settings", "get", "global", "tv_home_bridge_home_component")),
            ("color-action.txt", ("settings", "get", "global", "tv_home_bridge_color_action")),
            ("home-activity.txt", ("cmd", "package", "resolve-activity", "--brief", "-a", "android.intent.action.MAIN", "-c", "android.intent.category.HOME")),
        ):
            (backup / filename).write_text(device.shell(*command) + "\n", encoding="utf-8")
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
        device.shell("pm", "disable-user", "--user", "0", "com.realtek.tv/.receiver.HomeKeyReceiver")
    except SetupError as exc:
        raise SetupError(f"Installation stopped: {exc}\nRecovery backup: {backup}") from exc
    say(language, "نصب با موفقیت انجام شد. حالا دکمه‌های Home، Source و چهاررنگ را امتحان کنید.",
        "Installation completed. Now test Home, Source/Input, and the four-color button.")


def restore(device: Device, language: str) -> None:
    device.shell("pm", "enable", "com.realtek.tv/.receiver.HomeKeyReceiver")
    device.shell("cmd", "package", "set-home-activity", "com.google.android.tvlauncher/.MainActivity")
    device.shell("pm", "disable-user", "--user", "0", "org.pouya.tvhomebridge")
    device.shell("cmd", "package", "uninstall-system-updates", "com.example.tl_virtualkey")
    say(language, "تنظیم قبلی بازگردانده شد. تلویزیون را راه‌اندازی مجدد کنید.",
        "Previous Home behavior restored. Restart the TV and test the buttons.")


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
