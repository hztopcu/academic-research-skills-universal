from __future__ import annotations

from argparse import ArgumentParser
from pathlib import Path
import sys

from .installers import install, verify_install
from .platforms import PLATFORMS, resolve_platform


def build_parser() -> ArgumentParser:
    parser = ArgumentParser(prog="ars", description="Install Academic Research Skills on multiple agent platforms.")
    parser.add_argument("platform", nargs="?", help="Platform key, such as claude, codex, cursor, aider, gemini.")
    parser.add_argument("action", nargs="?", default="install", help="Action to run: install or verify.")
    parser.add_argument("--platform", dest="platform_flag", help="Alternative platform selector, e.g. ars install --platform kimi.")
    parser.add_argument("--target", type=Path, help="Override the install target directory.")
    parser.add_argument("--dry-run", action="store_true", help="Print planned writes without changing files.")
    parser.add_argument("--list", action="store_true", help="List supported platforms.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.list:
        for key, platform in sorted(PLATFORMS.items()):
            print(f"{key:12} {platform.label:24} {platform.status}")
        return 0

    platform_name, action = normalize_invocation(args.platform, args.action, args.platform_flag)
    platform = resolve_platform(platform_name)
    if action == "install":
        target = install(platform, target=args.target, dry_run=args.dry_run)
        print(f"Installed {platform.label} support at {target}")
        if not args.dry_run:
            print("Verification: OK")
        for note in platform.notes:
            print(f"- {note}")
    elif action == "verify":
        errors = verify_install(platform, target=args.target)
        if errors:
            print(f"Verification failed for {platform.label}:")
            for error in errors:
                print(f"- {error}")
            return 1
        target = (args.target or platform.default_target()).expanduser().resolve()
        print(f"Verification OK for {platform.label} at {target}")
    else:
        raise SystemExit(f"Unknown action '{action}'. Currently supported: install, verify")
    return 0


def normalize_invocation(platform: str | None, action: str, platform_flag: str | None) -> tuple[str, str]:
    if platform_flag:
        if platform and platform not in {"install", "verify"}:
            raise SystemExit("Use either 'ars <platform> install' or 'ars install --platform <platform>', not both.")
        return platform_flag, platform or "install"

    if platform == "install":
        raise SystemExit("Missing platform. Try: ars codex install")

    if not platform:
        raise SystemExit("Missing platform. Try: ars --list")

    return platform, action


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
