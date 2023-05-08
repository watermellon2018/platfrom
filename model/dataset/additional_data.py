import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import shutil
import yaml

from glob import glob
from tqdm import tqdm

from calc_stat import stat_nodes


# Пройтись по здоровым КТ, которые еще не трогали, и добавить индексы от них
# 1. Индексы возьмем из середины с разбросом
# 2. Либо вычислим в какой процентной части чаще всего находятся узла и возьмем эти индексы

# 2 вариант мне нравится

def find_good_lung_not_used(root_dir, path_used_lung, mode, path_txt_file):

    file = open(path_txt_file, "a")

    used_lung_df = pd.read_csv(path_used_lung)

    scan_dir = os.path.join(root_dir, 'scans')
    mask_dir = os.path.join(root_dir, 'masks')
    names_scan = os.listdir(scan_dir)

    for name in names_scan:
        path_mask = os.path.join(mask_dir, name)
        if os.path.isfile(path_mask):
            continue

        path_scan = os.path.join(scan_dir, name)
        is_used = len(used_lung_df[used_lung_df['path'] == path_scan]) > 0

        if is_used:
            continue

        file.write(path_scan)
        file.write('\n')

    file.close()


def add_new_data(mode, count_need_data, path_save):
    if count_need_data <= 0:
        return

    top_k = stat_nodes() # [45, 78, 96 ... ] eps=2

    path_txt_file = os.path.join('../data', '{}/{}_good_data_not_used.txt'.format(mode, mode))

    eps = 2

    df = {} # path: indexs

    count_added = 0
    is_stop = False

    for ind in tqdm(top_k):
        with open(path_txt_file, 'r') as f:
            for line in f:
                path_scan = line.rstrip()

                scan = np.load(path_scan)
                scan = np.transpose(scan, (2, 0, 1))
                count_slice = len(scan)

                if count_slice < ind - eps:
                    continue

                max_ind = ind + eps
                if count_slice < max_ind:
                    max_ind = count_slice

                min_ind = ind - eps

                if path_scan not in df.keys():
                    df[path_scan] = [i for i in range(min_ind, max_ind)]
                else:
                    for i in range(min_ind, max_ind):
                        df[path_scan].append(i)

                count_added += (max_ind - min_ind)

                if count_need_data < count_added:
                    is_stop = True
                    break

                eps2 = 50
                if count_need_data < count_added + eps2:
                    is_stop = True
                    break

        if is_stop:
            break


    # df : path_scan: [45, 45, 8, ...]

    for key, value in df.items():
        df[key] = list(set(value)) # unique indexs

    df = pd.DataFrame(df.items(), columns=['path', 'indexs'])
    df.to_csv(path_save, index=False)

    return count_added



def run_find_not_used():
    modes = ['train', 'val', 'test']

    for mode in modes:

        path = os.path.join('../data', '{}/{}_good_data_not_used.txt'.format(mode, mode))

        if os.path.isfile(path):
            os.remove(path)

        root_dir = '../../data/converted/{}'.format(mode)
        path_used_lung = os.path.join('../data', '{}/{}_good_data.csv'.format(mode, mode))
        find_good_lung_not_used(root_dir, path_used_lung, mode, path)

def calc_all_data(mode):
    path_good_data = os.path.join('../data', '{}/{}_good_data.csv'.format(mode, mode))
    path_bad_data = os.path.join('../data', '{}/{}_data.csv'.format(mode, mode))

    good_df = pd.read_csv(path_good_data)
    bad_df = pd.read_csv(path_bad_data)

    bad_df['indexs'] = bad_df['indexs'].apply(lambda lst: list(map(int, lst[1:-1].split(','))))
    good_df['indexs'] = good_df['indexs'].apply(lambda lst: list(map(int, lst[1:-1].split(','))))

    bad_count = pd.Series([x for lst in bad_df['indexs'] for x in lst]).count()
    good_count = pd.Series([x for lst in good_df['indexs'] for x in lst]).count()

    return good_count, bad_count



if __name__ == '__main__':

    # run_find_not_used()

    modes = ['train', 'val', 'test']

    for mode in modes:
        path = os.path.join('../data', '{}/{}_additional_data.csv'.format(mode, mode))

        if os.path.isfile(path):
            os.remove(path)

        good_count, bad_count = calc_all_data(mode)
        print('Mode: {}. Bad = {}; Good = {}'.format(mode, bad_count, good_count))
        count_need_data = bad_count - good_count

        count_added = add_new_data(mode, count_need_data, path)
        print('Mode: {}. Bad = {}; Good = {}'.format(mode, bad_count, good_count + count_added))
