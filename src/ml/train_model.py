"""
There is an easy heuristic that when starting out with new neural nets project.
You should take a small piece of your data and try to overfit it.

If you can't, usually it means you are doing something wrong.

"""
import cv2
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import tqdm

from keras.callbacks import ModelCheckpoint, TensorBoard
from keras.layers import Dense, Dropout, Flatten, ELU
from keras.layers.convolutional import Conv2D
from keras.models import Sequential
from keras.optimizers import Adam
from keras.preprocessing.image import img_to_array

from sklearn.model_selection import train_test_split


DATA_DIR = 'data/first_big_dataset'
LOG_FNAME = os.path.join(DATA_DIR, 'log.csv')
IMG_DIR = os.path.join(DATA_DIR, 'img')

INPUT_IMG_SIZE = (240, 320, 3)
BATCH_SIZE = 128
VALID_SPLIT = 0.10

MODEL_DEFINITION_FNAME = 'models/second.json'
MODEL_WEIGHTS_FNAME = 'models/second.h5'


def shuffle(data):
    return data.sample(frac=1.).reset_index(drop=True)


def load_driving_log():
    driving_log = pd.read_csv(LOG_FNAME)

    driving_log.loc[:, 'no_steering'] = (
        driving_log.steering_horizontal == 'nothing'
    ).astype(np.float32)

    driving_log.loc[:, 'right'] = (
        driving_log.steering_horizontal == 'right'
    ).astype(np.float32)

    driving_log.loc[:, 'left'] = (
        driving_log.steering_horizontal == 'left'
    ).astype(np.float32)

    print("Basic stats for data")
    print("There are {} data points".format(len(driving_log)))
    print(driving_log[['left', 'right', 'no_steering']].mean())

    return driving_log


def preload_images():
    """
    If dataset is small enough, training can be made a lot
    faster via pre-loading all images into RAM.
    For starters it should be good enough.
    """
    print("Preloading images into RAM...")

    driving_log = load_driving_log()
    imgs_list = list(driving_log.short_fname)

    resu = {}

    for img_fname_short in tqdm.tqdm(imgs_list):
        img_fname = os.path.join(IMG_DIR, img_fname_short)
        pre_img = mpimg.imread(img_fname)
        img = img_to_array(pre_img)
        img = img / 127.5 - 1.
        resu[img_fname_short] = img

    return resu


def load_data():
    """ Load the data and apply some basic preprocessing. """
    driving_log = load_driving_log()
    train, valid = train_test_split(driving_log, test_size=VALID_SPLIT)

    return train, valid


def batch_generator(data, batch_size, augs, preloaded_imgs):
    batch_x = np.zeros([batch_size] + list(INPUT_IMG_SIZE), dtype=np.float32)
    batch_y = np.zeros((batch_size, 3), dtype=np.float32)

    data = shuffle(data)
    idx_sample = 0
    relevant_cols = ['left', 'right', 'no_steering']

    while True:
        for idx_batch in range(batch_size):

            if idx_sample == len(data):
                data = shuffle(data)
                idx_sample = 0

            log_record = data.iloc[idx_sample]

            y = log_record[relevant_cols].values.astype(np.float32)
            x = preloaded_imgs[log_record.short_fname]

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
    # model.add(Lambda(lambda x: x / 127.5 - 1., input_shape=INPUT_IMG_SIZE))

    model.add(Conv2D(24, (5, 5), strides=(2, 2),
                     padding='valid', input_shape=INPUT_IMG_SIZE))
    model.add(ELU())

    model.add(Conv2D(36, (5, 5), strides=(2, 2), padding='valid'))
    model.add(ELU())

    model.add(Conv2D(48, (5, 5), strides=(2, 2), padding='valid'))
    model.add(ELU())

    model.add(Conv2D(64, (3, 3), strides=(1, 1), padding='valid'))
    model.add(ELU())

    model.add(Conv2D(64, (3, 3), strides=(1, 1), padding='valid'))
    model.add(ELU())

    model.add(Conv2D(64, (3, 3), strides=(1, 1), padding='valid'))
    model.add(ELU())

    model.add(Flatten())

    model.add(Dense(100))
    model.add(ELU())

    model.add(Dense(50))
    model.add(ELU())

    model.add(Dense(10))
    model.add(ELU())
    model.add(Dropout(0.5))

    model.add(Dense(3, activation='softmax'))

    optimizer = Adam()
    model.compile(
        optimizer=optimizer,
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    callbacks = [
        TensorBoard()
    ]

    return model, callbacks


def vanilla_data():
    """
    No batches, no problem.
    """
    dlog = load_driving_log()
    y = dlog[[
        'left',
        'right',
        'no_steering'
    ]].values.astype(np.float32)

    imgs = preload_images()

    x = np.zeros(
        (len(y), INPUT_IMG_SIZE[0], INPUT_IMG_SIZE[1], INPUT_IMG_SIZE[2]),
        dtype=np.float32
    )

    for idx, dlog_row in enumerate(dlog.itertuples()):
        x[idx] = imgs[dlog_row.short_fname]

    return x, y


def main_simplified_fit():
    x, y = vanilla_data()
    model, callbacks = get_model()

    # serialize model to json
    with open(MODEL_DEFINITION_FNAME, 'w') as json_file:
        json_file.write(model.to_json())

    model.fit(x, y, epochs=10, batch_size=128)
    model.save_weights(MODEL_WEIGHTS_FNAME)


def random_flip(img, steering):
    if np.random.rand() < 0.5:
        return img, steering
    else:
        new_steering = np.array([
            steering[1],
            steering[0],
            steering[2]
        ])

        new_img = cv2.flip(img, 1)

        return new_img, new_steering


def random_translation(img, steering):
    max_translation = 25.0

    x_translation_size = np.random.uniform(-max_translation, max_translation)
    y_translation_size = np.random.uniform(-max_translation, max_translation)

    translation_matrix = np.array([
        [1.0, 0.0, x_translation_size],
        [0.0, 1.0, y_translation_size]
    ])

    translated_img = cv2.warpAffine(img, translation_matrix,
                                    (img.shape[1], img.shape[0]))

    # NOTE: Warning, can interfere with steering
    return translated_img, steering


def random_rotation(img, steering):
    rg = 5
    theta = np.pi / 180 * np.random.uniform(-rg, rg)
    rotation_matrix = np.array([[np.cos(theta), -np.sin(theta), 0],
                                [np.sin(theta), np.cos(theta), 0]])

    rotated_img = cv2.warpAffine(img, rotation_matrix,
                                 (img.shape[1], img.shape[0]))

    return rotated_img, steering


def main_fit_with_generator():
    imgs = preload_images()
    train, valid = load_data()

    train_gen = batch_generator(train, BATCH_SIZE, [random_flip, random_translation], imgs)
    valid_gen = batch_generator(valid, BATCH_SIZE, [], imgs)

    model, callbacks = get_model()

    # serialize model to json
    with open(MODEL_DEFINITION_FNAME, 'w') as json_file:
        json_file.write(model.to_json())

    history = model.fit_generator(
        train_gen,
        validation_data=valid_gen,
        validation_steps=len(valid) / BATCH_SIZE,
        steps_per_epoch=len(train) / BATCH_SIZE,
        nb_epoch=100,
        callbacks=callbacks
    )

    model.save_weights(MODEL_WEIGHTS_FNAME)


if __name__ == '__main__':
    # main_simplified_fit()
    main_fit_with_generator()
