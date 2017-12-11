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
import ipdb

import ml.img_augmentation as img_aug

DATASET_DIR = '/home/misiu/src/self-driving/mini-self-driving-car/datasets/turn_right'
IMG_PATH = os.path.join(DATASET_DIR, 'img')
LOG_PATH = os.path.join(DATASET_DIR, 'log.csv')


def load_img(short_im_fname):
    img_name = os.path.join(IMG_PATH, short_im_fname)
    img = cv2.imread(img_name)
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

ROW_NO = 6
COL_NO = 2


def loop_through_augmentation():
    while True:
        idx = np.random.randint(low=0, high=len(df)-1)
        short_im_fname = df.iloc[idx].loc['short_fname']
        steering = df.iloc[idx].loc['steering_horizontal']
        img = load_img(short_im_fname)
    
        fig, axs = plt.subplots(ROW_NO, COL_NO, figsize=(20, 15))
        plt.suptitle("{} {}".format(idx, steering))
        axs[0][0].imshow(img)
    
        for plot_i in range(1, ROW_NO * COL_NO):
            new_img = img.copy()
            for f in transforms:
                new_img, _ = f(new_img, np.array([0, 0, 0]))
    
            # axs[int(plot_i / 6)][plot_i % 6].imshow(new_img)
            axs[int(plot_i / ROW_NO)][plot_i % COL_NO].imshow(new_img, cmap='gray')
    
        plt.show()
        # plt.savefig('test.jpg')
        # plt.close()


def show_training_examples():
    ROW_NO = 4
    COL_NO = 2

    idx = np.random.randint(low=0, high=len(df)-1)
    short_im_fname = df.iloc[idx].loc['short_fname']
    steering = df.iloc[idx].loc['steering_horizontal']
    img = load_img(short_im_fname)

    fig, axs = plt.subplots(ROW_NO, COL_NO, figsize=(5, 9))

    axs[0][0].imshow(img)
    axs[0][0].set_title(steering)

    for plot_i in range(1, ROW_NO * COL_NO):
        idx = np.random.randint(low=0, high=len(df)-1)
        short_im_fname = df.iloc[idx].loc['short_fname']
        steering = df.iloc[idx].loc['steering_horizontal']
        img = load_img(short_im_fname)

        axs[int(plot_i / COL_NO)][plot_i % COL_NO].imshow(img)
        axs[int(plot_i / COL_NO)][plot_i % COL_NO].set_title(steering)

    plt.savefig('training_data.jpg')
    plt.close()
    

def show_example_augmentation():
    idx = np.random.randint(low=0, high=len(df)-1)
    short_im_fname = df.iloc[idx].loc['short_fname']
    steering = df.iloc[idx].loc['steering_horizontal']
    img = load_img(short_im_fname)

    fig, axs = plt.subplots(ROW_NO, COL_NO, figsize=(5.4, 8))
    plt.suptitle("{} {}".format(idx, steering))
    axs[0][0].imshow(img)

    for plot_i in range(1, ROW_NO * COL_NO):
        new_img = img.copy()
        for f in transforms:
            new_img, _ = f(new_img, np.array([0, 0, 0]))

        # axs[int(plot_i / 6)][plot_i % 6].imshow(new_img)
        axs[int(plot_i / COL_NO)][plot_i % COL_NO].imshow(new_img, cmap='gray')

    plt.savefig('image_augmentation.jpg')
    plt.close()



if __name__ == '__main__':
    # show_example_augmentation()
    show_training_examples()
