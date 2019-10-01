#!/usr/bin/env python3

import pandas as pd
from itertools import product

# The file to read
in_file = 'Chinup_data_collection_plan_forFomat.xlsx'
out_file = 'OUI_script.txt'

#all_offset = {'f':(1.1, 2.2, 3.3), 
#              'r':(4, 5, 6), 
#              'l':(7.7, 8.8, 9.9), 
#              'b':(10, 11, 12), 
#              't':(13.3, 14.4, 15.5)}

df = pd.read_excel(in_file, 
                   skiprows=0, sheet_name=None, header=0, dtype=str)

xls = pd.ExcelFile(in_file)

sheets = [df.get(sheet) for sheet in xls.sheet_names]

df_total = pd.concat(sheets, ignore_index=True)

df_total.to_csv('result_df.csv', index = False)


num_index = len(df_total['Index'])
print('num_index: ', num_index)

lines = []

def write_step(lines, step, acttype, act, f_coord, t_coord,
               side, Y1, theta, expos, gain, whitebalance, filename):
    lines.append('[Step{}]\n'.format(step))
    lines.append('ActionType={}\n'.format(acttype))
    lines.append('action={}\n'.format(act))
    lines.append('F_X={}\n'.format(f_coord[0]))
    lines.append('F_Y={}\n'.format(f_coord[1]))
    lines.append('F_Z={}\n'.format(f_coord[2]))
    lines.append('T_X={}\n'.format(t_coord[0]))
    lines.append('T_Y={}\n'.format(t_coord[1]))
    lines.append('T_Z={}\n'.format(t_coord[2]))
#    lines.append('Offset=offset{}\n'.format(offset))
    lines.append('Y1={}\n'.format(Y1))
    lines.append('Theta={}\n'.format(theta))
    lines.append('Exposure={}\n'.format(expos))
    lines.append('Gain={}\n'.format(gain))
    lines.append('WhiteBalance={}\n'.format(whitebalance))
    lines.append('Filename={}\n'.format(filename))
    lines.append('\n')

step = 1
mv_step = 0
shot_step = 0
rotate_step = 0
old_theta = '0'
for i, Idx in enumerate(df_total['Index']):
    Xs = list(map(lambda x: x.strip(), df_total.iloc[i]['X'].split(',') ))
    Ys = list(map(lambda y: y.strip(), df_total.iloc[i]['Y'].split(',') ))
    Zs = list(map(lambda z: z.strip(), df_total.iloc[i]['Z'].split(',') ))
    Expos = df_total.iloc[i]['Exposure'].replace(' ', '')
    Side = df_total.iloc[i]['Side'].replace(' ', '') 
    Y1 = df_total.iloc[i]['Y1'].replace(' ', '')
    Theta = df_total.iloc[i]['Theta'].replace(' ', '')
    Gain = df_total.iloc[i]['Gain'].replace(' ', '')
    WhiteBalance = df_total.iloc[i]['WhiteBalance'].replace(' ', '')

    # Rotate
    if Theta != old_theta:
        acttype = 1
        act = 8
        Filename = 'None'
 
        write_step(lines, step, acttype, act, (0, 0, 0), (0, 0, 0), Side,
                   Y1, Theta, Expos, Gain, WhiteBalance, Filename)

        step += 1
        rotate_step += 1

    coords = [Xs, Ys, Zs]
    coords.sort(key=len, reverse=True)

    Xs_idx = coords.index(Xs)
    Ys_idx = coords.index(Ys)
    Zs_idx = coords.index(Zs)

    for outer, mid in product(coords[2], coords[1]):
        for inner in coords[0]:
            loop_list = [inner, mid, outer]

            X = loop_list[Xs_idx]
            Y = loop_list[Ys_idx]
            Z = loop_list[Zs_idx]

            # Translate
            acttype = 1
            act = 2 if df_total.iloc[i]['Side'] == 't' else 1
            Filename = 'None'

            write_step(lines, step, acttype, act, (X, Y, Z), (X, Y, Z),
                       Side, Y1, Theta, Expos, Gain, WhiteBalance, Filename)

            step += 1
            mv_step += 1

            # Shot
            acttype = 3 if df_total.iloc[i]['Side'] == 't' else 2
            act = 32 if df_total.iloc[i]['Side'] == 't' else 16
            Filename = '{}side_{}X_{}Y_{}Z'.format(Side.upper(), X, Y, Z)

            write_step(lines, step, acttype, act, (X, Y, Z), (X, Y, Z),
                       Side, Y1, Theta, Expos, Gain, WhiteBalance, Filename)

            coords[0] = coords[0][::-1]

            step += 1
            shot_step += 1
          
    old_theta = Theta

# write to file
lines.insert(0, '[StepDate]\n')
lines.insert(1, 'AllStep={}\n'.format(step-1))
#idx = 2
#for ofs in ('f', 'r', 'l', 'b', 't'):
#    string = 'offset' + ofs
#    lines.insert(idx, '{}={},{},{}\n'.format(string,
#                                             all_offset[ofs][0],
#                                             all_offset[ofs][1],
#                                             all_offset[ofs][2]))
#    idx += 1

lines.insert(2, '\n')
lines.pop()

with open(out_file, 'w') as f:
    for line in lines:
        f.write(line)

print()
print('{:>17s}{}'.format('total steps: ', step-1))
print('{:>17s}{}'.format('translate steps: ', mv_step))
print('{:>17s}{}'.format('rotate steps: ', rotate_step))
print('{:>17s}{}'.format('shot steps: ', shot_step))
print()
print('input file: ', in_file)
print('output file:', out_file)

