nek-tools
=========

Fork of [tools directory for nek5000](https://github.com/Nek5000/NekTools) to include additional `genrun` tool.

# genrun.py

genrun.py automates the generation of nek input files and executables through a templated user file and json dictonary of parameters by:
  1. Populating template.box, template.rea, and template.SIZE with contents of user-specified dictionary
  2. Populating user specified .usr file with contents of user-specified dictionary
  3. Calling genbox to generate an `.rea`,`.re2` input pair
  4. Calling genmap to generate a `.map` file
  5. Calling makenek to produce an executable

genrun.py also supports building [NekBox](http://github.com/maxhutch/Nek) using a similar workflow:
  1. Populates `template.rea` and `template.size_mod` with conntents of user-specififed dictionary
  2. Populating user specified `.usr` file with contents of user-specified dictionary
  3. Writes the one-line `.map` file
  4. Calls makenek to produce an executable

To start using genrun.py, copy the default.json directory and edit appropriately.  You can optionally add variables to the usr file with the pattern {NAME} and the inclusion of `"NAME" : val` in the json dictionary.

## Examples

### Basic usage
```
./genrun.py -d RTI.json -u RTI_f90.tusr Rayleigh_Taylor_run0
```

### Specify source directory
```
./genrun.py -d RTI.json -u RTI_f90.tusr -m ~/src/nek/ Rayleigh_Taylor_run1
```

### Override parameters
```
./genrun.py -d RTI.json -u RTI_f90.tusr --override={"num_steps": 128, "io_step": 16} Rayleigh_Taylor_run2
```

## Help
```
usage: genrun.py [-h] [-d CONFIG] [-u USR] [-n NP] [-m] [--makenek MAKENEK]
                 [-c] [-l] [--tdir TDIR] [--no-make] [--override OVERRIDE]
                 name

Generate NEK inputs

positional arguments:
  name                  Name to assign to generated system

optional arguments:
  -h, --help            show this help message and exit
  -d CONFIG, --dict CONFIG
                        Dictionary of parametesr (JSON)
  -u USR, --usr USR     *.usr file to use for build
  -n NP, --nproc NP     Number of processes to target
  -m, --map             Map?
  --makenek MAKENEK     Path to makenek
  -c, --clean           Clean?
  -l, --legacy          Legacy Nek5000
  --tdir TDIR           Directory to build in
  --no-make             Don't make?
  --override OVERRIDE   JSON overrides
```
