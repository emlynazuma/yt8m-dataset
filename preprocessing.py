import os

import nltk
import pandas as pd

from utils import combine_text, convert_label, preprocess_text

data_dir = './data/yt8m_in_csv_id_cap'
names = ['id', 'label', 'yt_id', 'texts']
res = []

for floder in os.listdir(data_dir):
    for fil in os.listdir(os.path.join(data_dir, floder)):
        path = os.path.join(data_dir, floder, fil)

        df = pd.read_csv(path, names=names)
        res.append(df[df['texts'].notnull()])
        print(floder, fil)

final = pd.concat(res, axis=0, ignore_index=True)

final['label_converted'] = final['label'].apply(convert_label)
final['texts_converted'] = final['texts'].apply(combine_text)
final['texts_converted'] = final['texts_converted'].apply(preprocess_text)

final.to_csv('./clean_data.csv', index=False, header=False, chunksize=5000)
