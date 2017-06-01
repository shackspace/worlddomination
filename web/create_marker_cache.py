#!/usr/bin/env python3

import json,sys
import requests
from multiprocessing import Pool
directory_url = 'http://spaceapi.net/directory.json'

def get_async(su):
    space,url = su
    try:
        ret = requests.get(url,verify=False).json()
    except:
        ret = {}
    return (space,url,ret)

def main():
    p = Pool(20)
    spaces = requests.get(directory_url,verify=False).json()
    out = {}
    print(len(spaces))
    for space,url,ret in p.map(get_async,spaces.items()):
        sys.stdout.write(space)

        if not ret:
            print(" failed - url {} - {}".format(space,url))
        else:
            out[space] = ret
            print(" succeeded!")

    with open('cache.json', 'w') as markers:
        json.dump(out,markers)


if __name__ == "__main__":
    main()
