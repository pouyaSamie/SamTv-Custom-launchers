"""Offline checks for restore safety; no ADB connection is used."""

import json
import hashlib
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
            package = {
                "ProjectivyLauncher-4.73": "com.spocky.projengmenu",
                "LTvLauncher-armeabi-v7a-release": "com.leanbitlab.ltvL",
            }.get(package, package)
            self.paths.setdefault(package, f"/data/app/{package}/base.apk")
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
    def test_download_checks_hash_and_cleans_failed_file(self):
        class Response:
            def __init__(self, payload):
                self.payload = payload

            def __enter__(self):
                return self

            def __exit__(self, *_):
                return False

            def geturl(self):
                return "https://example.test/app.apk"

            def read(self, _size):
                result, self.payload = self.payload, b""
                return result

        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder) / samtv.APKS["bridge"]
            with patch.object(samtv.urllib.request, "urlopen", return_value=Response(b"valid")), \
                 patch.dict(samtv.APK_SHA256, {"bridge": hashlib.sha256(b"valid").hexdigest()}):
                samtv.download_apks(Path(folder), ["bridge"])
            self.assertEqual(target.read_bytes(), b"valid")
            target.unlink()
            with patch.object(samtv.urllib.request, "urlopen", return_value=Response(b"invalid")):
                with self.assertRaisesRegex(samtv.SetupError, "Checksum failed"):
                    samtv.download_apks(Path(folder), ["bridge"])
            self.assertFalse(target.exists())
            self.assertFalse(target.with_name(target.name + ".part").exists())

    def test_failed_download_does_not_change_tv(self):
        device = FakeDevice()
        with tempfile.TemporaryDirectory() as folder, patch.object(samtv, "ROOT", Path(folder)):
            original = Path(folder) / "original.apk"
            original.write_bytes(b"original")
            with patch.object(samtv, "check_compatibility", return_value=(original, original)), \
                 patch.object(samtv, "download_apks", side_effect=samtv.SetupError("offline")):
                with self.assertRaisesRegex(samtv.SetupError, "offline"):
                    samtv.install(device, "en", True, True, True, False)
            self.assertFalse((Path(folder) / "backups").exists())
            self.assertEqual(device.commands, [])

    def test_optional_launchers_install_and_projectivy_is_default(self):
        device = FakeDevice()
        device.paths.pop("com.spocky.projengmenu")
        device.paths.pop("com.leanbitlab.ltvL")
        with tempfile.TemporaryDirectory() as folder, patch.object(samtv, "ROOT", Path(folder)):
            dist = Path(folder) / "dist"
            dist.mkdir()
            for filename in samtv.APKS.values():
                (dist / filename).write_bytes(filename.encode())
            checksums = {key: hashlib.sha256(filename.encode()).hexdigest()
                         for key, filename in samtv.APKS.items()}
            original = Path(folder) / "original.apk"
            original.write_bytes(b"original")
            with patch.object(samtv, "check_compatibility", return_value=(original, original)), \
                 patch.object(samtv, "save_restore_point"), \
                 patch.object(samtv, "APK_SHA256", checksums):
                samtv.install(device, "en", True, True, True, True, dist)
        self.assertIn("com.spocky.projengmenu", device.paths)
        self.assertIn("com.leanbitlab.ltvL", device.paths)
        self.assertEqual(device.settings["tv_home_bridge_home_component"], samtv.PROJECTIVY_HOME)
        self.assertEqual(device.settings["tv_home_bridge_color_action"], "settings")

    def test_restore_stock_state_removes_only_new_apps(self):
        device = FakeDevice()
        with tempfile.TemporaryDirectory() as folder, patch.object(samtv, "ROOT", Path(folder)):
            backup = Path(folder) / "backups" / "20260101T000000Z"
            backup.mkdir(parents=True)
            state = {
                "schema": 2,
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
                "schema": 2,
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
            self.assertEqual(len(installs), len(samtv.BACKUP_PACKAGES))
            self.assertFalse(any(call[:2] == ("pm", "uninstall") for call in device.commands))
            (package_dir / "com.example.tl_virtualkey.apk").write_bytes(b"changed")
            with self.assertRaisesRegex(samtv.SetupError, "incomplete or changed"):
                samtv.load_restore_point(device)


if __name__ == "__main__":
    unittest.main()
