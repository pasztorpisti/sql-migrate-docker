#!/usr/bin/env python
import json
import os
import re
import sys


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

    last_id = find_last_tags_id('tags')
    last_path = 'tags/%04d.json' % last_id
    prev_path = 'tags/%04d.json' % (last_id-1)

    with open(prev_path) as f:
        prev = json.load(f)
    with open(last_path) as f:
        last = json.load(f)

    new_scratch_tags = sorted(set(last['scratch_tags']) - set(prev['scratch_tags']))

    diff = set(last['os_tags'].keys()) - set(prev['os_tags'].keys())
    new_os_tags = {tag: last['os_tags'][tag] for tag in diff}

    diff = set(last['aliases'].keys()) - set(prev['aliases'].keys())
    new_aliases = {tag: last['aliases'][tag] for tag in diff}

    intersection = set(last['aliases'].keys()) & set(prev['aliases'].keys())
    updated_aliases = {tag: last['aliases'][tag] for tag in intersection
                       if last['aliases'][tag] != prev['aliases'][tag]}

    new_aliases.update(updated_aliases)

    with open('scratch_tags.txt', "w") as f:
        f.writelines([item+'\n' for item in new_scratch_tags])
    with open('os_tags.txt', "w") as f:
        f.writelines([k+' '+v+'\n' for k, v in new_os_tags.items()])
    with open('aliases.txt', "w") as f:
        f.writelines([k+' '+v+'\n' for k, v in new_aliases.items()])


if __name__ == '__main__':
    main()
