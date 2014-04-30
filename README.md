nek-tools
=========

Mirror of tools directory for nek5000

# genrun.py

genrun.py automates the generation of nek input files and executables through a template user file and json dictonary of parameters by:
  1. Populating template.box, template.rea, and template.SIZE with contents of user-specified dictionary
  2. Populating user specified .usr file with contents of user-specified dictionary
  3. Calling genbox to generate an .rea/.re2 input pair
  4. Calling genmap to generate a .map file
  5. Calling makenek to produce an executable.

To start using genrun.py, copy the default.json directory and edit appropriately.  You can optionally add variables to the usr file with the pattern {NAME} and the inclusion of `"NAME" : val` in the json dictionary.  Be sure to execute genrun from the directory with the templates and have genbox, genmap, and makenek in your PATH.

```
usage: genrun.py [-h] [-d CONFIG] [-u USR] [-n NP] name

Generate NEK inputs

positional arguments:
  name                  Name to assign to generated system

optional arguments:
  -h, --help            show this help message and exit
  -d CONFIG, --dict CONFIG
                        Dictionary of parametesr (JSON)
  -u USR, --usr USR     *.usr file to use for build
  -n NP, --nproc NP     Number of processes to target
```
