#!/usr/bin/env python3

import pandas as pd

check_file = 'AIORS_1007-1012_ailog.xlsx'
train_file = 'data13_train_20201015_test.xlsx'
train_csv = 'data13_train_20201015_test.csv'

check_xls = pd.ExcelFile(check_file)
train_xls = pd.ExcelFile(train_file)

check_df = pd.read_excel(check_file, sheet_name='M1')
train_df = pd.read_excel(train_file, sheet_name='Sheet1')

check_reduce_df = check_df[['Image_ARR', 'Image_ART', 'T', 'L']]

for img_arr, t, l in zip(check_reduce_df['Image_ARR'], 
                         check_reduce_df['T'],
                         check_reduce_df['L']):

    idx = train_df[train_df['Image_ARR'] == img_arr]['ORS_Judge'].index.tolist()[0]

    if t != 0 or l != 0:
        print(train_df.loc[idx, 'ORS_Judge'])
        train_df.loc[idx, 'ORS_Judge'] = 'P'
        print(train_df.loc[idx, 'ORS_Judge'])
 
    else:
        print(train_df.loc[idx, 'ORS_Judge'])
        train_df.loc[idx, 'ORS_Judge'] = 'G'
        print(train_df.loc[idx, 'ORS_Judge'])

train_tmp_df = train_df[(train_df['ORS_Judge']=='M') | 
                        (train_df['ORS_Judge']=='N') |
                        (train_df['Image_ARR'].isna()) | 
                        (train_df['Image_ART'].isna())]       

train_df.drop(train_tmp_df.index.tolist(), inplace=True)

train_df.to_csv(train_csv, index=False, header=False)
