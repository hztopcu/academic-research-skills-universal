# Validation

This project separates automated installer verification from real platform end-to-end validation.

## Validation Levels

| Level | Meaning |
| --- | --- |
| `passed` | Automated install and verification completed successfully. |
| `partial-local` | A local workflow smoke was performed, but not every native platform behavior is covered. |
| `environment-detected` | The platform executable was detected and version checked, but interactive E2E still needs to be recorded. |
| `blocked-not-installed` | The maintainer machine does not currently have that platform installed. |
| `pending-external` | Needs validation from a maintainer or user with access to that platform. |

## Current Registry

The machine-readable validation registry is stored in:

```text
validation/platform-validation.json
```

Every platform in `ars_universal/platforms.py` must have an entry in that registry. CI checks this so unvalidated platforms cannot silently appear.

## Manual E2E Checklist

For each platform:

- Install with the documented command.
- Run `ars <platform> verify --target <target>`.
- Run `ars <platform> diagnose --target <target>`.
- Start the target agent or editor.
- Ask for a literature review outline.
- Ask for a short article draft.
- Ask for a citation check.
- Ask for a peer-review pass.
- Confirm the platform loads the intended skill package or instruction file.
- Record platform version, OS, date, result, and notes.

Use the `Platform validation report` issue template for external validation reports.
