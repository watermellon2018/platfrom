import numpy as np
import os
import pandas as pd


def stat_nodes():
    path_train = os.path.join('../data', '{}/{}_good_data.csv'.format('train', 'train'))
    path_val = os.path.join('../data', '{}/{}_good_data.csv'.format('val', 'val'))
    path_test = os.path.join('../data', '{}/{}_good_data.csv'.format('test', 'test'))

    train_df = pd.read_csv(path_train)
    val_df = pd.read_csv(path_val)
    test_df = pd.read_csv(path_test)


    train_val_df = train_df.append(val_df, ignore_index=True)
    df = train_val_df.append(test_df, ignore_index=True)

    df['indexs'] = df['indexs'].apply(lambda lst: list(map(int, lst[1:-1].split(','))))

    value_counts = pd.Series([x for lst in df['indexs'] for x in lst]).value_counts()
    top = value_counts.nlargest(len(value_counts))

    return top.keys()
