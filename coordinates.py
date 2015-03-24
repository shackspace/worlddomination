#!/usr/bin/env python3

import json
import requests

def main():
    spaces = []
    with open("urls.txt", 'r') as file:
        urls = file.readlines()
        for line in urls:
            url = line.strip()
            url = url.split(':', 1)
            space = {}
            space['name'] = url[0]
            space['url'] = url[1]
            spaces.append(space)
    for space in spaces:
        get_spaceapi_data(space)
    output(spaces)

def output(spaces):
    out = {}
    for space in spaces:
        print(space)
        try:
            out[space['name']] = { 'latitude': space['lat'], 'longitude': space['lon'] }
        except:
            pass
    with open('markers.json', 'w') as markers:
        markers.write(json.dumps(out))



def get_spaceapi_data(space):
    data = requests.get(space['url'], verify=False)
    data = data.json()
    print(space)
    try:
        space['lat'] = data['location']['lat']
        space['lon'] = data['location']['lon']
    except:
        pass


if __name__ == "__main__":
    main()
