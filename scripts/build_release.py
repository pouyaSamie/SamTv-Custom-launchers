#!/usr/bin/env python3
"""Build the local Windows and Linux 0.1.4 installation ZIPs."""
from pathlib import Path
import sys
import tarfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from samtv import APKS, sha256, verify_bundle, VERSION  # noqa: E402


def main() -> None:
    if (ROOT / "VERSION").read_text(encoding="utf-8").strip() != VERSION:
        raise SystemExit("Version file and installer version differ")
    project_keys = ("bridge", "virtualkey", "choose", "settings")
    verify_bundle(ROOT / "dist", list(project_keys))
    release_apks = [ROOT / "dist" / APKS[key] for key in project_keys]
    unexpected_apks = sorted(set((ROOT / "dist").glob("*.apk")) -
                             {ROOT / "dist" / name for name in APKS.values()})
    if unexpected_apks:
        raise SystemExit(f"Unexpected APKs in dist: {[p.name for p in unexpected_apks]}")
    output = ROOT.parent / "releases"
    output.mkdir(exist_ok=True)
    common = [
        ROOT / "VERSION", ROOT / "README.md", ROOT / "README.en.md", ROOT / "README.fa.md", ROOT / "LICENSE",
        ROOT / "NOTICE.md", ROOT / "samtv.py",
        ROOT / "docs/INSTALL.en.md", ROOT / "docs/INSTALL.fa.md",
        ROOT / "docs/THIRD-PARTY-NOTICES.md",
    ]
    packages = {
        "windows": [ROOT / "Install-SAM-TV.cmd", *sorted((ROOT / "runtime").iterdir()),
                    ROOT / "tools/adb.exe", ROOT / "tools/AdbWinApi.dll",
                    ROOT / "tools/AdbWinUsbApi.dll", ROOT / "tools/libwinpthread-1.dll",
                    ROOT / "tools/NOTICE.txt"],
        "linux": [ROOT / "Install-SAM-TV", ROOT / "tools/adb", ROOT / "tools/NOTICE.txt"],
    }
    for platform, extra in packages.items():
        files = common + extra
        missing = [str(file) for file in files if not file.is_file()]
        if missing:
            raise SystemExit(f"Missing release inputs for {platform}: {missing}")
        suffix = "zip" if platform == "windows" else "tar.gz"
        destination = output / f"SAM-TV-v{VERSION}-{platform}.{suffix}"
        if platform == "windows":
            with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED,
                                 compresslevel=9) as archive:
                for file in files:
                    archive.write(file, arcname=f"SAM-TV-v{VERSION}/{file.relative_to(ROOT)}")
        else:
            with tarfile.open(destination, "w:gz") as archive:
                for file in files:
                    archive.add(file, arcname=f"SAM-TV-v{VERSION}/{file.relative_to(ROOT)}")
        print(f"Created {destination}")
    for key in project_keys:
        source = ROOT / "dist" / APKS[key]
        destination = output / source.name
        destination.write_bytes(source.read_bytes())
        print(f"Created {destination}")
    assets = sorted(output.glob(f"SAM-TV-v{VERSION}-*")) + [
        output / APKS[key] for key in project_keys]
    manifest = output / f"SHA256SUMS-v{VERSION}"
    manifest.write_text("".join(f"{sha256(path)}  {path.name}\n" for path in assets), encoding="utf-8")
    print(f"Created {manifest}")


if __name__ == "__main__":
    main()
