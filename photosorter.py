#!/usr/bin/env python3

import os
from pathlib import Path
from datetime import datetime, timedelta
import itertools
import sys
import subprocess

PATH = sys.argv[1]

# TODO: Move to configuration file
EXTENSIONS = {'.RW2', '.JPG', '.JPEG'}
# TODO: Move to configuration too
DESTANATION = Path(subprocess.check_output(
    ['xdg-user-dir', 'PICTURES']
).decode('utf-8').strip()) / 'PhotoSorter'

paths = Path(PATH).rglob('*')
files = filter(lambda p: p.is_file() and p.suffix in EXTENSIONS, paths)


def get_last_modification_date(path):
    return datetime.fromtimestamp(os.stat(path).st_mtime).date()


files_with_dates = map(lambda p: (p, get_last_modification_date(p)), files)
sorted_files_with_dates = sorted(files_with_dates, key=lambda p: p[1])
grouped = itertools.groupby(sorted_files_with_dates, lambda p: p[1])


merged = []
last_date = None
for date, paths in grouped:
    if last_date is None:
        last_date = date
        merged.append([[date], list(paths)])
        continue

    # Merge to the previous group if they differ by just one day
    # otherwise create a new group
    if date - timedelta(days=1) == last_date:
        dates, values = merged[-1]
        dates.append(date)
        merged[-1][1] = list(paths) + values
    else:
        merged.append([[date], list(paths)])
        last_date = date


def genereate_directory_name(dates):
    min_date = min(dates)
    max_date = max(dates)
    max_date_str = max_date.strftime('%d.%m.%Y')

    if min_date.year != max_date.year:
        return min_date.strftime('%d.%m.%Y') + '-' + max_date_str

    if min_date.month != max_date.month:
        return min_date.strftime('%d.%m') + '-' + max_date_str

    if min_date.day != max_date.day:
        return min_date.strftime('%d') + '-' + max_date_str

    return max_date_str


for dates, files in merged:
    dirname = genereate_directory_name(dates)
    destanation = DESTANATION / dirname
    destanation.mkdir()
    files = ' '.join(map(lambda f: f'\'{str(f[0])}\'', files))
    # TODO: Use a proper Python solution
    os.system(f'kioclient5 cp --interactive {files} \'{destanation}\'')
