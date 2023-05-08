import warnings

warnings.filterwarnings("ignore")

import numpy as np
import os
import random
import torch

from sklearn.utils import shuffle
from torch.utils.data import Dataset
from torchvision.transforms import Resize
from tqdm import tqdm

'''
    Датасет, вытаскиваем по КТ снимки. Читаем по одному
    Назначаем его текущим и проходимся по всему в рандомном порядке
    Как закончится, берем другой
'''


# TODO:: везде назначить seed

class LungDataset(Dataset):

    def __init__(self, path_dir, transform=None, seed=42):
        # self.COUNT_BAD = 5
        # self.COUNT_GOOD = 1

        self.scans_dir = os.path.join(path_dir, 'scans')
        self.masks_dir = os.path.join(path_dir, 'masks')
        self.img_size = 256
        good_lung_names, bad_lung_names = self.get_good_lung()
        bad_lung_names = bad_lung_names[0:50]
        good_lung_names = good_lung_names[0:10]
        self.paths = good_lung_names + bad_lung_names
        # self.paths = bad_lung_names # TODO: for debug
        random.shuffle(self.paths)

        self.transform = transform
        self.cur_ind = -1
        self.cur_data = ()
        self.size = self.get_count_all_slice()
        self.seed = seed

    def get_good_lung(self):
        paths = os.listdir(self.scans_dir)
        good_lung = []
        bad_lung = []


        for name_file in paths:
            # if len(good_lung) > self.COUNT_GOOD and len(bad_lung) > self.COUNT_BAD:
            #     break

            mask_path = os.path.join(self.masks_dir, name_file)
            if os.path.isfile(mask_path):
                    # and len(bad_lung) < self.COUNT_BAD:
                bad_lung.append(name_file)
                continue

            # # TODO: debug
            # if not os.path.isfile(mask_path) and len(good_lung) < self.COUNT_GOOD:
            #     good_lung.append(name_file)

        return good_lung, bad_lung

    def get_data(self, scan_name):
        path_scan = os.path.join(self.scans_dir, scan_name)
        path_mask = os.path.join(self.masks_dir, scan_name)

        ct = np.load(path_scan)  # 512 512 N
        ct = np.transpose(ct, (2, 0, 1))  # N 512 512

        if os.path.isfile(path_mask):
            mask = np.load(path_mask)
            mask = np.transpose(mask, (2, 0, 1))
            mask = mask.astype(np.uint8)
            return ct, mask

        mask = np.zeros_like(ct)
        mask = mask.astype(np.uint8)
        ct, masks = shuffle(ct, mask, random_state=self.seed)
        self.cur_ind = 0
        self.cur_data = (ct, mask)

        return ct, mask

    def get_count_all_slice(self):
        print('Calculate size...')
        size = 0

        for scan_name in tqdm(self.paths):
            path_scan = os.path.join(self.scans_dir, scan_name)
            ct = np.load(path_scan)
            count_slice = ct.shape[2]
            size += count_slice

        return size

    def __len__(self):
        return self.size

    def __getitem__(self, ind):

        if self.cur_ind == -1:
            # ind_path = ind % self.size
            ind_path = ind % len(self.paths)
            path = self.paths[ind_path]
            scan, mask = self.get_data(path)
        else:
            scan, mask = self.cur_data

        scan = scan[self.cur_ind]
        mask = mask[self.cur_ind]

        scan = scan - np.mean(scan) / np.std(scan) # normalize

        scan = torch.tensor(scan)
        mask = torch.tensor(mask).double()


        scan = torch.unsqueeze(scan, 0)
        mask = torch.unsqueeze(mask, 0)

        # scan = Image.fromarray(scan, 'L')
        # mask = Image.fromarray(mask.astype('uint8'), 'L')

        scan = Resize(self.img_size)(scan)
        mask = Resize(self.img_size)(mask)

        if self.transform is not None:
            scan = self.transform(scan)
            mask = self.transform(mask)

        scan = scan.float()
        mask = mask.float()
        return scan, mask
