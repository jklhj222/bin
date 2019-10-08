#!/usr/bin/env python3

import pandas as pd
from itertools import product

# The file to read
in_file = 'Chinup_data_collection_plan_forScratch_v5_Interval15mm_new2.xlsx'
out_file = 'OUI_script_v5_Scratch_Interval15mm_new2.txt'

#all_offset = {'f':(1.1, 2.2, 3.3), 
#              'r':(4, 5, 6), 
#              'l':(7.7, 8.8, 9.9), 
#              'b':(10, 11, 12), 
#              't':(13.3, 14.4, 15.5)}

xls = pd.ExcelFile(in_file)

df = pd.read_excel(in_file, 
                   skiprows=0, sheet_name=None, header=0, dtype=str)

data_sheet_names = list(filter(lambda x: x!='CCD1_code_table' and
                                         x!='CCD2_code_table', 
                               xls.sheet_names))

data_sheets = [df.get(sheet) for sheet in data_sheet_names]

df_total = pd.concat(data_sheets, ignore_index=True, sort=False)

df_ccd1 = pd.read_excel(in_file, skiprows=0,
                        sheet_name='CCD1_code_table', header=0, dtype=str)

df_ccd2 = pd.read_excel(in_file, skiprows=0,
                        sheet_name='CCD2_code_table', header=0, dtype=str)

df_total.to_csv('result_df.csv', index = False)


num_index = len(df_total['Index'])
print('num_index: ', num_index)

lines = []

def get_Pnumber(ccd_df, expos, gain, illu):
    expos_condition = ccd_df.Exposure==expos
    df_tmp = ccd_df[expos_condition]

    gain_condition = df_tmp.Gain==gain
    df_tmp = df_tmp[gain_condition]

    illu_condition = df_tmp.Illumination==illu
    df_tmp = df_tmp[illu_condition]

    P_number = df_tmp.iloc[0]['Code']

    return P_number

def write_step(lines, step, acttype, act, f_coord, t_coord,
               Y1, theta, p_number,  filename):
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
#    lines.append('Exposure={}\n'.format(expos))
#    lines.append('Gain={}\n'.format(gain))
#    lines.append('WhiteBalance={}\n'.format(whitebalance))
    lines.append('P_Number={}\n'.format(p_number))
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
    Exposes = df_total.iloc[i]['Exposure'].replace(' ', '').split(',')
    Side = df_total.iloc[i]['Side'].replace(' ', '') 
    Y1 = df_total.iloc[i]['Y1'].replace(' ', '')
    Theta = df_total.iloc[i]['Theta'].replace(' ', '')
    Gain = df_total.iloc[i]['Gain'].replace(' ', '')
#    WhiteBalance = df_total.iloc[i]['WhiteBalance'].replace(' ', '')
    Illu = df_total.iloc[i]['Illumination'].replace(' ', '')

    # Rotate
    if Theta != old_theta:
        acttype = 1
        act = 8
        P_number = 'None'
        Filename = 'None'
 
        write_step(lines, step, acttype, act, (0, 0, 0), (0, 0, 0), 
                   Y1, Theta, P_number, Filename)

        step += 1
        rotate_step += 1

    coords = [Xs, Ys, Zs]
    coords.sort(key=len, reverse=True)

    Xs_idx = coords.index(Xs)
    Ys_idx = coords.index(Ys)
    Zs_idx = coords.index(Zs)

    mv_idx = 0
    for outer, mid in product(coords[2], coords[1]):
        for inner in coords[0]:
            loop_list = [inner, mid, outer]

            X = loop_list[Xs_idx]
            Y = loop_list[Ys_idx]
            Z = loop_list[Zs_idx]

            # Translate
            acttype = 1
            act = 2 if Side == 't' else 1
            f_coord = (0, 0, 0) if Side == 't' else (X, Y, Z)
            t_coord = (X, Y, Z) if Side == 't' else (0, 0, 0)
            P_number = 'None'
            Filename = 'None'

            write_step(lines, step, acttype, act, f_coord, t_coord,
                       Y1, Theta, P_number, Filename)

            step += 1
            mv_step += 1
            mv_idx += 1

            # Shot
            acttype = 3 if Side == 't' else 2
            act = 32 if Side == 't' else 16
            ccd_df = df_ccd2 if Side == 't' else df_ccd1
            f_coord = (0, 0, 0) if Side == 't' else (X, Y, Z)
            t_coord = (X, Y, Z) if Side == 't' else (0, 0, 0)

            if '.' in X:
                X_name = X.split('.')[0] + 'd' + X.split('.')[1]
            else:
                X_name = X

            if '.' in Y:
                Y_name = Y.split('.')[0] + 'd' + Y.split('.')[1]
            else:
                Y_name = Y

            if '.' in Z:
                Z_name = Z.split('.')[0] + 'd' + Z.split('.')[1]
            else:
#                Z_name = Z + 'd'
                Z_name = Z

            Filename = '{}side_{}_{:04d}_{}X_{}Y_{}Z'.format(
                         Side.upper(), Idx, mv_idx, X_name, Y_name, Z_name)

            P_numbers = ''
            for Expos in Exposes:
                P_number = get_Pnumber(ccd_df, Expos, Gain, Illu)
                P_numbers += P_number + ','
          
            P_numbers = P_numbers.rstrip(',')   
         
            write_step(lines, step, acttype, act, f_coord, t_coord,
                       Y1, Theta, P_numbers, Filename)

            step += 1
            shot_step += 1
          
        coords[0] = coords[0][::-1]

    old_theta = Theta

# write to file
lines.insert(0, '[StepData]\n')
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

