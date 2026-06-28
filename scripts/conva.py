#!/usr/bin/env python3
"""Convallaria project maintenance CLI."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CLAUDE_TARGET = ROOT / ".claude"
CLAUDE_COMMAND_SOURCE = ROOT / "claude" / "commands"


def run(command: list[str]) -> int:
    return subprocess.run(command, cwd=ROOT).returncode


def cmd_sync(args: argparse.Namespace) -> int:
    command = ["python3", str(ROOT / "scripts" / "update_convallaria.py")]
    if args.no_codex_cachebuster:
        command.append("--no-codex-cachebuster")
    if args.no_claude_sync:
        command.append("--no-claude-sync")
    if args.dry_run:
        command.append("--dry-run")
    if args.smoke:
        command.append("--smoke")
    if args.skip_raster:
        command.append("--skip-raster")
    return run(command)


def cmd_doctor(args: argparse.Namespace) -> int:
    command = ["python3", str(ROOT / "scripts" / "smoke_test.py")]
    if args.skip_raster:
        command.append("--skip-raster")
    return run(command)


def cmd_install(args: argparse.Namespace) -> int:
    print("Convallaria install prepares local Claude Code adapters and refreshes Codex plugin metadata.")
    print("For Codex, install or refresh the local plugin entry that points at this checkout.")
    return cmd_sync(args)


def remove_if_generated(path: Path, source: Path | None = None) -> bool:
    if not path.exists() or not path.is_file():
        return False
    if source is not None and source.exists():
        if path.read_text(encoding="utf-8") != source.read_text(encoding="utf-8"):
            return False
    path.unlink()
    return True


def cmd_uninstall(args: argparse.Namespace) -> int:
    removed = []
    guide = CLAUDE_TARGET / "CLAUDE.md"
    if remove_if_generated(guide, ROOT / "CLAUDE.md"):
        removed.append(guide)

    command_target = CLAUDE_TARGET / "commands"
    for source in sorted(CLAUDE_COMMAND_SOURCE.glob("*.md")):
        target = command_target / source.name
        if remove_if_generated(target, source):
            removed.append(target)

    if command_target.exists() and not any(command_target.iterdir()):
        command_target.rmdir()
    if CLAUDE_TARGET.exists() and not any(CLAUDE_TARGET.iterdir()):
        CLAUDE_TARGET.rmdir()

    for path in removed:
        print(f"removed: {path.relative_to(ROOT)}")
    if not removed:
        print("ok: no generated Convallaria Claude Code files were removed")

    print("next: remove the Codex plugin entry for convallaria from your local Codex marketplace or run the matching Codex plugin remove command")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    install = subparsers.add_parser("install", help="Prepare local Codex and Claude Code integrations.")
    install.add_argument("--dry-run", action="store_true")
    install.add_argument("--smoke", dest="smoke", action="store_true", help="Run the smoke test after installing.")
    install.add_argument("--no-smoke", dest="smoke", action="store_false", help="Skip the smoke test after installing.")
    install.set_defaults(smoke=True)
    install.add_argument("--skip-raster", action="store_true")
    install.add_argument("--no-codex-cachebuster", action="store_true")
    install.add_argument("--no-claude-sync", action="store_true")
    install.set_defaults(func=cmd_install)

    sync = subparsers.add_parser("sync", help="Refresh generated local integration surfaces.")
    sync.add_argument("--dry-run", action="store_true")
    sync.add_argument("--smoke", action="store_true")
    sync.add_argument("--skip-raster", action="store_true")
    sync.add_argument("--no-codex-cachebuster", action="store_true")
    sync.add_argument("--no-claude-sync", action="store_true")
    sync.set_defaults(func=cmd_sync)

    update = subparsers.add_parser("update", help="Alias for sync with a smoke test.")
    update.add_argument("--dry-run", action="store_true")
    update.add_argument("--smoke", dest="smoke", action="store_true", help="Run the smoke test after updating.")
    update.add_argument("--no-smoke", dest="smoke", action="store_false", help="Skip the smoke test after updating.")
    update.set_defaults(smoke=True)
    update.add_argument("--skip-raster", action="store_true")
    update.add_argument("--no-codex-cachebuster", action="store_true")
    update.add_argument("--no-claude-sync", action="store_true")
    update.set_defaults(func=cmd_sync)

    doctor = subparsers.add_parser("doctor", help="Run the Convallaria smoke test.")
    doctor.add_argument("--skip-raster", action="store_true")
    doctor.set_defaults(func=cmd_doctor)

    uninstall = subparsers.add_parser("uninstall", help="Remove generated local Claude Code adapters for Convallaria.")
    uninstall.set_defaults(func=cmd_uninstall)

    args = parser.parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
