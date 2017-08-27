import matplotlib.pyplot as plt

import multiprocessing
import time
import numpy as np
import operator

from keras.models import model_from_json

import lib.state as state
import ml.img_augmentation as img_aug

from keras.backend.tensorflow_backend import set_session
import tensorflow as tf


class NNFeedForwarder(multiprocessing.Process):
    def __init__(self, the_state, net_file, weight_file):
        super(NNFeedForwarder, self).__init__()
        self.state = the_state
        self.net_file = net_file
        self.weight_file = weight_file
        self.model = None

        self.augs = [
            img_aug.crop,
            img_aug.to_gray
        ]

    def preprocess(self, image):
        new_img = image.copy()

        for f in self.augs:
            new_img, _ = f(new_img, np.array([0, 0, 0]))

        # plt.imshow(new_img)
        # plt.imshow(new_img, cmap='gray')
        # plt.show()

        new_img, _ = img_aug.to_unit_interval_float(new_img, None)
        if len(new_img.shape) == 2:
            new_img = new_img[..., np.newaxis]

        batch_size = 1
        batchified = np.zeros([batch_size] + list(new_img.shape), dtype=np.float32)
        for i in range(batch_size):
            batchified[i] = new_img

        # batchified = new_img[np.newaxis, :]

        return batchified

    def read_model(self):
        try:
            with open(self.net_file) as net_file:
                self.model = model_from_json(net_file.read())
                self.model.load_weights(self.weight_file)
        except Exception as e:
            print('Problem opening one of the files: {}, {}'
                    .format(self.net_file, self.weight_file))
            print('Callback: {}'.format(e))
            self.model = None

    def run(self):
        """
        Fix for annoying TF bug. Without this, we get CUDDN
        cuda_dnn.cc:385] could not create cudnn handle: CUDNN_STATUS_INTERNAL_ERROR
        cuda_dnn.cc:352] could not destroy cudnn handle: CUDNN_STATUS_BAD_PARAM
        etc...
        """
        config = tf.ConfigProto()
        config.gpu_options.allow_growth = True
        config.gpu_options.per_process_gpu_memory_fraction = 0.1
        set_session(tf.Session(config=config))

        self.read_model()
        if not self.model:
            return


        while True:
            time.sleep(0.1)
            if self.state.image is not None:
                processed_img = self.preprocess(self.state.image)

                prediction = self.model.predict(processed_img)[0]
                self.state.direction_probabilities = prediction

                if self.state.auto:
                    index, value = max(enumerate(prediction), key=operator.itemgetter(1))
                    if index == 0:
                        self.state.horizontal = state.Horizontal.left
                    elif index == 1:
                        self.state.horizontal = state.Horizontal.right
                    elif index == 2:
                        self.state.horizontal = state.Horizontal.nothing

            if self.state.done:
                print('exiting neural network feed-forwarder')
                break
