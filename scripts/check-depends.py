#!/usr/bin/env python3
import json
from pathlib import Path
import sys


def main():
    found_components = set([688062441])  # 688062441 in the game's included "RegisterPlus"
    missing_components = set()

    json_files = Path('.').glob('**/*.json')
    for json_file in json_files:
        with open(json_file) as fp:
            circuit = json.load(fp)
            found_components.add(circuit["save_id"])
            missing_components.update(circuit["dependencies"])

    unmet = missing_components - found_components
    if(len(unmet) > 0):
        print("Missing components:", unmet)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
