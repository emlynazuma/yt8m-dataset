import json
import os
import xml.etree.cElementTree as ET
from urllib import request as req
import pandas as pd

import requests
import tensorflow as tf
from youtube_transcript_api import YouTubeTranscriptApi, _errors


def convert(yt_8m_id):
    init = yt_8m_id[:2]
    url = f'http://data.yt8m.org/2/j/i/{init}/{yt_8m_id}.js'
    response = requests.get(url)

    if response.status_code != 200:
        return

    data = response.text
    startidx = data.find('(')
    endidx = data.rfind(')')
    y_id = data[startidx + 1:endidx].split(',')[1].replace('"', '')
    return y_id


def get_id_label(dataset, category):
    count = 0
    temp = []

    for data in dataset:
        example = tf.train.Example()
        example.ParseFromString(data.numpy())
        yt_8m_id = example.features.feature['id'].bytes_list.value[0].decode(encoding='UTF-8')
        yt_id = convert(yt_8m_id)
        labels = list(example.features.feature['labels'].int64_list.value)
        # mean_rgb = example.features.feature['mean_rgb'].float_list.value
        info = {
            "yt_8m_id": yt_8m_id,
            "yt_id": yt_id,
            "labels": labels,
            "texts": get_yt_text(yt_id)
        }
        temp.append(info)
        count += 1
        print(count)

        if len(temp) % 100 == 0:
            df = pd.DataFrame(temp)
            df.to_csv('./data.csv', mode='a', header=False, index=False)
            temp = []

    df = pd.DataFrame(temp)
    df.to_csv(f'./{category}_data.csv', mode='a', header=False, index=False)


def get_yt_text(yt_id):
    try:
        return YouTubeTranscriptApi.get_transcript(yt_id, languages=['en'])
    except Exception as e:
        with open('log.txt', 'a') as f:
            f.write(f'{str(e.__class__)}, {yt_id}\n')


if __name__ == "__main__":
    video_dir = './video/'
    log = open('./parsed.txt').read().split()
    print(log)

    for fil in os.listdir(video_dir):
        print(fil)

        if fil.endswith('tfrecord') and fil not in log:
            print('in', fil)

            with open('./parsed.txt', 'a+') as f:
                f.write(f'{fil}\n')

            dataset = tf.data.TFRecordDataset(f"{video_dir}{fil}")

            if fil.startswith('train'):
                category = 'train'
            elif fil.startswith('validate'):
                category = 'validate'
            elif fil.startswith('test'):
                category = 'test'
            else:
                category = ''

            get_id_label(dataset, category)
