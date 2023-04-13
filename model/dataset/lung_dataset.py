import cv2
import numpy as np
import os

from sklearn.utils import shuffle
from torch.utils.data import Dataset
from tqdm import tqdm

class LungDataset(Dataset):

    def __init__(self, path_dir, transform=None):
        self.scans_dir = os.path.join(path_dir, 'scans')
        self.masks_dir = os.path.join(path_dir, 'masks')
        self.img_size = 256

        self.scans, self.masks = self.get_data()

        print(self.scans.shape, self.masks.shape)

        self.transform = transform

    def get_good_lung(self):
        paths = os.listdir(self.scans_dir)
        good_lung = []
        bad_lung = []

        for name_file in paths:
            mask_path = os.path.join(self.masks_dir, name_file)
            if os.path.isfile(mask_path):
                bad_lung.append(name_file)
                continue

            good_lung.append(name_file)

        # TODO:: fix
        good_lung = good_lung[0:1]
        bad_lung = bad_lung[0:1]

        return good_lung, bad_lung

    def form_tensor_ct(self, arr_names, is_good=False):
        cts = np.empty((0, self.img_size, self.img_size))
        masks = np.empty((0, self.img_size, self.img_size), dtype=np.uint8)

        for name in tqdm(arr_names):
            path_scan = os.path.join(self.scans_dir, name)
            path_mask = os.path.join(self.masks_dir, name)

            ct = np.load(path_scan)
            ct = np.transpose(ct, (2, 0, 1))

            ct_resized = np.zeros((ct.shape[0], self.img_size, self.img_size))

            for i in range(ct.shape[0]):
                resized_img = cv2.resize(ct[i], (self.img_size, self.img_size))
                ct_resized[i] = resized_img

            slice_cts = cts.shape[0]
            new_shape = slice_cts + ct_resized.shape[0]
            cts.resize(new_shape, self.img_size, self.img_size)
            cts[slice_cts:, :, :] = ct_resized

            if not is_good:
                mask = np.load(path_mask)
                mask = mask.astype(np.uint8)
                mask = np.transpose(mask, (2, 0, 1))

                mask_resized = np.zeros((mask.shape[0], self.img_size, self.img_size))

                for i in range(mask.shape[0]):
                    resized_img = cv2.resize(mask[i], (self.img_size, self.img_size))
                    mask_resized[i] = resized_img

                slice_mask = masks.shape[0]
                new_shape = masks.shape[0] + mask_resized.shape[0]
                masks.resize(new_shape, self.img_size, self.img_size)
                masks[slice_mask:, :, :] = mask_resized


        if is_good:
            masks = np.zeros_like(cts)
            masks = masks.astype(np.uint8)

        return cts, masks

    def get_data(self):
        good_lung_names, bad_lung_names = self.get_good_lung()

        healthy_scans, healthy_masks = self.form_tensor_ct(good_lung_names, True)
        bad_scans, bad_masks = self.form_tensor_ct(bad_lung_names)

        scans = np.concatenate((bad_scans, healthy_scans), axis=0)
        masks = np.concatenate((bad_masks, healthy_masks), axis=0)

        scans, masks = shuffle(scans, masks, random_state=42)

        return scans, masks

    def __len__(self):
        return len(self.scans)

    def __getitem__(self, ind):
        scan = self.scans[ind]
        mask = self.masks[ind]

        scan_min = np.min(scan)
        scan_max = np.max(scan)
        scan = scan - np.mean(scan) / np.std(scan)
        # scan = ((scan - scan_min) / (scan_max - scan_min))

        # scan = Image.fromarray(scan, 'L')
        # mask = Image.fromarray(mask.astype('uint8'), 'L')

        if self.transform is not None:
            scan = self.transform(scan)
            mask = self.transform(mask)

        return scan, mask



if __name__ == '__main__':
    import yaml

    with open('../config/standard.yaml') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    train_path = config['train']

    train_ds = LungDataset(train_path)
    x, y = next(iter(train_ds))

'''
    Либо сделать датасет, вытаскиваем по КТ снимки. Читаем по одному
    Назначаем его текущим и проходимся по всему в рандомном порядке
    Как закончится, берем другой
'''