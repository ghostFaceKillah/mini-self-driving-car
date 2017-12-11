import os

import numpy as np
import tqdm
from matplotlib import image as mpimg

from ml import img_augmentation as aug


def preload_images(driving_log, img_dir):
    """
    If dataset is small enough, training can be made a lot
    faster via pre-loading all images into RAM.
    For starters it should be good enough.
    """
    print("Preloading images into RAM...")

    imgs_list = list(driving_log.short_fname)
    resu = {}

    for img_fname_short in tqdm.tqdm(imgs_list):
        img_fname = os.path.join(img_dir, img_fname_short)
        img = mpimg.imread(img_fname)

        resu[img_fname_short] = img

    return resu


def load_process_image(path):
    img = mpimg.imread(path)
    img, _ = aug.crop(img, None)
    img, _ = aug.to_gray(img, None)
    img, _ = aug.to_unit_interval_float(img, None)
    img = np.expand_dims(img, axis=-1)
    return img


def preload_preprocessed_images(driving_log, img_dir):
    """
    If dataset is small enough, training can be made a lot
    faster via pre-loading all images into RAM.

    Here we load and preprocess them
    """
    print("Processing & preloading images into RAM...")

    imgs_list = list(driving_log.short_fname)
    resu = {}

    for img_fname_short in tqdm.tqdm(imgs_list):
        img_fname = os.path.join(img_dir, img_fname_short)
        img = load_process_image(img_fname)

        resu[img_fname_short] = img

    return resu


