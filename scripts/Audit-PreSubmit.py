"""Read-only, project-scoped source/history and release-candidate audit.
Findings are evidence for review, not a guarantee that no secret exists.
No publication, token display, history rewrite, or file deletion is performed.
"""
from __future__ import annotations
import argparse, hashlib, json, re, subprocess, zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PATTERNS={
 'private-key':rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
 'github-classic-token':rb'gh[pousr]_[A-Za-z0-9]{30,}',
 'aws-access-key':rb'AKIA[0-9A-Z]{16}',
 'api-secret-assignment':rb'(?i)(?:api[_-]?key|access[_-]?token|client[_-]?secret)\s*[=:]\s*[\"\'][A-Za-z0-9_+/.=-]{28,}[\"\']',
}
def git(*args: str)->bytes:
 return subprocess.check_output(['git',*args],cwd=ROOT)

def main()->None:
 parser=argparse.ArgumentParser();parser.add_argument('--package',required=True);parser.add_argument('--output',required=True)
 args=parser.parse_args();package=Path(args.package).resolve();output=Path(args.output).resolve()
 if not package.is_relative_to(ROOT/'artifacts') or not output.is_relative_to(ROOT/'artifacts'):
  raise ValueError('Package and evidence must remain under project artifacts')
 tracked=git('ls-files','-z').decode().split('\0');tracked=[p for p in tracked if p]
 private=[p for p in tracked if p=='devpost/learner-profile.md' or (p.startswith('devpost/') and p.endswith('.html')) or p.startswith('artifacts/') or Path(p).name in ('.env','.env.local')]
 hits=[];inspected=0
 lines=git('rev-list','--objects','--all').decode().splitlines()
 for line in lines:
  oid,_,path=line.partition(' ')
  if not path or git('cat-file','-t',oid).strip()!=b'blob':continue
  data=git('cat-file','blob',oid);inspected+=1
  for name,pattern in PATTERNS.items():
   if re.search(pattern,data):hits.append({'rule':name,'blob':oid,'path':path})
  if path=='devpost/learner-profile.md' or (path.startswith('devpost/') and path.endswith('.html')):
   hits.append({'rule':'private-local-doc-in-history','blob':oid,'path':path})
 app_project=(ROOT/'src/Aquarium.Core/Aquarium.Core.csproj').read_text(encoding='utf-8')
 isolated=not re.search(r'ProjectReference|PackageReference|UseWPF|UseWindowsForms',app_project)
 runtime=(package/'app/Aquarium.Windows.runtimeconfig.json')
 settings=json.loads(runtime.read_text(encoding='utf-8-sig'))['runtimeOptions']
 inventory=json.loads((package/'FILES.json').read_text(encoding='utf-8-sig'));mismatches=[]
 for item in inventory:
  path=(package/item['path']).resolve()
  if not path.is_relative_to(package):raise ValueError('Unsafe inventory path')
  if not path.is_file() or path.stat().st_size!=item['bytes'] or hashlib.sha256(path.read_bytes()).hexdigest().lower()!=item['sha256'].lower():mismatches.append(item['path'])
 notice_manifests=list((package/'notices').glob('*/provenance.json'))
 source_license=(ROOT/'LICENSE').is_file() or (ROOT/'LICENSE.md').is_file()
 report={'kind':'read-only pre-submission audit','source_head':git('rev-parse','HEAD').decode().strip(),
  'commit_count':int(git('rev-list','--count','HEAD')),'tracked_file_count':len(tracked),'history_blobs_scanned':inspected,
  'private_tracked_paths':private,'credential_pattern_findings':hits,'core_dependency_isolation':isolated,
  'package_inventory_count':len(inventory),'package_inventory_mismatches':mismatches,
  'self_contained':bool(settings.get('includedFrameworks')) and not bool(settings.get('frameworks')),
  'included_frameworks':settings.get('includedFrameworks'), 'upstream_notice_manifests':len(notice_manifests),
  'source_license_selected':source_license,'configured_remote_count':len(git('remote').decode().splitlines()),
  'submitted':False,'published':False,'scope':'Pattern scan plus inventory; does not certify legal compliance or absence of every secret. Git author identities exist as ordinary commit metadata and need owner publication consent.',
  'blocking_owner_items':['final project name and participant-authored submission fields','project license/publication decision','public repository and demo URLs','final package hands-on acceptance','exit survey and current form review']}
 output.parent.mkdir(parents=True,exist_ok=True);output.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(report))
 if private or hits or mismatches or not isolated:raise SystemExit(1)
if __name__=='__main__':main()
