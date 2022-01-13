import json
import os
import re
from typing import Tuple, Sequence, Optional

from updater import update

if not os.path.isdir('data'):
    os.mkdir('data/')

if not os.path.isfile('data/perks.json') or not os.path.isfile('data/weapons.json'):
    update()

with open('data/perks.json', 'r', encoding='utf8') as f:
    perks_dict = json.load(f)

with open('data/weapons.json', 'r', encoding='utf8') as f:
    weapons_dict = json.load(f)


def extract(raw: str) -> Optional[Tuple[str, Sequence[str]]]:
    ptn = r'dimwishlist:item=(\d*)&perks=(\d*),(\d*),(\d*),(\d*)'
    objs = re.match(ptn, raw)

    if objs is None:
        return None

    matched = objs.groups()

    if len(matched) != 5:
        raise Exception("Unknown string format")

    res = (matched[0], matched[1:5])

    return res


def interpret_file(file: str):
    r = ""
    with open(file, 'r', encoding='utf8') as f:
        lines = f.read()
        return interpret(lines)


def interpret(raw: str):
    lst = raw.split('\n')
    r = ''
    for line in lst:
        if line[0:3] == 'dim':
            data = extract(line)

            if data:
                name = weapons_dict[data[0]]['name']
                perks = []
                for i in data[1]:
                    if i in perks_dict:
                        perks.append(perks_dict[i])
                    else:
                        perks.append('Masterwork')

                r += f"{name} {perks}\n"
                pass
        else:
            r += line + '\n'

    return r


if __name__ == '__main__':
    intp = interpret_file('data/testfile.txt')
    print(intp)
