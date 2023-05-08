import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import shutil
import yaml

from glob import glob
from tqdm import tqdm


def write_data(path_dir, save_file_path):
    masks_dir = os.path.join(path_dir, 'masks')
    paths = glob(os.path.join('..', masks_dir, '*.npy'))

    file = open(save_file_path, "a")

    for path_mask in tqdm(paths):
        mask = np.load(path_mask)
        mask = np.transpose(mask, (2, 0, 1))
        inds = []

        for ind_slice, slice_ct in enumerate(mask):
            is_bad = (slice_ct > 0).sum() > 0
            if is_bad:
                inds.append(ind_slice)

        file.write(path_mask)
        file.write(' ')
        file.write(str(inds))
        file.write('\n')

    file.close()


def txt_to_csv(path_txt, mode):
    df = {'path': [], 'indexs': []}
    with open(path_txt, 'r') as f:
        for line in f:
            line = line.rstrip()
            path, inds_str = line.split(' [')
            inds = list(map(int, inds_str[:-2].split(', ')))

            df['path'].append(path)
            df['indexs'].append(inds)

    df = pd.DataFrame(df)
    path_csv = os.path.join('../data', '{}/{}_data.csv'.format(mode, mode))
    df.to_csv(path_csv, index=False)


def collect_info(config, mode):
    path = config[mode]
    path_txt_file = os.path.join('../data', '{}/{}_data.txt'.format(mode, mode))
    write_data(path, path_txt_file)

    txt_to_csv(path_txt_file, mode)


if __name__ == '__main__':
    with open('../config/standard.yaml') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    modes = ['train', 'val', 'test']



    for mode in modes:
        path = '../data/{}'.format(mode)
        shutil.rmtree(path)
        os.makedirs(path, exist_ok=True)
        collect_info(config, mode)
