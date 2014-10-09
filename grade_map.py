#!/usr/bin/env python3

from sys import argv

map_file = open(argv[1], 'r')
nproc = int(argv[2])

toks = map_file.readline().split()
nel = int(toks[0])
nblock = int((nel - 1) / nproc) + 1

gather = {}
corner_count = {}
for e in range(nel):
  toks = map_file.readline().split()
  for i in range(8):
    if int(toks[i+1]) in gather:
      gather[int(toks[i+1])].add(int(int(toks[0]) / nblock ))
      corner_count[int(toks[i+1])] += 1
    else:
      gather[int(toks[i+1])] = set([int(int(toks[0]) / nblock )])
      corner_count[int(toks[i+1])] = 1


nprocs = [0, 0, 0, 0, 0, 0, 0, 0]
for procs in gather.values():
  nprocs[len(procs) - 1] += 1

ninst = [0, 0, 0, 0, 0, 0, 0, 0]
for count in corner_count.values():
  ninst[count-1] += 1

print(sum(nprocs), nprocs) 
print(ninst)
