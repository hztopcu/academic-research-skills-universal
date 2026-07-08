from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json

from .adapters import get_adapter, verify_install
from .platforms import Platform


@dataclass(frozen=True)
class Diagnosis:
    platform: Platform
    target: Path
    adapter: str
    errors: tuple[str, ...]
    warnings: tuple[str, ...]
    manifest: dict[str, object] | None

    @property
    def ok(self) -> bool:
        return not self.errors


def diagnose_install(platform: Platform, target: Path | None = None) -> Diagnosis:
    target = (target or platform.default_target()).expanduser().resolve()
    adapter = get_adapter(platform)
    errors = tuple(verify_install(platform, target))
    warnings: list[str] = []
    manifest = read_manifest(target)

    if platform.status == "experimental":
        warnings.append("platform is experimental; installer verification is available, but manual E2E is still required")

    if manifest and manifest.get("adapter") != adapter.__class__.__name__:
        warnings.append(
            f"manifest adapter is {manifest.get('adapter')}; current adapter is {adapter.__class__.__name__}"
        )

    return Diagnosis(
        platform=platform,
        target=target,
        adapter=adapter.__class__.__name__,
        errors=errors,
        warnings=tuple(warnings),
        manifest=manifest,
    )


def read_manifest(target: Path) -> dict[str, object] | None:
    manifest_path = target / "ars-universal.json"
    if not manifest_path.exists():
        return None
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    return data if isinstance(data, dict) else None
