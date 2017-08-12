import cv2
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import pickle
import tqdm

from keras.callbacks import ModelCheckpoint, TensorBoard
from keras.layers import Dense, Dropout, Flatten, Lambda, ELU
from keras.layers.convolutional import Convolution2D
from keras.models import Sequential
from keras.optimizers import Adam
from keras.preprocessing.image import img_to_array
from keras.utils.np_utils import to_categorical

from sklearn.model_selection import train_test_split


DATA_DIR = 'data'
LOG_FNAME = os.path.join(DATA_DIR, 'log.csv')
IMG_DIR = os.path.join(DATA_DIR, 'img')

INPUT_IMG_SIZE = (240, 320, 3)
LEARNING_RATE = 1e-4
BATCH_SIZE = 200


def shuffle(data):
    return data.sample(frac=1.).reset_index(drop=True)


def load_driving_log():
    driving_log = pd.read_csv(LOG_FNAME)
    driving_log.loc[:, 'short_img_fname'] = driving_log.img_fname.map(lambda x: x.split('/')[-1])

    driving_log.loc[:, 'no_steering'] = (driving_log.steering_horizontal == 'nothing').astype(np.float32)
    driving_log.loc[:, 'right'] = (driving_log.steering_horizontal == 'right').astype(np.float32)
    driving_log.loc[:, 'left'] = (driving_log.steering_horizontal == 'left').astype(np.float32)

    return driving_log


def preload_images():
    """
    If dataset is small enough, training can be made a lot
    faster via pre-loading all images into RAM.
    For starters it should be good enough.
    """
    driving_log = load_driving_log()
    imgs_list = list(driving_log.short_img_fname)

    resu = {}

    for img_fname_short in tqdm.tqdm(imgs_list):
        img_fname = os.path.join(IMG_DIR, img_fname_short)
        pre_img = mpimg.imread(img_fname)
        resu[img_fname_short] = img_to_array(pre_img)

    return resu


def load_data():
    """ Load the data and apply some basic preprocessing. """
    driving_log = load_driving_log()
    train, valid = train_test_split(driving_log)

    return train, valid


def batch_generator(data, batch_size, augs, preloaded_imgs):
    batch_x = np.zeros((batch_size, INPUT_IMG_SIZE[0], INPUT_IMG_SIZE[1], INPUT_IMG_SIZE[2]), dtype=np.float32)
    batch_y = np.zeros((batch_size, 3), dtype=np.float32)

    data = shuffle(data)
    idx_sample = 0

    while True:
        for idx_batch in range(batch_size):

            if idx_sample == len(data):
                data = shuffle(data)
                idx_sample = 0

            log_record = data.iloc[idx_sample]
            x, y = None, None

            y = log_record[['left', 'right', 'no_steering']].values.astype(np.float32)
            x = imgs[log_record.short_img_fname]

            # apply all the augmentation
            for f in augs:
                x, y = f(x, y)

            batch_x[idx_batch] = x
            batch_y[idx_batch] = y

            idx_sample += 1

        yield batch_x, batch_y



def get_model():
    """
    Define and compile Keras model.
    """
    model = Sequential()
    model.add(Lambda(lambda x: x / 127.5 - 1., input_shape=INPUT_IMG_SIZE))

    model.add(Convolution2D(24, 5, 5, subsample=(2, 2), border_mode='valid', init='he_normal'))
    model.add(ELU())

    model.add(Convolution2D(36, 5, 5, subsample=(2, 2), border_mode='valid', init='he_normal'))
    model.add(ELU())

    model.add(Convolution2D(48, 5, 5, subsample=(2, 2), border_mode='valid', init='he_normal'))
    model.add(ELU())

    model.add(Convolution2D(64, 3, 3, subsample=(1, 1), border_mode='valid', init='he_normal'))
    model.add(ELU())

    model.add(Convolution2D(64, 3, 3, subsample=(1, 1), border_mode='valid', init='he_normal'))
    model.add(ELU())

    model.add(Flatten())

    model.add(Dense(100, init='he_normal'))
    model.add(ELU())

    model.add(Dense(50, init='he_normal'))
    model.add(ELU())

    model.add(Dense(10, init='he_normal'))
    model.add(ELU())

    model.add(Dense(3, init='he_normal'))

    optimizer = Adam(lr=LEARNING_RATE)
    model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])

    callbacks = [
        TensorBoard()
    ]

    return model, callbacks



if __name__ == '__main__':
    imgs = preload_images()
    train, valid = load_data()

    train_gen = batch_generator(train, BATCH_SIZE, [], imgs)
    # valid_gen = batch_generator(train, BATCH_SIZE, [], imgs)

    model, callbacks = get_model()

    history = model.fit_generator(
        train_gen,
        validation_data=train_gen,
        validation_steps=5,
        samples_per_epoch=5*BATCH_SIZE,
        nb_epoch=100,
        callbacks=callbacks
    )


