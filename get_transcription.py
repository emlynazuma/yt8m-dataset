import os
from argparse import ArgumentParser

import pandas as pd

from dataset import get_yt_text

names = ['id', 'yt_id', 'labels']
video_dir = './data'


def parsed(to_be_parse, names):
    chunksize = 10
    target_path = to_be_parse.split('/')
    target_path[1] = 'parsed'
    target_path = '/'.join(target_path) + '.csv'

    # df_parsed = pd.read_csv(target_path)
    # parsed_id = df_parsed['id'].to_list()
    # print('parsed', parsed_id)

    for df in pd.read_csv(to_be_parse, names=names, chunksize=chunksize):
        df['text'] = df['yt_id'].apply(lambda x: get_yt_text(x))
        df.to_csv(target_path, mode='a', header=False, index=False)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('--category', type=str)
    args = parser.parse_args()
    category = args.category

    log = open('./parsed_transcribed.txt').read().split()

    for floder in os.listdir(video_dir):
        if floder != category:
            print(f'skip {floder}')
            continue
        for fil in os.listdir(os.path.join(video_dir, floder)):
            print(fil)
            if fil not in log:
                with open('./parsed_transcribed.txt', 'a+') as f:
                    f.write(f'{fil}\n')
                path = os.path.join(video_dir, floder, fil)
                parsed(path, names=names)
