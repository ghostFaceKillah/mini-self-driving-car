"""
There is an easy heuristic that when starting out with new neural nets project.
You should take a small piece of your data and try to overfit it.

If you can't, usually it means you are doing something wrong.

"""
import cv2
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import glob
import os
import pandas as pd
import shutil
import tqdm

from keras.callbacks import ModelCheckpoint, TensorBoard
from keras.layers import Dense, Dropout, Flatten, ELU
from keras.layers.convolutional import Conv2D
from keras.models import Sequential
from keras.optimizers import Adam
from keras.preprocessing.image import img_to_array

from sklearn.model_selection import train_test_split

import lib.file as file_util
import ml.img_augmentation as img_aug

DATA_DIR = 'data/turn_right'
LOG_FNAME = os.path.join(DATA_DIR, 'log.csv')
IMG_DIR = os.path.join(DATA_DIR, 'img')

# INPUT_IMG_SIZE = (240, 320, 3)
# cropped / grayed ?

# INPUT_IMG_SIZE = (100, 320, 3)
INPUT_IMG_SIZE = (100, 320, 1)

BATCH_SIZE = 128
VALID_SPLIT = 0.10

MODEL_NAME = 'six'
MODEL_SAVEPATH = None


################## Path helpers

def current_experiment_savepath():
    global MODEL_SAVEPATH

    if MODEL_SAVEPATH is None:
        runs_list = glob.glob('models/{}_run_*'.format(MODEL_NAME))

        if len(runs_list) == 0:
            MODEL_SAVEPATH = 'models/{}_run_00'.format(MODEL_NAME)
        else:
            last_run = sorted(runs_list)[-1]
            last_run_no = int(last_run.split('_')[-1])
            new_no = last_run_no + 1

            MODEL_SAVEPATH = 'models/{}_run_{:02d}'.format(MODEL_NAME, new_no)

    file_util.mkdir_p(MODEL_SAVEPATH)
    shutil.copy(__file__, os.path.join(MODEL_SAVEPATH, 'model.py'))

    return MODEL_SAVEPATH


def model_weights_fname():
    return os.path.join(current_experiment_savepath(), "weights.hdf5")


def model_def_fname():
    return os.path.join(current_experiment_savepath(), "model.json")


def model_weights_fname_detailed():
    return os.path.join(
        current_experiment_savepath(),
        "weights-epoch-{epoch:02d}-val_acc-{val_acc:.2f}.hdf5"
    )



######################## Data loading

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

        # Moved to data processing
        # img = img_to_array(pre_img)
        # img = img / 127.5 - 1.

        # Maybe still want to crop etc for simplified data tasks
        img = pre_img

        resu[img_fname_short] = img

    return resu


def load_data():
    """ Load the data and apply some basic preprocessing. """
    driving_log = load_driving_log()
    train, valid = train_test_split(driving_log, test_size=VALID_SPLIT)

    return train, valid


######################## Batch generator

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

            if len(x.shape) == 2:
                batch_x[idx_batch] = x[..., np.newaxis]
            else:
                batch_x[idx_batch] = x
            batch_y[idx_batch] = y

            idx_sample += 1

        yield batch_x, batch_y


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
    # TODO: Cast to float, center!

    x = np.zeros(
        # cropped!
        (len(y), INPUT_IMG_SIZE[0], INPUT_IMG_SIZE[1], INPUT_IMG_SIZE[2]),
        dtype=np.float32
    )

    for idx, dlog_row in enumerate(dlog.itertuples()):
        x[idx] = imgs[dlog_row.short_fname]

    return x, y



################################### Model

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

    model.add(Conv2D(64, (3, 3), strides=(1, 1), padding='same'))
    model.add(ELU())

    model.add(Conv2D(64, (3, 3), strides=(1, 1), padding='same'))
    model.add(ELU())

    model.add(Conv2D(64, (3, 3), strides=(1, 1), padding='same'))
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
        TensorBoard(),
        ModelCheckpoint(
            model_weights_fname_detailed(),
            monitor='val_acc',
            save_weights_only=True,
            save_best_only=True
        )

    ]

    return model, callbacks


################################# Main loops

def main_simplified_fit():
    x, y = vanilla_data()
    model, callbacks = get_model()

    # serialize model to json
    with open(model_def_fname(), 'w') as json_file:
        json_file.write(model.to_json())

    model.fit(x, y, epochs=10, batch_size=128)
    model.save_weights(model_weights_fname())


def main_fit_with_generator():
    imgs = preload_images()
    train, valid = load_data()

    train_gen = batch_generator(train, BATCH_SIZE,
        [
            img_aug.crop,
            img_aug.to_gray,
            img_aug.contrast,
            img_aug.brightness_additive,
            img_aug.random_flip,
            img_aug.random_rotation,
            img_aug.random_translation,
            img_aug.to_unit_interval_float
        ],
        imgs
    )

    valid_gen = batch_generator(valid, BATCH_SIZE,
        [
            img_aug.crop,
            img_aug.to_gray,
            img_aug.to_unit_interval_float
        ],
        imgs
    )

    model, callbacks = get_model()

    # serialize model to json
    with open(model_def_fname(), 'w') as json_file:
        json_file.write(model.to_json())

    history = model.fit_generator(
        train_gen,
        validation_data=valid_gen,
        validation_steps=len(valid) / BATCH_SIZE,
        steps_per_epoch=len(train) / BATCH_SIZE,
        epochs=100,
        callbacks=callbacks
    )

    model.save_weights(model_weights_fname())


if __name__ == '__main__':
    # main_simplified_fit()
    main_fit_with_generator()
