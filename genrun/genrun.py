#!/usr/bin/python3
from sys import argv
from os import system
from os import path
import argparse
import json

''' Loading stuff '''

parser = argparse.ArgumentParser(description="Generate NEK inputs")
parser.add_argument('name', help="Name to assign to generated system")
parser.add_argument('-d', '--dict', dest='config', help="Dictionary of parametesr (JSON)")
parser.add_argument('-u', '--usr', dest='usr', help="*.usr file to use for build")
parser.add_argument('-n', '--nproc', dest='np', type=int, default=-1, help="Number of processes to target")

args = parser.parse_args()
mypath = (path.realpath(__file__))[:-9]

with open(path.join(mypath, "default.json"), "r") as f:
  default_config = json.load(f)

loaded_config = {}
if args.config != None:
  with open(args.config, 'r') as f:
    loaded_config = json.load(f)

config = dict(list(default_config.items()) + list(loaded_config.items()))

with open("./test.json", "w") as f:
  json.dump(config, f, indent=2)

''' Computing stuff '''

# loads the configuration into current variable scope
locals().update(config)

# Manipulate the configuration here
elements_total = shape_mesh[0] * shape_mesh[1] * shape_mesh[2]
if args.np > 0: 
  procs = args.np

# writes the current variable scope to the configuration
config = locals()

''' Writing stuff '''

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

system("echo 'tmp.box' | genbox")
system("mv box.rea "+args.name+".rea")
system("mv box.re2 "+args.name+".re2")
system("echo '"+args.name+"' | genmap")
if args.usr != None:
  system("cp "+ args.usr + " "+args.name+".usr")
system("makenek clean")
system("makenek "+args.name)

