#!/usr/bin/env python3.6
import json
from pathlib import Path
import subprocess
import re
import math
from typing import Tuple

BASE_PATH = Path('./solutions')


def get_sourcecode():
    source = subprocess.run(['xclip', '-out', '-selection', 'clipboard'], stdout=subprocess.PIPE).stdout
    if source.startswith(b'-- 7 Billion Humans'):
        return source.decode().strip().split('\n')


def read_integer(msg):
    level_id = None
    while not level_id:
        try:
            n = int(input(msg))
        except ValueError:
            print('Invalid number')
        return n


def add_scores(source, size, speed):
    source.insert(3, '')
    source.insert(3, f'-- Speed: {speed}')
    source.insert(3, f'-- Size: {size}')


def get_details(source):
    n, name = re.search('(\d{1,2}): (.+) --', source[1]).groups()
    return int(n), name


def get_target_scores(year):
    with open('challenges.json') as f:
        challenges = json.load(f)
    scores = challenges[str(year)]
    return scores['size_challenge'], scores['speed_challenge']


def get_score(path, category):
    with path.open() as f:
        for line in f.readlines():
            s = line.lower()
            if category in s and 'target' not in s:
                match = re.search(r'\d+', s)
                if match:
                    return int(match.group())
    return math.inf


def save(source, categories, path, scores: Tuple=(math.inf,)):
    if path.exists():
        for category, score in zip(categories, scores):
            old_score = get_score(path, category)
            if score > old_score:
                print(f'Already exists, current solution is better: {str(path):>40}')
                return
    if not path.parent.exists():
        path.parent.mkdir()
    with path.open('w') as f:
        f.write('\n'.join(source))
    print(f'Saved:                                      {str(path):>40}')


def add_solution():
    size = read_integer('Size: ')
    speed = read_integer('Speed: ')

    source = None
    while not source:
        input('Copy the sourcecode to the clipboard and press enter\n')
        source = get_sourcecode()

    add_scores(source, size, speed)

    level_id, level_name = get_details(source)
    target_size, target_speed = get_target_scores(level_id)

    print()
    dirname = f'{level_id:02} - {level_name}'
    if size <= target_size:
        save(source, ['size'], BASE_PATH / dirname / 'size.asm', (size,))
    if speed <= target_speed:
        save(source, ['speed'], BASE_PATH / dirname / 'speed.asm', (speed,))
    if size <= target_size and speed <= target_speed:
        save(source, ['speed', 'size'], BASE_PATH / dirname / 'speed+size.asm', (speed, size))
    print()

    return input('Add another source? [y/N] ').lower() == 'y'


if __name__ == '__main__':
    while add_solution():
        pass
