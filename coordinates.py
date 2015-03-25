#!/usr/bin/env python3

import json
import requests


def main():
    spaces = []

    data = requests.get('http://spaceapi.net/directory.json?api=0.13')
    data = data.json()
    for key in data:
        name = key
        url = data[key]
        space = {}
        space['name'] = name
        space['url'] = url
        spaces.append(space)

    for space in spaces:
        get_spaceapi_data(space)
    output(spaces)


def output(spaces):
    out = {}
    for space in spaces:
        print(space)
        try:
            out[space['name']] = {'latitude': space['lat'],
                                   'longitude': space['lon']}
        except:
            print("no data for spacei %s" % space['name'])
            print(space)
            pass

    with open('marker.json', 'w') as marker:
        marker.write(json.dumps(out))


def get_spaceapi_data(space):
    requests.packages.urllib3.disable_warnings()
    data = requests.get(space['url'], verify=False)
    data = data.json()
    try:
        space['lat'] = data['location']['lat']
        space['lon'] = data['location']['lon']
    except:
        pass


if __name__ == "__main__":
    main()
