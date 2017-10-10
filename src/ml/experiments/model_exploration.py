import numpy as np
import os
import pandas as pd
import tqdm
import matplotlib.image as mpimg
import seaborn as sns


import lib.constant as cnst
import ml.img_augmentation as aug
import ml.data_utils as data_utils
import ml.model_utils as model_utils
import ml.utils as misc_utils



# CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# DATA_DIR = os.path.join(CURRENT_DIR, '../datasets/turn_right')
DATA_DIR = '../datasets/turn_right'
LOG_FNAME = os.path.join(DATA_DIR, 'log.csv')
IMG_DIR = os.path.join(DATA_DIR, 'img')

BATCH_SIZE = 128


def load_data():
    # preload data
    df = pd.read_csv(LOG_FNAME)[['short_fname']]
    imgs = data_utils.preload_preprocessed_images(df, IMG_DIR)

    return df, imgs


def record_data_ordering_by_final_output(save_to_csv=False):
    df, imgs = load_data()

    model = model_utils.load_model()

    acc = []
    pre_last_layer_acc = []


    iterator = tqdm.tqdm(
        misc_utils.group(range(len(df)), BATCH_SIZE)
    )

    layer_no = -3
    proto_func = model_utils.cut_sequential_model(model, layer_no)

    pre_last_layer_func = lambda x: proto_func([x])[0]

    # TODO: resolve that the last one is not handled properly
    for index_range in iterator:
        indexer = list(index_range)
        df_part = df.iloc[indexer].short_fname

        img_batch = np.array([imgs[x] for x in df_part])

        predictions = model.predict(img_batch, BATCH_SIZE)
        pre_last_out = pre_last_layer_func(img_batch)

        acc.append(predictions)
        pre_last_layer_acc.append(pre_last_out)

    outs = np.vstack(acc)
    pre_last_layer_outs = np.vstack(pre_last_layer_acc)

    # left, right, nothing
    left_prob = outs[:, 0]
    right_prob = outs[:, 1]
    nothing_prob = outs[:, 2]

    pre_df = {
        'img_name': df.short_fname[:len(left_prob)],
        'left': left_prob,
        'right': right_prob,
        'nothing': nothing_prob
    }

    pre_df.update({
        'layer_{}_{}'.format(layer_no, i): pre_last_layer_outs[:, i]
        for i in range(pre_last_layer_outs.shape[-1])
    })

    new_df = pd.DataFrame(pre_df)

    if save_to_csv:
        new_df.to_csv('some_data.csv')

    return new_df


if __name__ == '__main__':
    new_df = record_data_ordering_by_final_output()
    sns.heatmap(new_df.corr(), fmt=".0%", annot=True, cmap='coolwarm')

    print("ww")
