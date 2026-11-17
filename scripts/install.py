#!/usr/bin/env python3
"""Install only this skill; never overwrite a different existing version."""
import argparse
import os
import shutil
from pathlib import Path
from validate import validate


def files(path):
    return {p.relative_to(path).as_posix(): p.read_bytes() for p in path.rglob('*') if p.is_file()}


def install(source, destination, dry_run=False):
    source, destination = Path(source).resolve(), Path(destination).expanduser().absolute()
    if destination.is_symlink():
        raise ValueError(f'Refusing a symlink destination: {destination}')
    if destination.exists():
        if destination.is_dir() and files(source) == files(destination):
            return 'Already installed; no changes.'
        raise ValueError(f'A different skill already exists at {destination}; compare it before updating.')
    if dry_run:
        return f'Would install {source} -> {destination}'
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, destination)
    if files(source) != files(destination):
        raise ValueError('Post-install verification failed')
    return f'Installed and verified: {destination}'


if __name__ == '__main__':
    repo = Path(__file__).resolve().parents[1]
    codex_dir = Path(os.environ.get('CODEX_HOME') or Path.home() / '.codex')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dest', type=Path, default=codex_dir / 'skills/clopos', help='Destination skill folder')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    try:
        validate(repo)
        print(install(repo / 'skills/clopos', args.dest, args.dry_run))
    except (ValueError, OSError) as exc:
        raise SystemExit(str(exc))
