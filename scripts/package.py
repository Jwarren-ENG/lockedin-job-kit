#!/usr/bin/env python3
"""Build three shareable editions from the audited files in this repository."""
import argparse
import hashlib
import shutil
import zipfile
from pathlib import Path

from audit_release import ROOT, audit


def write_archive(path, members):
    # A clean checkout produces the same archive on every computer.
    with zipfile.ZipFile(path, 'w') as archive:
        for name, content in sorted(members.items()):
            info = zipfile.ZipInfo(name)
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, content, compress_type=zipfile.ZIP_DEFLATED)


def package(destination):
    allowed = {name: (ROOT / name).read_bytes() for name in audit()}
    destination.mkdir(parents=True, exist_ok=True)

    def emit(name, contents):
        target = destination / name
        write_archive(target, contents)
        return target

    def quick_start(edition, guide, starter, app):
        return (
            f'#LOCKEDIN Job Kit | {edition}\n\n'
            f'1. Open {starter} in this folder. Copy all the text.\n'
            f'2. Paste it into a private conversation in {app}. Press Send.\n'
            '3. Share your résumé or work history. Check the extracted facts before answering any new questions.\n\n'
            f'Open {guide} for step by step setup. Keep completed files in a private folder.\n'
        ).encode()

    full = dict(allowed)
    full['START HERE.txt'] = quick_start('Advanced', 'ADVANCED.md', 'editions/ADVANCED_STARTER.txt',
                                         'your assistant with access to the kit folder')
    advanced = emit('lockedin-advanced.zip', full)
    outputs = [advanced]
    for name in ('job-search-kit.plugin', 'job-search-kit.zip'):
        outputs.append(Path(shutil.copyfile(advanced, destination / name)))

    # Include the reading material offline. Only Advanced needs the executable tools.
    guides = ['BEGINNER.md', 'ADVANCED.md', 'LOCAL.md', 'OPTIONAL_OBSIDIAN.md',
              'START_HERE.md', 'references/obsidian.md', 'references/hosts.md',
              'references/tracking.md', 'skills/obsidian/SKILL.md', 'LICENSE']
    shared = {name: allowed[name] for name in guides}
    shared['CHAT_STARTER.txt'] = allowed['CHAT_STARTER.txt']
    shared['editions/LOCAL_STARTER.txt'] = allowed['editions/LOCAL_STARTER.txt']
    for tier, guide, starter in [('lite', 'BEGINNER.md', 'CHAT_STARTER.txt'),
                                 ('local', 'LOCAL.md', 'LOCAL_STARTER.txt')]:
        members = dict(shared)
        app = 'your local model app' if tier == 'local' else 'ChatGPT or Claude'
        members['START HERE.txt'] = quick_start(tier.title(), guide, starter, app)
        if tier == 'local':
            members[starter] = allowed['editions/LOCAL_STARTER.txt']
        members['README.md'] = (
            f'# #LOCKEDIN Job Kit | {tier.title()}\n\n'
            f'Open [{guide}]({guide}) for setup. Copy [{starter}]({starter}) into a new private chat. '
            'Your first step is to share and review your résumé. Next, answer only the missing details.\n\n'
            'The other guides are included for offline reading. Desktop tools referenced in the Advanced guide '
            'come with the separate Advanced download.\n'
        ).encode()
        outputs.append(emit(f'lockedin-{tier}.zip', members))

    starter = destination / 'CHAT_STARTER.txt'
    starter.write_bytes(allowed[starter.name])
    outputs.append(starter)
    lines = [f'{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}\n' for path in sorted(outputs)]
    (destination / 'SHA256SUMS.txt').write_text(''.join(lines))
    return outputs


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('destination', type=Path)
    for artifact in package(parser.parse_args().destination.resolve()):
        print(artifact.name)
