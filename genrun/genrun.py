#!/usr/bin/python3
from sys import argv
from os import system
from os import path
import argparse
import json

parser = argparse.ArgumentParser(description="Generate NEK inputs")
parser.add_argument('name', help="Name to assign to generated system")
parser.add_argument('-d', '--dict', dest='config', help="Dictionary of parametesr (JSON)")
parser.add_argument('-u', '--usr', dest='usr', help="*.usr file to use for build")

args = parser.parse_args()

mypath = (path.realpath(__file__))[:-9]

with open(path.join(mypath, "default.json"), "r") as f:
  default_config = json.load(f)

loaded_config = {}
if args.config != None:
  with open(args.config, 'r') as f:
    loaded_config = json.load(f)

config = dict(list(default_config.items()) + list(loaded_config.items()))

with open(path.join(mypath, "template.SIZE"), "r") as f:
  size_template = f.read()
size = size_template.format(**config)

with open("./SIZE", "w") as f:
  f.write(size)

with open(path.join(mypath, "template.rea"), "r") as f:
  rea_template = f.read()
rea = rea_template.format(**config)

with open("./tmp.rea", "w") as f:
  f.write(rea)

with open(path.join(mypath, "template.box"), "r") as f:
  box_template = f.read()
box = box_template.format(**config)

with open("./tmp.box", "w") as f:
  f.write(box)

with open("./test.json", "w") as f:
  json.dump(config, f, indent=2)

system("echo 'tmp.box' | genbox")
system("mv box.rea "+args.name+".rea")
system("mv box.re2 "+args.name+".re2")
if args.usr != None:
  system("cp "+ args.usr + " "+args.name+".usr")
system("makenek clean")
system("makenek "+args.name)

