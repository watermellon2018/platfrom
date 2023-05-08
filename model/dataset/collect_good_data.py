import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import shutil
import yaml

from glob import glob
from tqdm import tqdm


def write_data(path_dir, mode):
    scans_dir = os.path.join(path_dir, 'scans')
    masks_dir = os.path.join(path_dir, 'masks')
    files = os.listdir(scans_dir)

    path_txt_file = os.path.join('../data', '{}/{}_good_data.txt'.format(mode, mode))
    file = open(path_txt_file, "a")

    path_csv_file = os.path.join('../data', '{}/{}_data.csv'.format(mode, mode))
    df = pd.read_csv(path_csv_file)
    indexs = df['indexs'].values
    cur_num_mask = 0

    for num_file, name_file in tqdm(enumerate(files)):

        mask_path = os.path.join(masks_dir, name_file)
        if os.path.isfile(mask_path):
            continue

        path_scan = os.path.join(scans_dir, name_file)
        scan = np.load(path_scan)
        scan = np.transpose(scan, (2, 0, 1))

        inds = indexs[cur_num_mask]
        inds = list(map(int, inds[1:-1].split(', ')))

        if max(inds) > len(scan):
            continue

        file.write(path_scan)
        file.write(' ')
        file.write(str(inds))
        file.write('\n')

        cur_num_mask += 1

    file.close()

    print(cur_num_mask, df.shape[0])

def txt_to_csv(mode):
    df = {'path': [], 'indexs': []}

    path_txt = os.path.join('../data', '{}/{}_good_data.txt'.format(mode, mode))

    with open(path_txt, 'r') as f:
        for line in f:
            line = line.rstrip()
            path, inds_str = line.split(' [')
            inds = list(map(int, inds_str[:-1].split(', ')))

            df['path'].append(path)
            df['indexs'].append(inds)

    df = pd.DataFrame(df)
    path_csv = os.path.join('../data', '{}/{}_good_data.csv'.format(mode, mode))
    df.to_csv(path_csv, index=False)


def collect_info(config, mode):
    path = config[mode]
    path = os.path.join('..', path) # TODO:: костыль
    write_data(path, mode)

    txt_to_csv(mode)


if __name__ == '__main__':
    with open('../config/standard.yaml') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    modes = ['train', 'val', 'test']

    for mode in modes:
        path1 = os.path.join('../data', '{}/{}_good_data.csv'.format(mode, mode))
        path2 = os.path.join('../data', '{}/{}_good_data.txt'.format(mode, mode))

        if os.path.isfile(path1):
            os.remove(path1)

        if os.path.isfile(path2):
            os.remove(path2)

        collect_info(config, mode)
