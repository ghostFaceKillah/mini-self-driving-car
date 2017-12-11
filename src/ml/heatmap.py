from __future__ import division

import argparse
import math

import matplotlib.pyplot as plt
import numpy as np
from keras.models import model_from_json

import lib.constant as cnst
from ml.data_utils import load_process_image
from ml.model_utils import cut_sequential_model
from ml.utils import group


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


def get_all_feature_maps(tensor):
    """
    Args:
        tensor (numpy array): an intermediate output from the 
                              neural network, of size (H, W, ?)

    """
    feature_maps = [tensor[:,:,mp] for mp in range(tensor.shape[-1])]
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
        subplot.imshow(img, cmap='gray')
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


def one_layer_some_feature_maps():
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
        args.layer_no
    )

    images = get_feature_maps(output, args.feature_maps)
    show_images(
        images,
        [
            "Layer {}, feature map {}".format(
                    args.layer_no,
                    args.feature_maps[i]
            ) for i in range(len(images))
        ]
    )


def one_layer_all_feature_maps():
    model = None
    try:
        with open(cnst.MODEL_FILE) as net_file:
            model = model_from_json(net_file.read())
            model.load_weights(cnst.WEIGHT_FILE)

    except Exception as e:
        print('Problem opening one of the files')
        print('Callback: {}'.format(e))
        exit(1)

    image_path = '/home/misiu/src/self-driving/mini-self-driving-car/datasets/turn_right/img/img_1_kweym3.jpg'

    for layer_no in range(14):
        print(layer_no)

        output = count_intermediate_output(
            model,
            load_process_image(image_path),
            layer_no
        )

        images = get_all_feature_maps(output)

        grouped_images = list(group(images, 6))

        big_img = np.hstack([
            np.vstack(grp)
            for grp in grouped_images
        ])

        plt.figure(figsize=(60, 60))
        plt.imshow(big_img, cmap='gray', interpolation='none')
        plt.title(
            "Layer {} - {}".format(layer_no, model.layers[layer_no].name)
        )
        plt.savefig('out/layer_{}.png'.format(layer_no))
        plt.close()





if __name__ == '__main__':
    # one_layer_some_feature_maps()
    one_layer_all_feature_maps()
