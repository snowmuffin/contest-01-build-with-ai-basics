"""Prepare a disposable offline Windows Sandbox test using the existing native tests.
Downloads only a pinned, hash-checked CPython embeddable ZIP on the HOST.
Python is a test driver, never added to the aquarium package or installed globally.
No guest/host networking, security-policy or feature settings are changed here.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import socket
import subprocess
import urllib.request
import uuid
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PYTHON_URL = 'https://www.python.org/ftp/python/3.13.15/python-3.13.15-embed-amd64.zip'
PYTHON_SHA256 = 'd1f04d990aee1253d8569e8e5104e30fa9f5fa830899f14843448872d936a2cf'
PYTHON_SOURCE = 'https://www.python.org/downloads/release/python-31315/'
SCRIPTS = ['Verify-OfflineGuest.ps1', 'Verify-FeedingNative.py',
           'Verify-G3Native.py', 'Create-FeederShortcut.ps1']


def sha(path: Path) -> str:
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--package-zip', required=True, type=Path)
    parser.add_argument('--output-directory', required=True, type=Path)
    args = parser.parse_args()
    package, out = args.package_zip.resolve(), args.output_directory.resolve()
    artifacts = (ROOT / 'artifacts').resolve()
    if not package.is_relative_to(artifacts) or not package.is_file():
        raise ValueError('Use an existing package ZIP under this project artifacts directory.')
    if not out.is_relative_to(artifacts) or out == artifacts or out.exists():
        raise ValueError('Use a NEW kit directory under project artifacts; never overwrite evidence.')
    for name in SCRIPTS:
        if not (ROOT / 'scripts' / name).is_file():
            raise FileNotFoundError(name)
    with zipfile.ZipFile(package) as archive:
        bad = archive.testzip()
        if bad:
            raise ValueError('ZIP integrity failure: ' + bad)
        build = json.loads(archive.read('DesktopAquarium/BUILD.json').decode('utf-8-sig'))
    inputs, results = out / 'input', out / 'results'
    inputs.mkdir(parents=True)
    results.mkdir()
    shutil.copy2(package, inputs / 'DesktopAquarium-win-x64.zip')
    for name in SCRIPTS:
        shutil.copy2(ROOT / 'scripts' / name, inputs / name)
    runtime = inputs / 'python-embed.zip'
    req = urllib.request.Request(PYTHON_URL, headers={'User-Agent': 'Aquarium-G4-offline-test-kit'})
    with urllib.request.urlopen(req, timeout=45) as response, runtime.open('xb') as stream:
        if response.url != PYTHON_URL:
            raise ValueError('Unexpected Python download redirect; verify it before proceeding.')
        shutil.copyfileobj(response, stream)
    if sha(runtime) != PYTHON_SHA256:
        raise ValueError('Test-only Python archive differs from the official SHA-256.')
    manifest = {
        'kind': 'G4 offline native test kit', 'nonce': uuid.uuid4().hex,
        'host_name': socket.gethostname(), 'host_user': os.environ.get('USERNAME'),
        'source_checkpoint': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
        'application_build': build, 'python_test_driver': {
            'version': '3.13.15', 'url': PYTHON_URL, 'official_checksum_page': PYTHON_SOURCE,
            'sha256': PYTHON_SHA256, 'installed_globally': False,
            'included_in_application_package': False},
        'files': {p.name: {'bytes': p.stat().st_size, 'sha256': sha(p)} for p in inputs.iterdir() if p.is_file()},
        'guest_networking': 'Disable', 'guest_vgpu': 'Disable',
        'manual_acceptance': 'not performed by automation', 'executed': False,
    }
    (inputs / 'kit.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    config = ET.Element('Configuration')
    for name in ['Networking', 'vGPU', 'AudioInput', 'VideoInput',
                 'PrinterRedirection', 'ClipboardRedirection']:
        ET.SubElement(config, name).text = 'Disable'
    ET.SubElement(config, 'MemoryInMB').text = '4096'
    folders = ET.SubElement(config, 'MappedFolders')
    for host, guest, readonly in [(inputs, r'C:\AquariumInput', 'true'),
                                  (results, r'C:\AquariumResults', 'false')]:
        node = ET.SubElement(folders, 'MappedFolder')
        ET.SubElement(node, 'HostFolder').text = str(host)
        ET.SubElement(node, 'SandboxFolder').text = guest
        ET.SubElement(node, 'ReadOnly').text = readonly
    command = ET.SubElement(ET.SubElement(config, 'LogonCommand'), 'Command')
    command.text = r'powershell.exe -NoLogo -NoProfile -File C:\AquariumInput\Verify-OfflineGuest.ps1'
    ET.indent(config)
    path = out / 'Offline-Native.wsb'
    ET.ElementTree(config).write(path, encoding='utf-8', xml_declaration=True)
    (out / 'README.txt').write_text(
        'Open Offline-Native.wsb in Windows Sandbox after inspecting input/kit.json.\n'
        'Networking is disabled only in the guest. input is read-only, results is writable.\n'
        'The guest first initializes the unchanged app with no Python installed/extracted,\n'
        'then extracts the test-only Python driver and runs the existing native tests.\n'
        'No package downloads, SDK installation, policy change or host reboot occurs in the guest script.\n'
        'Read results/acceptance.json; an existing config is NOT a passed test.\n'
        'Do not type into the guest while the bounded native tests run.\n'
        'Final user review and physical-console support remain separate.\n', encoding='utf-8')
    print(json.dumps({'configuration': str(path), 'results': str(results),
                      'python_sha256_verified': True, 'package_sha256': sha(package),
                      'executed': False}))


if __name__ == '__main__':
    main()
