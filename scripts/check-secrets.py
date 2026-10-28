#!/usr/bin/env python3
"""Inspect Git content without displaying secret values."""
import fnmatch
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import sys


def git(*args):
    return subprocess.check_output(['git', *args])


root = Path(git('rev-parse', '--show-toplevel').decode().strip())
mode = sys.argv[1] if len(sys.argv) == 2 else ''
if mode not in ('--staged', '--history'):
    sys.exit('Usage: python3 scripts/check-secrets.py --staged|--history')

patterns = (
    '.env', '.env.*', '*.pem', '*.key', '*.p12', '*.pfx', '*.keystore',
    'id_rsa', 'id_ed25519', 'id_ecdsa', 'id_dsa', '.git-credentials',
    '.netrc', '.npmrc', '.pypirc', 'credentials', 'credentials.json',
    'client_secret*.json', '*service-account*.json', 'secrets.json',
    'secrets.yaml', 'secrets.yml',
)
private_dirs = {'.ssh', '.aws', '.codex', 'private', 'secrets'}
args = ('diff', '--cached', '--name-only', '--diff-filter=ACMR', '-z') if mode == '--staged' else ('ls-files', '-z')
paths = git(*args).decode().split('\0')
blocked = []
for name in filter(None, paths):
    path = PurePosixPath(name)
    if private_dirs.intersection(path.parts[:-1]) or any(fnmatch.fnmatch(path.name, pattern) for pattern in patterns):
        blocked.append(name)
if blocked:
    print('업로드 금지 파일이 포함되어 있습니다. 파일 내용은 출력하지 않습니다.', file=sys.stderr)
    for name in blocked:
        print(f'  {name}', file=sys.stderr)
    sys.exit(1)

if mode == '--staged':
    for role in ('GIT_AUTHOR_IDENT', 'GIT_COMMITTER_IDENT'):
        identity = git('var', role).decode()
        match = re.search(r'<([^>]+)>', identity)
        if not match or not match.group(1).endswith('@users.noreply.github.com'):
            sys.exit('개인 이메일 노출 방지: 이 저장소에는 GitHub noreply 커밋 이메일을 사용해 주세요.')

local_binary = Path(git('rev-parse', '--git-path', 'tools/gitleaks').decode().strip())
binary = str(local_binary.resolve()) if local_binary.is_file() else shutil.which('gitleaks')
if not binary:
    sys.exit('Gitleaks가 없어 업로드를 중단했습니다. 공식 Gitleaks를 설치한 후 다시 시도해 주세요.')

command = [binary, 'git', '--redact=100', '--no-banner', '--no-color', '--ignore-gitleaks-allow']
command += ['--pre-commit', '--staged'] if mode == '--staged' else ['--log-opts=--all']
command += [str(root)]
sys.exit(subprocess.call(command, cwd=root))
