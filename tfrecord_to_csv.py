import os
from argparse import ArgumentParser

import tensorflow as tf

from utils import tfrecord_to_csv

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('--category', type=str)
    args = parser.parse_args()
    category = args.category

    data_dir = './data/yt8m_raw/'
    log = open('./parsed.txt').read().split()
    print(log)

    for fil in os.listdir(data_dir):
        print(fil)

        if fil.endswith('tfrecord') and fil.startswith(category) and fil not in log:

            with open('./parsed.txt', 'a+') as f:
                f.write(f'{fil}\n')

            dataset = tf.data.TFRecordDataset(f"{data_dir}{fil}")

            tfrecord_to_csv(dataset, category)
