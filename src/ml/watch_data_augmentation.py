"""
Based on:
- input image
- collection of augmentation

show sample of data augmentations
"""

import cv2
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd

import ml.img_augmentation as img_aug

DATASET_DIR = 'data/turn_right'
IMG_PATH = os.path.join(DATASET_DIR, 'img')
LOG_PATH = os.path.join(DATASET_DIR, 'log.csv')


def load_img(short_im_fname):
    img = cv2.imread(os.path.join(IMG_PATH, short_im_fname))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    return img

# Load some data
df = pd.read_csv(LOG_PATH)

idx = 0



# Prepare transforms
transforms =[
    img_aug.crop,
    img_aug.to_gray,
    img_aug.contrast,
    img_aug.brightness_additive,
    # img_aug.brightness_multiplicative,
    # img_aug.hue_shift,  # hard to say if needed, maybe for different lighting?
    img_aug.random_flip,
    img_aug.random_rotation,
    img_aug.random_translation,
    # img_aug.to_centered_float
]

while True:
    idx = np.random.randint(low=0, high=len(df)-1)
    short_im_fname = df.iloc[idx].loc['short_fname']
    steering = df.iloc[idx].loc['steering_horizontal']
    img = load_img(short_im_fname)

    fig, axs = plt.subplots(8, 6, figsize=(20, 15))
    plt.suptitle("{} {}".format(idx, steering))
    axs[0][0].imshow(img)

    for plot_i in range(1, 8 * 6):
        new_img = img.copy()
        for f in transforms:
            new_img, _ = f(new_img, np.array([0, 0, 0]))

        # axs[int(plot_i / 6)][plot_i % 6].imshow(new_img)
        axs[int(plot_i / 6)][plot_i % 6].imshow(new_img, cmap='gray')

    plt.show()