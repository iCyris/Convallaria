#!/usr/bin/env python3
"""Refresh local Convallaria integration surfaces for Codex and Claude Code."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_JSON = ROOT / ".codex-plugin" / "plugin.json"
CLAUDE_GUIDE_SOURCE = ROOT / "CLAUDE.md"
CLAUDE_COMMAND_SOURCE = ROOT / "claude" / "commands"
CLAUDE_TARGET = ROOT / ".claude"
STALE_COMMANDS = [
    "atelier.md",
    "atelier-brand.md",
    "atelier-logo.md",
    "atelier-optimize.md",
    "atelier-refine.md",
]


def cachebuster() -> str:
    return datetime.now(timezone.utc).strftime("local-%Y%m%d-%H%M%S")


def refreshed_version(version: str, token: str) -> str:
    base = version.split("+", 1)[0]
    return f"{base}+codex.{token}"


def update_plugin_version(dry_run: bool = False) -> tuple[str, str]:
    data = json.loads(PLUGIN_JSON.read_text(encoding="utf-8"))
    before = str(data.get("version", "0.1.0"))
    after = refreshed_version(before, cachebuster())
    data["version"] = after
    if not dry_run:
        PLUGIN_JSON.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return before, after


def sync_file(source: Path, target: Path, dry_run: bool = False) -> bool:
    target.parent.mkdir(parents=True, exist_ok=True)
    source_text = source.read_text(encoding="utf-8")
    current = target.read_text(encoding="utf-8") if target.exists() else None
    changed = current != source_text
    if changed and not dry_run:
        target.write_text(source_text, encoding="utf-8")
    return changed


def sync_claude(dry_run: bool = False) -> list[str]:
    changed = []
    if sync_file(CLAUDE_GUIDE_SOURCE, CLAUDE_TARGET / "CLAUDE.md", dry_run):
        changed.append(str(CLAUDE_TARGET / "CLAUDE.md"))

    for name in STALE_COMMANDS:
        stale = CLAUDE_TARGET / "commands" / name
        if stale.exists():
            changed.append(str(stale))
            if not dry_run:
                stale.unlink()

    for source in sorted(CLAUDE_COMMAND_SOURCE.glob("*.md")):
        target = CLAUDE_TARGET / "commands" / source.name
        if sync_file(source, target, dry_run):
            changed.append(str(target))
    return changed


def marketplace_hint() -> str | None:
    personal = Path.home() / ".agents" / "plugins" / "marketplace.json"
    if not personal.exists():
        return None

    try:
        data = json.loads(personal.read_text(encoding="utf-8"))
    except Exception:
        return None

    name = data.get("name")
    if not isinstance(name, str) or not name:
        return None

    plugins = data.get("plugins", [])
    for plugin in plugins if isinstance(plugins, list) else []:
        if not isinstance(plugin, dict) or plugin.get("name") != "convallaria":
            continue
        source = plugin.get("source", {})
        if isinstance(source, dict) and source.get("source") == "local":
            return f"codex plugin add convallaria@{name}"
    return None


def run_smoke(skip_raster: bool) -> int:
    command = ["python3", str(ROOT / "scripts" / "smoke_test.py")]
    if skip_raster:
        command.append("--skip-raster")
    return subprocess.run(command, cwd=ROOT).returncode


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="Report changes without writing files.")
    parser.add_argument("--no-codex-cachebuster", action="store_true", help="Do not update .codex-plugin/plugin.json.")
    parser.add_argument("--no-claude-sync", action="store_true", help="Do not sync root CLAUDE.md and claude/commands/ into .claude/.")
    parser.add_argument("--smoke", action="store_true", help="Run scripts/smoke_test.py after updating.")
    parser.add_argument("--skip-raster", action="store_true", help="Pass --skip-raster to the smoke test.")
    args = parser.parse_args()

    if not PLUGIN_JSON.exists():
        print(f"error: missing {PLUGIN_JSON}", file=sys.stderr)
        return 1

    if not args.no_codex_cachebuster:
        before, after = update_plugin_version(args.dry_run)
        verb = "would update" if args.dry_run else "updated"
        print(f"{verb}: .codex-plugin/plugin.json version {before} -> {after}", flush=True)

    if not args.no_claude_sync:
        changed = sync_claude(args.dry_run)
        verb = "would sync" if args.dry_run else "synced"
        if changed:
            for path in changed:
                print(f"{verb}: {Path(path).relative_to(ROOT)}", flush=True)
        else:
            print("ok: Claude Code files already in sync", flush=True)

    hint = marketplace_hint()
    if hint:
        print(f"next: {hint}", flush=True)
    else:
        print("next: reinstall the Codex plugin from the marketplace that points at this local checkout", flush=True)

    if args.smoke:
        return run_smoke(args.skip_raster)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
