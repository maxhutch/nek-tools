#!/usr/bin/python3
from sys import argv
import json

with open("./default.json", "r") as f:
  default_config = json.load(f)

loaded_config = {}
if len(argv) > 1:
  with open(argv[1], 'r') as f:
    loaded_config = json.load(f)
    print("Loaded config")

config = dict(list(default_config.items()) + list(loaded_config.items()))

with open("./template.rea", "r") as f:
  rea_template = f.read()
rea = rea_template.format(**config)

with open("./tmp.rea", "w") as f:
  f.write(rea)

with open("./template.box", "r") as f:
  box_template = f.read()
box = box_template.format(**config)

with open("./tmp.box", "w") as f:
  f.write(box)

with open("./test.json", "w") as f:
  json.dump(config, f, indent=2)

