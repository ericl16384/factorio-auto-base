#!/bin/python3
# made by Lonami - lonamiwebs.github.io
import zlib
import json
from sys import argv
from io import BytesIO
from base64 import b64decode, b64encode


def decode(blueprint, out=dict):
    string = zlib.decompress(b64decode(blueprint.encode('ascii')[1:]))
    if out == dict:
        return json.loads(string)
    elif out == str:
        return string.decode('utf-8')
    elif out == bytes:
        return string
    elif callable(out):
        return out(json.dumps(json.loads(string), indent=2, sort_keys=True))
    else:
        raise TypeError('out must be dict, str, bytes or callable')


def encode(data):
    if isinstance(data, dict):
        data = json.dumps(data).encode('utf-8')
    elif isinstance(data, str):
        data = data.encode('utf-8')
    elif not isinstance(data, bytes):
        raise TypeError('data must be dict, str or bytes')
    return '0' + b64encode(zlib.compress(data)).decode('ascii')


__all__ = ['decode', 'encode']


if __name__ == '__main__':
    for blueprint in argv[1:]:
        if '{' in blueprint:
            print(encode(blueprint))
        else:
            decode(blueprint, print)