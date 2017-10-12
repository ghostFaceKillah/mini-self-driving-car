import cv2
import ipdb
import numpy as np
import os
import pandas as pd
import tqdm
import matplotlib.image as mpimg
import seaborn as sns
import matplotlib.pyplot as plt


import lib.constant as cnst
import ml.img_augmentation as aug
import ml.data_utils as data_utils
import ml.model_utils as model_utils
import ml.utils as misc_utils



CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(CURRENT_DIR, '../datasets/turn_right')
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
        new_df.to_csv(datapath())

    return new_df

def datapath():
    return os.path.join(CURRENT_DIR, 'some_data.csv')


def make_last_layer_correlation_visualization():
    new_df = record_data_ordering_by_final_output()
    sns.heatmap(new_df.corr(), fmt=".0%", annot=True, cmap='coolwarm')


def visualize_pictures():
    no_imgs = 60
    imgs_in_row = 8

    df = pd.read_csv(datapath())
    df.loc[:, 'steering'] = -df.left + df.right
    imgs_by_steering = df.sort_values('steering')[['img_name', 'steering']]
    step = int(len(df) / no_imgs)

    images = []

    # every step-th row in imgs_by_steering
    iterable = [i for i in imgs_by_steering.itertuples()][::step]


    for data in iterable:
        img_fname_short, steering = data.img_name, data.steering

        img_fname = os.path.join(IMG_DIR, img_fname_short)
        # img = mpimg.imread(img_fname)
        img = data_utils.load_process_image(img_fname)[:, :, 0]

        # out_img = cv2.putText(
        #     img,
        #     "{:.0%}".format(steering),
        #     (10, 40),                 # origin
        #     cv2.FONT_HERSHEY_SIMPLEX, # font
        #     1.0,                      # font scale
        #     (255, 255, 255),              # color
        #     2,                        # thickness
        #     cv2.LINE_AA               # Line type
        # )
        # images.append(out_img)

        images.append(img)

    grouped_images = list(misc_utils.group(images, imgs_in_row))
    big_img = np.vstack([
        np.hstack(grp)
        for grp in grouped_images
    ])

    plt.figure(figsize=(30, 30))
    plt.imshow(big_img, cmap='gray', interpolation='none')
    plt.savefig(os.path.join(CURRENT_DIR, 'preprocessed_images_by_predicted_direction.png'))
    plt.close()

    print("Done")


if __name__ == '__main__':
    visualize_pictures()

