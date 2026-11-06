"""Offline checks for restore safety; no ADB connection is used."""

import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import samtv


class FakeDevice:
    def __init__(self):
        self.home = "org.pouya.tvhomebridge/.LauncherRouterActivity"
        self.receiver = "disabled"
        self.paths = {package: f"/data/app/{package}/base.apk" for package in samtv.BACKUP_PACKAGES}
        self.hashes = {}
        self.settings = {
            "tv_home_bridge_home_component": "com.spocky.projengmenu/.MainActivity",
            "tv_home_bridge_color_action": "settings",
        }
        self.commands = []

    def package_path(self, package):
        return self.paths.get(package)

    def run(self, *args, **kwargs):
        self.commands.append(args)
        if args[0] == "install":
            package = Path(args[-1]).stem
            self.hashes[self.paths[package]] = samtv.sha256(Path(args[-1]))
        return "Success"

    def shell(self, *args):
        self.commands.append(args)
        if args[:2] == ("su", "0"):
            args = args[2:]
        if args == ("settings", "get", "secure", "android_id"):
            return "test-device-id"
        if args[:3] == ("cmd", "package", "resolve-activity"):
            return "priority=0\n" + self.home
        if args[:3] == ("cmd", "package", "set-home-activity"):
            self.home = args[3]
        if args[:2] == ("dumpsys", "package"):
            if self.receiver == "default":
                return "User 0: enabled=0\nQueries:\n"
            group = "disabledComponents:" if self.receiver == "disabled" else "enabledComponents:"
            return "User 0: enabled=0\n      " + group + "\n        com.realtek.tv.receiver.HomeKeyReceiver\nQueries:\n"
        if args[:2] == ("pm", "default-state"):
            self.receiver = "default"
        if args[:2] == ("pm", "enable"):
            self.receiver = "enabled"
        if args[:2] == ("pm", "disable-user"):
            self.receiver = "disabled"
        if args[:3] == ("cmd", "package", "uninstall-system-updates"):
            self.paths["com.example.tl_virtualkey"] = samtv.ORIGINAL_VIRTUALKEY_PATH
        if args[:2] == ("pm", "uninstall"):
            self.paths.pop(args[2], None)
        if args[:3] == ("settings", "put", "global"):
            self.settings[args[3]] = args[4]
        if args[:3] == ("settings", "delete", "global"):
            self.settings.pop(args[3], None)
        if args[0] == "sha256sum":
            return self.hashes.get(args[1], "missing") + "  " + args[1]
        return "Success"


class RestoreTests(unittest.TestCase):
    def test_restore_stock_state_removes_only_new_apps(self):
        device = FakeDevice()
        with tempfile.TemporaryDirectory() as folder, patch.object(samtv, "ROOT", Path(folder)):
            backup = Path(folder) / "backups" / "20260101T000000Z"
            backup.mkdir(parents=True)
            state = {
                "schema": 1,
                "device_id_hash": samtv.device_identity(device),
                "home_activity": "com.google.android.tvlauncher/.MainActivity",
                "home_receiver": "default",
                "selected_launcher": "null",
                "color_action": "null",
                "packages": {package: {"present": False, "system_only": False,
                                      "file": None, "sha256": None}
                             for package in samtv.BACKUP_PACKAGES},
            }
            state["packages"]["com.example.tl_virtualkey"].update(
                present=True, system_only=True)
            (backup / "state.json").write_text(json.dumps(state), encoding="utf-8")
            samtv.restore(device, "en")
            self.assertEqual(device.home, state["home_activity"])
            self.assertEqual(device.receiver, "default")
            self.assertEqual(device.paths, {
                "com.example.tl_virtualkey": samtv.ORIGINAL_VIRTUALKEY_PATH})
            self.assertNotIn("tv_home_bridge_color_action", device.settings)

    def test_missing_backup_cannot_claim_success(self):
        device = FakeDevice()
        with tempfile.TemporaryDirectory() as folder, patch.object(samtv, "ROOT", Path(folder)):
            with self.assertRaisesRegex(samtv.SetupError, "No complete backup"):
                samtv.restore(device, "en")

    def test_prior_app_versions_are_reinstalled_and_checked(self):
        device = FakeDevice()
        with tempfile.TemporaryDirectory() as folder, patch.object(samtv, "ROOT", Path(folder)):
            backup = Path(folder) / "backups" / "20260101T000000Z"
            package_dir = backup / "packages"
            package_dir.mkdir(parents=True)
            records = {}
            for package in samtv.BACKUP_PACKAGES:
                filename = package + ".apk"
                target = package_dir / filename
                target.write_bytes(package.encode())
                records[package] = {"present": True, "system_only": False,
                                    "file": filename, "sha256": samtv.sha256(target)}
            state = {
                "schema": 1,
                "device_id_hash": samtv.device_identity(device),
                "home_activity": "org.pouya.tvhomebridge/.LauncherRouterActivity",
                "home_receiver": "disabled",
                "selected_launcher": "com.spocky.projengmenu/.MainActivity",
                "color_action": "settings",
                "packages": records,
            }
            (backup / "state.json").write_text(json.dumps(state), encoding="utf-8")
            samtv.restore(device, "en")
            installs = [call for call in device.commands if call[:2] == ("install", "-r")]
            self.assertEqual(len(installs), 4)
            self.assertFalse(any(call[:2] == ("pm", "uninstall") for call in device.commands))
            (package_dir / "com.example.tl_virtualkey.apk").write_bytes(b"changed")
            with self.assertRaisesRegex(samtv.SetupError, "incomplete or changed"):
                samtv.load_restore_point(device)


if __name__ == "__main__":
    unittest.main()
