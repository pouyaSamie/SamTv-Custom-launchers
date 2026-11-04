#!/usr/bin/env python3
"""Build the local Windows and Linux 0.1.4 installation ZIPs."""
from pathlib import Path
import sys
import tarfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from samtv import verify_bundle, VERSION  # noqa: E402


def main() -> None:
    if (ROOT / "VERSION").read_text(encoding="utf-8").strip() != VERSION:
        raise SystemExit("Version file and installer version differ")
    verify_bundle(ROOT / "dist", True, True)
    output = ROOT.parent / "releases"
    output.mkdir(exist_ok=True)
    common = [
        ROOT / "VERSION", ROOT / "README.md", ROOT / "README.fa.md", ROOT / "samtv.py",
        ROOT / "docs/INSTALL.en.md", ROOT / "docs/INSTALL.fa.md",
        ROOT / "docs/THIRD-PARTY-NOTICES.md",
        *sorted((ROOT / "dist").glob("*.apk")), ROOT / "dist/SHA256SUMS.local",
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


if __name__ == "__main__":
    main()
