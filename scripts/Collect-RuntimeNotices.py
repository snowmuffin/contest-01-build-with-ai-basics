"""Fetch the exact official .NET distribution notices for a release candidate.
Downloads remain under artifacts; only notice texts plus their provenance enter Git.
This is build-time tooling, never invoked by the application. No host runtime install.
"""
from __future__ import annotations
import argparse, hashlib, json, re, urllib.request, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
METADATA = 'https://builds.dotnet.microsoft.com/dotnet/release-metadata/10.0/releases.json'

def fetch(url: str, path: Path) -> bytes:
    if not url.startswith('https://builds.dotnet.microsoft.com/dotnet/'):
        raise ValueError('Only the official .NET distribution host is accepted')
    with urllib.request.urlopen(url, timeout=60) as response:
        data = response.read(150_000_000)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return data

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', required=True)
    args = parser.parse_args()
    if not re.fullmatch(r'10\.0\.\d+', args.version):
        parser.error('Expected a stable 10.0 patch version')
    out = ROOT / 'artifacts' / 'runtime-notices' / args.version
    out.mkdir(parents=True, exist_ok=True)
    raw = fetch(METADATA, out / 'releases.json')
    metadata = json.loads(raw)
    release = next(item for item in metadata['releases'] if item['release-version'] == args.version)
    target = ROOT / 'notices' / ('dotnet-' + args.version)
    target.mkdir(parents=True, exist_ok=True)
    records = []
    for component in ('runtime', 'windowsdesktop'):
        archive = next(item for item in release[component]['files']
                       if item['rid'] == 'win-x64' and item['name'].endswith('.zip')
                       and 'apphost' not in item['name'])
        path = out / (component + '.zip')
        data = path.read_bytes() if path.exists() else b''
        if hashlib.sha512(data).hexdigest().lower() != archive['hash'].lower():
            data = fetch(archive['url'], path)
        digest = hashlib.sha512(data).hexdigest()
        if digest.lower() != archive['hash'].lower():
            raise RuntimeError(f'Official SHA-512 mismatch for {component}; nothing extracted')
        members = []
        with zipfile.ZipFile(path) as package:
            for member in package.infolist():
                name = Path(member.filename).name
                if name.lower() not in ('license.txt', 'thirdpartynotices.txt', 'third-party-notices.txt', 'notice.txt'):
                    continue
                # Preserve bytes exactly; archive subpaths never become host paths.
                text = package.read(member)
                destination = target / (component + '-' + name)
                if destination.exists() and destination.read_bytes() != text:
                    raise RuntimeError('Refusing conflicting notice text at ' + str(destination))
                destination.write_bytes(text)
                members.append({'archive_path': member.filename,
                                'path': destination.relative_to(ROOT).as_posix(),
                                'bytes': len(text), 'sha256': hashlib.sha256(text).hexdigest()})
        records.append({'component': component, 'source_url': archive['url'],
                        'official_archive_sha512': archive['hash'], 'verified': True,
                        'notices': members})
    supplementary = []
    for project in ('wpf', 'winforms'):
        for name in ('LICENSE.TXT', 'THIRD-PARTY-NOTICES.TXT'):
            url = f'https://raw.githubusercontent.com/dotnet/{project}/v{args.version}/{name}'
            with urllib.request.urlopen(url, timeout=30) as response:
                text = response.read(2_000_000)
            destination = target / (project + '-' + name)
            destination.write_bytes(text)
            supplementary.append({'project': project, 'source_url': url, 'bytes': len(text),
                                  'path': destination.relative_to(ROOT).as_posix(),
                                  'sha256': hashlib.sha256(text).hexdigest()})
    manifest = {'runtime_version': args.version, 'release_date': release['release-date'],
                'metadata_source': METADATA, 'metadata_sha256': hashlib.sha256(raw).hexdigest(),
                'latest_in_live_metadata': metadata['latest-release'],
                'latest_release_date_in_live_metadata': metadata['latest-release-date'],
                'archives': records, 'supplementary_source_notices': supplementary,
                'scope': 'Unmodified notice files from the matching official binary distributions; not a legal audit of the project.'}
    (target / 'provenance.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(manifest))

if __name__ == '__main__':
    main()
