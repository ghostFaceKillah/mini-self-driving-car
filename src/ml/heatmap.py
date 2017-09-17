from __future__ import division
import math

import argparse
import numpy as np
from keras import backend as K
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from keras.models import model_from_json

import lib.constant as cnst
import ml.img_augmentation as aug

def cut_sequential_model(model, layer_no):
    """
    Args:
        model: sequential keras model
        layer_no:  number of layer to take outpu from
    Returns:
        a function returning output of layer number layer_no,
        fed input suited for model
    """
    try:
        input_layer = model.layers[0].input
        output_layer = model.layers[layer_no].output
        return K.function([input_layer], [output_layer])
    except Exception as e:
        print("ERROR: {}".format(e.what()))
        return None

def count_intermediate_output(model, img, layer_no):
    """
    Args:
        model: sequential keras model
        img: a numpy array of size appropriate for the model
        layer_no:  number of layer to take output from
    Returns:
        an output of layer_no-th layer from the sequential
        model on img as input
    """
    inter_fun = cut_sequential_model(model, layer_no)
    output = np.squeeze(
            inter_fun([np.expand_dims(img, axis=0)])[0],
            axis=0)
    return output

def load_process_image(path):
    img = mpimg.imread(path)
    img, _ = aug.crop(img, None)
    img, _ = aug.to_gray(img, None)
    img, _ = aug.to_unit_interval_float(img, None)
    img = np.expand_dims(img, axis=-1)
    return img

def get_feature_maps(tensor, maps):
    """
    Args:
        tensor (numpy array): an intermediate output from
                              the neural network, of size
                              (H, W, ?)
        maps (list): a list of numbers of maps to show
    """
    feature_maps = [ tensor[:,:,mp] for mp in maps ]
    return feature_maps

def show_images(images, titles):
    """
    Args:
        images (list): a list of images to display
        titles (list):  a list of titles
    """
    ln = len(images)
    h, w = int(math.ceil(ln / 2)), 2
    for i, img in enumerate(images):
        subplot = plt.subplot(h, w, i + 1)
        subplot.imshow(img)
    plt.show()

def parser():
    parser = argparse.ArgumentParser("heatmap.py")
    parser.add_argument("image_path", type=str,
                        help="path to image to view heatmap of")
    parser.add_argument("layer_no", type=int,
                        help="number of layer to stop the computation on")
    parser.add_argument("feature_maps", type=int, nargs="+",
                        help="number of feature map to display")
    return parser

if __name__ == '__main__':
    args = parser().parse_args()
    model = None
    try:
        with open(cnst.MODEL_FILE) as net_file:
            model = model_from_json(net_file.read())
            model.load_weights(cnst.WEIGHT_FILE)
    except Exception as e:
        print('Problem opening one of the files')
        print('Callback: {}'.format(e))
        exit(1)
    output = count_intermediate_output(
        model,
        load_process_image(args.image_path),
        args.layer_no)
    images = get_feature_maps(output, args.feature_maps)
    show_images(
            images,
            [ "Layer {}, feature map {}".format(
                    args.layer_no,
                    args.feature_maps[i]
                ) for i in range(len(images))]
            )
