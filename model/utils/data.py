import os
import pandas as pd

from glob import glob
from random import shuffle

from utils.seed import set_seed

''' TODO:: разбить по размера. 
    Убедиться, что в тренировочной выборке есть маленькие, 
    средние и большие узлы'''

def split(prop=(80, 10, 10)):
    set_seed()

    stat = pd.read_csv('../../data/converted/statistics.csv')

    path_dir_scans = '../data/converted/scans'
    path_dir_mask = '../data/converted/masks'

    paths = glob(os.path.join(path_dir_scans, '*.npy'))
    shuffle(paths)

    tr, v, ts = prop
    size = len(paths_dir_scans)
    train_data = paths[:tr]
