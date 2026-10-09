#!/usr/bin/env python3
"""Build the Kodi repository site (addon zips, addons.xml, md5, index pages) into _site/."""
import hashlib
import html
import os
import re
import shutil
import subprocess
import sys
import zipfile
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO_ADDON_DIR = os.path.join(ROOT, 'kodi-repo', 'repository.avinashiitd')
OUT = os.path.join(ROOT, '_site')
ZIPS = os.path.join(OUT, 'zips')

# Repo-only files that must not end up inside the plugin zip.
PLUGIN_EXCLUDE_PREFIXES = ('.github/', 'kodi-repo/', '_site/')
PLUGIN_EXCLUDE_FILES = {'.gitignore', '.gitattributes', 'README.md'}


def read_addon(addon_dir):
    with open(os.path.join(addon_dir, 'addon.xml'), encoding='utf-8') as f:
        text = f.read()
    root = ET.fromstring(text.encode('utf-8'))
    assets = [a.text.strip() for a in root.iter() if a.tag in ('icon', 'fanart') and a.text and a.text.strip()]
    return root.get('id'), root.get('version'), text, assets


def tracked_files(addon_dir):
    out = subprocess.run(['git', 'ls-files', '-z'], cwd=addon_dir, check=True, capture_output=True).stdout
    return [p for p in out.decode('utf-8').split('\0') if p]


def write_zip(addon_dir, addon_id, version, files):
    dest_dir = os.path.join(ZIPS, addon_id)
    os.makedirs(dest_dir, exist_ok=True)
    dest = os.path.join(dest_dir, f'{addon_id}-{version}.zip')
    with zipfile.ZipFile(dest, 'w', zipfile.ZIP_DEFLATED) as z:
        for rel in sorted(files):
            z.write(os.path.join(addon_dir, rel), f'{addon_id}/{rel}')
    return dest


def copy_assets(addon_dir, addon_id, assets):
    for rel in assets:
        src = os.path.join(addon_dir, rel)
        if os.path.isfile(src):
            dst = os.path.join(ZIPS, addon_id, rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)


def index_page(title, names):
    links = '\n'.join(f'<a href="{html.escape(n)}">{html.escape(n)}</a><br>' for n in names)
    return f'<!DOCTYPE html>\n<html>\n<head><meta charset="utf-8"><title>{html.escape(title)}</title></head>\n<body>\n{links}\n</body>\n</html>\n'


def main():
    shutil.rmtree(OUT, ignore_errors=True)
    os.makedirs(ZIPS)

    addon_xmls = []

    plugin_id, plugin_ver, plugin_xml, plugin_assets = read_addon(ROOT)
    plugin_files = [p for p in tracked_files(ROOT)
                    if not p.startswith(PLUGIN_EXCLUDE_PREFIXES) and p not in PLUGIN_EXCLUDE_FILES]
    write_zip(ROOT, plugin_id, plugin_ver, plugin_files)
    copy_assets(ROOT, plugin_id, plugin_assets)
    addon_xmls.append(plugin_xml)

    repo_id, repo_ver, repo_xml, repo_assets = read_addon(REPO_ADDON_DIR)
    repo_files = ['addon.xml'] + repo_assets
    repo_zip = write_zip(REPO_ADDON_DIR, repo_id, repo_ver, repo_files)
    copy_assets(REPO_ADDON_DIR, repo_id, repo_assets)
    addon_xmls.append(repo_xml)
    shutil.copy2(repo_zip, OUT)

    body = ''.join(re.sub(r'^\s*<\?xml[^>]*\?>\s*', '', x).rstrip() + '\n\n' for x in addon_xmls)
    addons_xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<addons>\n' + body + '</addons>\n'
    ET.fromstring(addons_xml.encode('utf-8'))
    with open(os.path.join(ZIPS, 'addons.xml'), 'w', encoding='utf-8') as f:
        f.write(addons_xml)
    with open(os.path.join(ZIPS, 'addons.xml.md5'), 'w') as f:
        f.write(hashlib.md5(addons_xml.encode('utf-8')).hexdigest())

    repo_zip_name = os.path.basename(repo_zip)
    with open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(index_page('TMDb Movies Repository', [repo_zip_name]))
    open(os.path.join(OUT, '.nojekyll'), 'w').close()

    print(f'{plugin_id} {plugin_ver}, {repo_id} {repo_ver} -> {OUT}')


if __name__ == '__main__':
    sys.exit(main())
