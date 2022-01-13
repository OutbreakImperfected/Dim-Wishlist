# This script is for adding the translation of each dimWishlist line before each entry
# It's a pretty simple version, might need some further development

import json
import re
from typing import *

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
        line = f.readline()
        while line != '':
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

                    r += f"== {name} {perks}\n{line}"
                    pass
            else:
                r += line
            line = f.readline()

    return r


if __name__ == '__main__':
    st = interpret_file('data/wishlist')
    print(st)

    with open('data/wishlist_new', 'w', encoding='utf-8') as f:
        f.write(st)
