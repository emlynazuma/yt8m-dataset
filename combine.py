import os

import nltk
import pandas as pd

from utils import combine_text, convert_label, preprocess_text

video_dir = './parsed'
names = ['id', 'yt_id', 'label', 'texts']
res = []

for floder in os.listdir(video_dir):
    for fil in os.listdir(os.path.join(video_dir, floder)):
        path = os.path.join(video_dir, floder, fil)

        df = pd.read_csv(path, names=names)
        res.append(df[df['texts'].notnull()])
        print(floder, fil)

final = pd.concat(res, axis=0, ignore_index=True)

final['label_converted'] = final['label'].apply(convert_label)
final['texts_converted'] = final['texts'].apply(combine_text)
final['texts_converted'] = final['texts_converted'].apply(preprocess_text)

final.to_csv('./preprocessed_data.csv', index=False, header=False, chunksize=5000)
print('total', final.head())
