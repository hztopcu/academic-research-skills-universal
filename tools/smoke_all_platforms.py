from __future__ import annotations

import argparse
import shutil
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ars_universal.installers import install, verify_install  # noqa: E402
from ars_universal.platforms import PLATFORMS, Platform  # noqa: E402


def selected_platforms(stable_only: bool) -> list[Platform]:
    platforms = sorted(PLATFORMS.values(), key=lambda platform: platform.key)
    if stable_only:
        platforms = [platform for platform in platforms if platform.status == "stable"]
    return platforms


def run_smoke(platforms: list[Platform], target_root: Path) -> int:
    failures: list[str] = []
    target_root.mkdir(parents=True, exist_ok=True)

    for platform in platforms:
        target = target_root / platform.key
        if target.exists():
            shutil.rmtree(target)

        print(f"[smoke] installing {platform.key} ({platform.status}) -> {target}")
        try:
            install(platform, target=target)
            errors = verify_install(platform, target=target)
        except Exception as exc:  # pragma: no cover - defensive CLI boundary
            failures.append(f"{platform.key}: {exc}")
            continue

        if errors:
            failures.append(f"{platform.key}: {'; '.join(errors)}")
        else:
            print(f"[smoke] ok {platform.key}")

    if failures:
        print("\nSmoke failures:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    print(f"\nSmoke OK: {len(platforms)} platform(s)")
    return 0


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Install and verify all ARS Universal platform bundles.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--stable-only", action="store_true", help="Only smoke-test stable platforms.")
    group.add_argument("--all", action="store_true", help="Smoke-test stable and experimental platforms.")
    parser.add_argument("--target-root", type=Path, help="Directory for smoke-test installs.")
    parser.add_argument("--keep", action="store_true", help="Keep the temporary smoke-test directory.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    platforms = selected_platforms(stable_only=not args.all)

    if args.target_root:
        return run_smoke(platforms, args.target_root.expanduser().resolve())

    with tempfile.TemporaryDirectory(prefix="ars-platform-smoke-") as tmp:
        target_root = Path(tmp)
        code = run_smoke(platforms, target_root)
        if args.keep:
            keep_root = ROOT / "tmp-install" / "platform-smoke"
            if keep_root.exists():
                shutil.rmtree(keep_root)
            keep_root.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(target_root, keep_root)
            print(f"Kept smoke installs at {keep_root}")
        return code


if __name__ == "__main__":
    raise SystemExit(main())
