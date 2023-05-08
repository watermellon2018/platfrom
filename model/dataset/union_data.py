import pandas as pd


'''
    Mode: train. Bad = 10778; Good = 11035 -> Good = 10778
    Mode: val. Bad = 1467; Good = 1411
    Mode: test. Bad = 1534; Good = 1478
'''
def union(mode):
    path_additional = '../data/{}/{}_additional_data.csv'.format(mode, mode)
    path_good = '../data/{}/{}_good_data.csv'.format(mode, mode)
    path_bad = '../data/{}/{}_data.csv'.format(mode, mode)

    add_df = pd.read_csv(path_additional)
    add_df = add_df[:-5]
    good_df = pd.read_csv(path_good)
    bad_df = pd.read_csv(path_bad)

    print('Bad: {}; Good: {}'.format(len(bad_df), len(add_df)+len(good_df)))

    good_data = add_df.append(good_df)
    good_data = good_data[0:10778]
    df = good_data.append(bad_df)

    print(df.shape)
    df = df.sample(frac=1)

    df.to_csv('../data/{}/data.csv'.format(mode), index=False)


if __name__ == '__main__':
    modes = ['train', 'val', 'test']

    for mode in modes:
        union(mode)