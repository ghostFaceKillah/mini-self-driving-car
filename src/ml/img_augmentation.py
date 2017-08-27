"""
A collection of utils that is used for adjusting the images.

Some of them are inspired by excellent tensorpack package, see
https://github.com/ppwwyyxx/tensorpack/

"""

import cv2
import numpy as np


def crop(img, steering):
    cropped_img = img[140:, :]
    return cropped_img, steering


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
    max_translation = 10.0

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
    rg = 2
    theta = np.pi / 180 * np.random.uniform(-rg, rg)
    rotation_matrix = np.array([[np.cos(theta), -np.sin(theta), 0],
                                [np.sin(theta), np.cos(theta), 0]])

    rotated_img = cv2.warpAffine(img, rotation_matrix,
                                 (img.shape[1], img.shape[0]))

    return rotated_img, steering


def to_unit_interval_float(img, steering):
    """
    Input img is of type np.uint8 in range 0 255
    Output img is of type np.float32 in range -1 1
    """
    new_img = img.astype(np.float32) / 127.5 - 1.

    return new_img, steering


def hue_shift(img, steering):
    """
    Perform a hue shift "Rotate colors"
    """

    hi = 0
    lo = 180

    hue_delta = np.random.uniform(lo, hi, size=None) % 180  # from 0 to 179
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    hsv[..., 0] = (hsv[..., 0] + hue_delta) % 180
    new_img = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)

    return new_img, steering


def to_gray(img, steering):

    new_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    return new_img, steering


def brightness_additive(img, steering):
    """
    Adjust brightness by adding random number
    """
    delta = 100
    noise = np.random.uniform(-delta, delta, size=None)

    old_dtype = img.dtype
    img = img.astype('float32')
    img += noise
    img = np.clip(img, 0, 255)
    img = img.astype(old_dtype)

    return img, steering


def brightness_multiplicative(img, steering):
    """
    Adjust brightness by multiplying by a random number.
    """
    lo = 0.5
    hi = 1.3
    noise = np.random.uniform(lo, hi, size=None)

    old_dtype = img.dtype
    img = img.astype('float32')
    img *= noise
    img = np.clip(img, 0, 255)
    img = img.astype(old_dtype)

    return img, steering


def contrast(img, steering):
    """
    Apply x = (x - mean) * contrast factor + mean to each channel
    """

    lo = 2. / 3
    hi = 3. / 2
    contrast_factor = np.random.uniform(lo, hi, size=None)

    old_dtype = img.dtype
    img = img.astype('float32')
    mean = np.mean(img, axis=(0, 1), keepdims=True)
    img = (img - mean) * contrast_factor + mean
    img = np.clip(img, 0, 255)
    new_img = img.astype(old_dtype)

    return new_img, steering
