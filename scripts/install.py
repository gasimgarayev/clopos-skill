#!/usr/bin/env python3
"""Install this skill; explicit updates retain a complete backup."""
import argparse
import os
import shutil
import tempfile
import uuid
from pathlib import Path
from validate import validate


def files(path):
    result = {}
    for p in path.rglob('*'):
        if p.is_symlink():
            raise ValueError(f'Refusing a symlink inside the skill: {p}')
        if p.is_file():
            result[p.relative_to(path).as_posix()] = p.read_bytes()
    return result


def install(source, destination, dry_run=False, update=False):
    source, destination = Path(source).resolve(), Path(destination).expanduser().absolute()
    if destination.is_symlink():
        raise ValueError(f'Refusing a symlink destination: {destination}')
    if not source.is_dir():
        raise ValueError(f'Skill source is not a directory: {source}')
    resolved_destination = destination.resolve()
    if resolved_destination != source and (
        source.is_relative_to(resolved_destination) or resolved_destination.is_relative_to(source)
    ):
        raise ValueError('Source and destination must not contain one another')
    expected = files(source)
    replacing = False
    if destination.exists():
        if not destination.is_dir():
            raise ValueError(f'Destination is not a directory: {destination}')
        if expected == files(destination):
            return 'Already installed; no changes.'
        if not update:
            raise ValueError(f'A different skill already exists at {destination}; compare it before using --update.')
        replacing = True
    if dry_run:
        if replacing:
            return f'Would back up {destination} and update from {source}; no files changed.'
        return f'Would install {source} -> {destination}'
    destination.parent.mkdir(parents=True, exist_ok=True)
    # Verify a complete staged copy before touching the installed version.
    with tempfile.TemporaryDirectory(prefix='.clopos-stage-', dir=destination.parent) as staging:
        staged = Path(staging) / 'clopos'
        shutil.copytree(source, staged)
        if expected != files(staged):
            raise ValueError('Staged skill verification failed; installed version was not changed')
        backup = None
        if replacing:
            backup = destination.with_name(f'.{destination.name}-backup-{uuid.uuid4().hex}')
            destination.rename(backup)
        try:
            # rename refuses a nonempty destination; never replace an unexpected install.
            staged.rename(destination)
        except OSError:
            if backup is not None and not destination.exists():
                backup.rename(destination)
            raise
    if replacing:
        return f'Updated and verified: {destination}\nPrevious version and local edits retained: {backup}'
    return f'Installed and verified: {destination}'


if __name__ == '__main__':
    repo = Path(__file__).resolve().parents[1]
    codex_dir = Path(os.environ.get('CODEX_HOME') or Path.home() / '.codex')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dest', type=Path, default=codex_dir / 'skills/clopos', help='Destination skill folder')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--update', action='store_true', help='Replace a different version after retaining a full backup')
    args = parser.parse_args()
    try:
        validate(repo)
        print(install(repo / 'skills/clopos', args.dest, args.dry_run, args.update))
    except (ValueError, OSError) as exc:
        raise SystemExit(str(exc))
