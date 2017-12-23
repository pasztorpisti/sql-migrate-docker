#!/usr/bin/env python
import json
import os
import re
import sys


def load_scratch_versions():
    tags = []
    for tag in os.listdir('.'):
        if re.match(r'^\d+\.\d+\.\d+$', tag) is None:
            continue
        tags.append(tag)
    latest_version = sorted(tags, key=lambda t: tuple(int(x) for x in t.split('.')))[-1]
    return tags, latest_version


def load_os_dir(dir, ver, latest_ver):
    tags = {}
    aliases = {}

    oses = {}
    for os_name_ver in os.listdir(dir):
        m = re.match(r'^(?P<os>\w+?)(?P<os_ver>\d+(\.\d+)*)$', os_name_ver)
        if m is None:
            continue
        os_name, os_ver = m.group('os'), m.group('os_ver')
        tag = ver + '-' + os_name_ver
        tags[tag] = dir + '/' + os_name_ver
        os_list = oses.setdefault(os_name, [])
        os_list.append({
            'tag': tag,
            'ver': ver,
            'os': os_name,
            'os_ver': os_ver,
        })

    for os_list in oses.values():
        os_list.sort(key=lambda d: tuple(int(x) for x in d['os_ver'].split('.')))
        for item in os_list:
            latest_os_ver = item['os_ver'] == os_list[-1]['os_ver']
            if latest_os_ver:
                aliases[item['ver']+'-'+item['os']] = item['tag']
            if item['ver'] == latest_ver:
                aliases['latest-'+item['os']+item['os_ver']] = item['tag']
                if latest_os_ver:
                    aliases['latest-'+item['os']] = item['tag']

    return tags, aliases


def find_last_tags_id(dir):
    numbers = []
    for entry in os.listdir(dir):
        m = re.match('^(\d{4})\.json$', entry, 0)
        if m is None:
            continue
        numbers.append(int(m.group(1)))
    return max(numbers)


def main():
    os.chdir(os.path.dirname(sys.argv[0]))

    scratch_tags, latest_version = load_scratch_versions()
    aliases = {'latest': latest_version}

    os_tags = {}
    for ver in scratch_tags:
        tags, os_aliases = load_os_dir(ver, ver, latest_version)
        os_tags.update(tags)
        aliases.update(os_aliases)

    last_id = find_last_tags_id('tags')
    last_path = 'tags/%04d.json' % last_id
    with open(last_path) as f:
        prev_tags = json.load(f)

    new_tags = {
        'scratch_tags': sorted(scratch_tags),
        'os_tags': os_tags,
        'aliases': aliases,
    }

    if prev_tags == new_tags:
        print('%s is up to date.' % last_path)
        return

    path = 'tags/%04d.json' % (last_id+1)
    print('Writing %s ...' % path)
    with open(path, 'w') as f:
        json.dump(new_tags, f, indent=4)


if __name__ == '__main__':
    main()
