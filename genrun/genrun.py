#!/usr/bin/env python3

##!/home/maxhutch/anaconda3/bin/python
from sys import argv
from os import system
from os import path
import shutil
import argparse
import json
from mesh import Mesh

class Timer(object):
    def __init__(self, name=None):
        self.name = name

    def __enter__(self):
        import time
        self.tstart = time.time()

    def __exit__(self, type, value, traceback):
        import time
        if self.name:
            print("[{:s}]".format(self.name),)
        print('Elapsed: {:f}'.format(time.time() - self.tstart))

''' Loading stuff '''
parser = argparse.ArgumentParser(description="Generate NEK inputs")
parser.add_argument('name', help="Name to assign to generated system")
parser.add_argument('-d', '--dict', dest='config', help="Dictionary of parametesr (JSON)")
parser.add_argument('-u', '--usr', dest='usr', help="*.usr file to use for build")
parser.add_argument('-n', '--nproc', dest='np', type=int, default=-1, help="Number of processes to target")
parser.add_argument('-m', '--map', dest='map', default=False, action="store_true", help="Map?")
parser.add_argument('--makenek', dest='makenek', default="makenek", help="Path to makenek")
parser.add_argument('-c', '--clean', dest='clean', default=False, action="store_true", help="Clean?")

args = parser.parse_args()
mypath = (path.realpath(__file__))[:-9]

with open(path.join(mypath, "default.json"), "r") as f:
  default_config = json.load(f)

loaded_config = {}
if args.config != None:
  with open(args.config, 'r') as f:
    loaded_config = json.load(f)

config = dict(list(default_config.items()) + list(loaded_config.items()))

with open("./{:s}.json".format(args.name), "w") as f:
  json.dump(config, f, indent=2)

''' Computing stuff '''

# loads the configuration into current variable scope
locals().update(config)

# Manipulate the configuration here
elements_total = shape_mesh[0] * shape_mesh[1] * shape_mesh[2]

if args.np > 0: 
  procs = args.np

if left_bound == 'P':
  left_boundv = 'P'
else:
  left_boundv = 'I'

if right_bound == 'P':
  right_boundv = 'P'
else:
  right_boundv = 'I'

if front_bound == 'P':
  front_boundv = 'P'
else:
  front_boundv = 'I'

if back_bound == 'P':
  back_boundv = 'P'
else:
  back_boundv = 'I'

if top_bound == 'P':
  top_boundv = 'P'
else:
  top_boundv = 'I'

if bottom_bound == 'P':
  bottom_boundv = 'P'
else:
  bottom_boundv = 'I'

# genbox and genmap
with Timer("init_mesh"):
  msh = Mesh(root_mesh, extent_mesh, shape_mesh, [left_bound, front_bound, right_bound, back_bound, top_bound, bottom_bound])
if args.map:
  with Timer("generate_elements"):
    msh.generate_elements()
#mesh_data = msh.get_mesh_data()
#msh.generate_faces()
#fluid_boundaries = msh.get_fluid_boundaries()
#thermal_boundaries = fluid_boundaries.replace('SYM', 'I  ').replace('W  ', 'I  ')
if args.map:
  with Timer("set_map"):
    msh.set_map(procs)
  with Timer("get_map"):
    map_data = msh.get_map()
else:
  map_data = "{:d} 0 {:d} {:d} {:d} 0 0\n".format(
              elements_total, 
              shape_mesh[0],
              shape_mesh[1],
              shape_mesh[2])

# writes the current variable scope to the configuration
config = locals()

''' Writing stuff '''

with open(path.join(mypath, "template.SIZE"), "r") as f:
  size_template = f.read()
size = size_template.format(**config)
with open("./SIZE", "w") as f:
  f.write(size)

with open(path.join(mypath, "template.size_mod"), "r") as f:
  size_template = f.read()
size = size_template.format(**config)
with open("./size_mod.F90", "w") as f:
  f.write(size)

with Timer("write_rea"):
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

with open("./{:s}.map".format(args.name), "w") as f:
  f.write(map_data) 

if args.usr != None:
  with open(args.usr, "r") as f:
    usr_template = f.read()
  usr = usr_template.format(**config)
  with open(args.name + ".usr", "w") as f:
    f.write(usr)

#system("echo 'tmp.box' | genbox")
shutil.copy("tmp.rea", args.name+".rea")
#shutil.copy("box.re2", args.name+".re2")
#with open(".tmp", "w") as f:
#  f.write(args.name + "\n0.05\n")
#system("genmap < .tmp")
from subprocess import call
from os.path import dirname
if args.clean:
  args = [args.makenek, clean, dirname(args.makenek)]
  call(args)
args = [args.makenek, args.name, dirname(args.makenek)]
call(args)

