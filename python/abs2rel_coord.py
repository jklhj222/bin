#!/usr/bin/env python3

import csv

with open('abs_coord.csv', 'r') as absf:
    lines = list(csv.reader(absf))
  
coords = []
for coord in lines:
   coord = list(map(int, coord))

   coords.append(coord)

rel_coords = []
with open('rel_coord.csv', 'w') as relf:
    writer = csv.writer(relf)

    for idx, line in enumerate(coords):
        if idx == 0:
            rel_coord = [coords[idx][0], coords[idx][1], coords[idx][2]]
            writer.writerow(rel_coord)
      
        else:
            rel_coord = [coords[idx][0] - coords[idx-1][0],
                         coords[idx][1] - coords[idx-1][1],
                         coords[idx][2] - coords[idx-1][2]]

            writer.writerow(rel_coord)

        rel_coords.append(rel_coord)

with open('AbsRel_coord.csv', 'w') as totalf:
    writer = csv.writer(totalf)

    for Abs, Rel in zip(coords, rel_coords):
        writer.writerow(Abs + Rel)



