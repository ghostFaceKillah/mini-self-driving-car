import multiprocessing
import time
import numpy as np
import operator

from keras.models import model_from_json

import lib.constant as cnst
import lib.state as state

class NNFeedForwarder(multiprocessing.Process):
    def __init__(self, the_state, net_file, weight_file):
        super(NNFeedForwarder, self).__init__()
        self.state = the_state
        self.net_file = net_file
        self.weight_file = weight_file
        self.model = None

    # TODO move the pixels by -127.5 in each color
    def preprocess(self, image):
        return image

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
        self.read_model()
        if not self.model:
            return

        while True:
            time.sleep(0.1)
            if self.state.image is not None:
                prediction = self.model.predict(self.state.image[np.newaxis, :])[0]
                if self.state.auto:
                    index, value = max(enumerate(prediction), key=operator.itemgetter(1))
                    self.state.direction_probabilities = prediction
                    if index == 0:
                        self.state.horizontal = state.Horizontal.left
                    elif index == 1:
                        self.state.horizontal = state.Horizontal.right
                    elif index == 2:
                        self.state.horizontal = state.Horizontal.nothing

            if self.state.done:
                print('exiting neural network feed-forwarder')
                break
