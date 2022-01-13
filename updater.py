import os
from pprint import pprint

import requests
import json


def update_database(payload: dict):
    weapons = {}
    perks = {}

    masterworks = {}

    def pull_perks(target: int):
        res_list = []
        pl = payload['DestinyPlugSetDefinition'][str(target)]['reusablePlugItems']
        for x in pl:
            perk_item = payload['DestinyInventoryItemDefinition'][str(x['plugItemHash'])]
            if str(x['plugItemHash']) not in perks:
                perks[str(x['plugItemHash'])] = perk_item['displayProperties']['name']
            res_list.append(str(x['plugItemHash']))
        return res_list

    for k, v in payload['DestinyInventoryItemDefinition'].items():
        if 'plug' in v and 'uiPlugLabel' in v['plug'] and v['plug']['uiPlugLabel'] == 'masterwork':
            rl = v['plug']['plugCategoryIdentifier']
            pl = rl.split('.')
            if len(pl) >= 2 and pl[-2] == 'stat':
                masterworks[k] = (v['plug']['plugCategoryIdentifier'], pl[-1])
            continue
        if 'itemCategoryHashes' in v and 1 in v['itemCategoryHashes'] and v['inventory']['tierType'] == 5:
            print(k, v['displayProperties']['name'])
            # pprint(v)
            lst = v['sockets']['socketEntries']
            suc = True
            perks_list = []
            rnd = True
            for pos in range(0, 5):
                # It's for filtering out some data (but I forgot what exactly)
                if pos == 4 and lst[pos]['socketTypeHash'] != 2614797986:
                    break
                # Weapon frame
                if lst[pos]['socketTypeHash'] == 3956125808:
                    frame_hash = str(lst[pos]['singleInitialItemHash'])
                    frame_prop = payload['DestinyInventoryItemDefinition'][frame_hash]['displayProperties'][
                        'name']
                    perks_list.append([(frame_hash, frame_prop)])
                # Fixed perk weapons
                elif "randomizedPlugSetHash" not in lst[pos]:
                    if "reusablePlugSetHash" in lst[pos]:
                        perks_list.append(pull_perks(lst[pos]['reusablePlugSetHash']))
                        print("fix")
                        rnd = False
                    else:
                        # there's always some error data or so
                        print('Fail')
                        suc = False
                        break
                else:
                    val = lst[pos]['randomizedPlugSetHash']
                    print(val)
                    perks_list.append(pull_perks(val))

            if suc:
                weapons[k] = {
                    "name": payload['DestinyInventoryItemDefinition'][k]['displayProperties']['name'],
                    "randomness": rnd,
                    "perks": perks_list}

    pprint(masterworks)

    with open('data/weapons.json', 'w') as f:
        json.dump(weapons, f, indent=2)

    with open('data/perks.json', 'w') as f:
        json.dump(perks, f, indent=2)


def update(force_update=False):
    # Path of Destiny 2 Manifest
    url = "https://www.bungie.net/Platform/Destiny2/Manifest/"
    ret = requests.get(url)
    data = ret.json()

    # Check update
    if os.path.isfile('data/manifest.json'):
        with open('data/manifest.json', 'r') as f:
            old = json.load(f)

            # No update needed
            if old['Response']['version'] == data['Response']['version'] and not force_update:
                return

    # Save new manifest file
    with open('data/manifest.json', 'w') as f:
        json.dump(data, f)

    # Fetch new raw database
    url = f"https://www.bungie.net{data['Response']['jsonWorldContentPaths']['en']}"
    ret = requests.get(url)
    data = ret.json()

    with open('data/en.json', 'w', encoding='utf8') as f:
        json.dump(data, f)

    # Update local database
    update_database(data)


if __name__ == '__main__':
    update(force_update=True)
