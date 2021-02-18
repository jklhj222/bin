# to reduce the ML_ORS csv data
#!/usr/bin/env python3

import pandas as pd
import os

output_prefix = 'phase2_'

# image data dirs
imgs_dir1 = '/mnt/sda1/work/ML_ORS/after_20201015/ORS_20201124_FabTest/all_images'
imgs_dir2 = '/mnt/sda1/work/ML_ORS_all_images_till20210208/all' 

# csv files there are combined into one file with header
#check_file = 'total_EQLOG_reduce.csv'
check_file = 'phase2_EQLOG.csv'
#check_file = 'test.csv'

# columns to be check (usually Image_ART, Image_ARR, ..)
check_art_col = 'AI_Image_ART'
check_arr_col = 'AI_Image_ARR'

# items to reserve in ORS judge column
ors_judge_col = 'Re_ORS_Judge'
judge_reserve_items = ['G', 'P', 'I']

# number of column which have to be read, integer or 'all'
check_ncol = 'all' 

imgs_1 = os.listdir(imgs_dir1)
imgs_2 = os.listdir(imgs_dir2)

imgs_total = imgs_1 + imgs_2
#print(len(imgs_total))

#df = pd.read_csv(check_file, error_bad_lines=False)
if check_ncol == 'all':
    df = pd.read_csv(check_file)

else:
    df = pd.read_csv(check_file, usecols=[col for col in range(check_ncol)])

# drop the rows that 'check_col' with NaN and duplicated images 
df.dropna(subset=[check_art_col, check_arr_col], inplace=True)
print('df_dropna: ', df)
df.drop_duplicates(subset=[check_art_col, check_arr_col], keep='first', inplace=True)
print('df_dropdup: ', df)
df = df[ df[ors_judge_col].isin(judge_reserve_items) ]
print('df_dropnotGPI: ', df)

# reset the index in data frame
df.reset_index(drop=True, inplace=True)

#check_df = df[[check_col]]
check_df = df[[check_art_col, check_arr_col]]
#print(check_df)

i=0
noimg_idx_list = []
yesimg_idx_list = []
for idx, col in enumerate(check_df[check_art_col]):
#    print(idx, col, type(col))
    print(f'{idx}/{len(df)}   {col}   {type(col)}')

    if col in imgs_total: 
        print('OK') 
        i += 1
 
        yesimg_idx_list.append(idx)

    else:
        noimg_idx_list.append(idx)

    print(f'i = {i}')
#    print('idx_list: ', del_idx_list)

print('len(yesimg_idx_list):', len(yesimg_idx_list))
print('len(noimg_idx_list):', len(noimg_idx_list))
#df.drop(del_idx_list, inplace=True)

if len(yesimg_idx_list) > 0:
    df_yesimg = df.drop(noimg_idx_list)
    df_yesimg.to_csv(output_prefix + 'yesimg.csv', index=False, header=False)

if len(noimg_idx_list) > 0:
    df_noimg = df.drop(yesimg_idx_list, axis=0)
    df_noimg.to_csv(output_prefix + 'noimg.csv', index=False, header=False)

