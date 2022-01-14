import os
from pprint import pprint
from typing import List

import requests
import json


def update_database(payload: dict):
    """
    Update the local database based on the response received from bungie API
    :param payload: the response received from bungie API
    :return: None
    """
    weapons = {}
    perks = {}

    masterworks = {}

    def pull_perks(target: int) -> List[str]:
        """
        Function for extracting the perk name and hash from the database entry
        :param target: the hash of target perk pool
        :return: return a list of hashes of perks in the perk pool
        """
        res_list = []
        pl = payload['DestinyPlugSetDefinition'][str(target)]['reusablePlugItems']
        for x in pl:
            perk_item = payload['DestinyInventoryItemDefinition'][str(x['plugItemHash'])]
            if str(x['plugItemHash']) not in perks:
                perks[str(x['plugItemHash'])] = perk_item['displayProperties']['name']
            res_list.append(str(x['plugItemHash']))
        return res_list

    # Extract the masterwork and weapon entries from database
    for k, v in payload['DestinyInventoryItemDefinition'].items():
        # Check if it's a masterwork
        if 'plug' in v and 'uiPlugLabel' in v['plug'] and v['plug']['uiPlugLabel'] == 'masterwork':
            rl = v['plug']['plugCategoryIdentifier']
            pl = rl.split('.')
            if len(pl) >= 3 and pl[-2] == 'stat' and pl[2] == 'weapons':
                masterworks[k] = f"M.{pl[-1]}"
            continue
        # Check if it's a weapon
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
                        # print("fix")
                        rnd = False
                    else:
                        # there's always some error data or so
                        # print('Fail')
                        suc = False
                        break
                # Perk pool for specific row
                else:
                    val = lst[pos]['randomizedPlugSetHash']
                    # print(val)
                    perks_list.append(pull_perks(val))

            if suc:
                weapons[k] = {
                    "name": payload['DestinyInventoryItemDefinition'][k]['displayProperties']['name'],
                    "randomness": rnd,
                    "perks": perks_list}

    # Save data
    with open('data/weapons.json', 'w') as f:
        json.dump(weapons, f, indent=2)

    with open('data/perks.json', 'w') as f:
        json.dump(perks, f, indent=2)

    with open('data/masterworks.json', 'w') as f:
        json.dump(masterworks, f, indent=2)


def update(force_update=False):
    """
    Check if there's updates Destiny2 database
    :param force_update: force update the local database
    :return: None
    """
    # Path of Destiny 2 Manifest
    url = "https://www.bungie.net/Platform/Destiny2/Manifest/"
    ret = requests.get(url)
    data = ret.json()

    # Check update
    print("Checking update")
    if os.path.isfile('data/manifest.json'):
        with open('data/manifest.json', 'r') as f:
            old = json.load(f)

            # No update needed
            if old['Response']['version'] == data['Response']['version'] and not force_update:
                print("No update needed")
                return

    # Save new manifest file
    with open('data/manifest.json', 'w') as f:
        print("Saving manifest file")
        json.dump(data, f)

    # Fetch new raw database
    print("Downliading newest database")
    url = f"https://www.bungie.net{data['Response']['jsonWorldContentPaths']['en']}"
    ret = requests.get(url)
    data = ret.json()

    with open('data/en.json', 'w', encoding='utf8') as f:
        print("Saving new database")
        json.dump(data, f)

    # Update local database
    print("Updating database")
    update_database(data)


if __name__ == '__main__':
    update(force_update=True)
