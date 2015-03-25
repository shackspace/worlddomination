#!/usr/bin/env python3

import json,sys
import requests
directory_url = 'http://spaceapi.net/directory.json'

def main():
    spaces = requests.get(directory_url,verify=False).json()
    out = {}
    for space,url in spaces.items():
        sys.stdout.write(space)
        try:
            ret = requests.get(url,verify=False).json()


            out[space] = ret
            print(" succeeded!")
        except Exception as e:
            print(" failed - url {} - {}".format(space,url,e))


    with open('cache.json', 'w') as markers:
        json.dump(out,markers)


if __name__ == "__main__":
    main()
