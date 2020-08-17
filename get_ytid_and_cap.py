import os
from argparse import ArgumentParser

import pandas as pd

from utils import get_yt_text, convert_id

names = ['yt_8m_id', 'labels']
data_dir = './data/yt8m_in_csv'


def parsed(to_be_parse, names):
    chunksize = 10
    target_path = to_be_parse.split('/')
    target_path[2] = 'yt8m_in_csv_id_cap'
    target_path = '/'.join(target_path)

    for df in pd.read_csv(to_be_parse, names=names, chunksize=chunksize):
        df['yt_id'] = df['yt_8m_id'].apply(lambda x: convert_id(x))
        df['text'] = df['yt_id'].apply(lambda x: get_yt_text(x))
        df.to_csv(target_path, mode='a', header=False, index=False)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('--category', type=str)
    args = parser.parse_args()
    category = args.category

    log = open('./parsed_transcribed.txt').read().split()

    for floder in os.listdir(data_dir):
        if floder != category:
            print(f'skip {floder}')
            continue
        for fil in os.listdir(os.path.join(data_dir, floder)):
            print(fil)
            if fil not in log:
                with open('./parsed_transcribed.txt', 'a+') as f:
                    f.write(f'{fil}\n')
                path = os.path.join(data_dir, floder, fil)
                parsed(path, names=names)
