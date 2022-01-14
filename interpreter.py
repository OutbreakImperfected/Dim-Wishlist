import json
import os
import re
from typing import Tuple, Sequence, Optional

from updater import update

# Check if data files exist
if not os.path.isdir('data'):
    os.mkdir('data/')

if not os.path.isfile('data/perks.json') \
        or not os.path.isfile('data/weapons.json') \
        or not os.path.isfile('data/masterworks.json'):
    update()

with open('data/perks.json', 'r', encoding='utf8') as f:
    perks_dict = json.load(f)

with open('data/weapons.json', 'r', encoding='utf8') as f:
    weapons_dict = json.load(f)

with open('data/masterworks.json', 'r', encoding='utf8') as f:
    masterwork_dict = json.load(f)


def extract(raw: str) -> Optional[Tuple[str, Sequence[str]]]:
    """
    Processing the provided text
    :param raw: the raw input text
    :return:
        None if the text is not in expected format.
        Tuple consists of hashes of weapon name and perks
    """
    ptn = r'dimwishlist:item=(\d*)&perks=((\d*,)*(\d*))$'
    objs = re.match(ptn, raw)

    if objs is None:
        return None

    matched = objs.groups()

    if len(matched) < 2:
        # Shouldn't be triggered but just in case'
        raise Exception("Unknown string format")

    res = (matched[0], matched[1].split(','))

    return res


def interpret_file(file: str) -> str:
    """
    Read the file and translate it
    I think it hasn't been used yet but just left it here for future use
    :param file: File path
    :return: Translated string
    """
    r = ""
    with open(file, 'r', encoding='utf8') as f:
        lines = f.read()
        return interpret(lines)


def interpret(raw: str, add_raw: bool = False) -> str:
    """
    Function for translating the lines into human readable texts
    :param add_raw: add the raw line before the translation or not
    :param raw: Raw input string
    :return: Translated strings
    """
    lst = raw.split('\n')
    r = ''
    for line in lst:
        if line[0:2] == "==":
            continue
        if line[0:3] == "dim":
            data = extract(line)

            if data:
                name = weapons_dict[data[0]]['name']
                perks = []
                for i in data[1]:
                    if i in masterwork_dict:
                        perks.append(masterwork_dict[i])
                    else:
                        perks.append(perks_dict[i])
                if add_raw:
                    r += line + '\n'
                r += f"{name} {perks}\n"
                pass
        else:
            r += line + '\n'

    return r


if __name__ == '__main__':
    intp = interpret_file('data/wishlist')
    print(intp)
