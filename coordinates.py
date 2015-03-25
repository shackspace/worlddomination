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

            try:
                lat = ret['location']['lat'] 
                lon = ret['location']['lon'] 
            except:
                lat = ret['lat']
                lon = ret['lon']

            try:
                o = ret['open']
            except:
                o = False

            out[space] = { 'latitude': lat, 
                    'longitude': lon,
                    'open': o }
            print(" succeeded!")
        except Exception as e:
            print(" failed - url {} - {}".format(space,url,e))


    with open('marker.json', 'w') as markers:
        json.dump(out,marker)


if __name__ == "__main__":
    main()
