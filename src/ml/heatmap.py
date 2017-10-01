from __future__ import division
import math
import os

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

def show_images(images, title=None, titles=None, save_as=None, plot_width=2):
    """
    Args:
        images (list): a list of images to display
        title (str):   the title
        titles (list):  a list of titles
        save_as (str):  path to save the plot
    """
    ln = len(images)
    h, w = int(math.ceil(ln / plot_width)), plot_width
    fig = plt.figure()
    for i, img in enumerate(images):
        subplot = fig.add_subplot(h, w, i + 1)
        subplot.imshow(img, cmap='gray')
        if titles is not None:
            subplot.set_title(titles[i])
        subplot.axis('off')
    if title is not None:
        plt.suptitle(title)
    if save_as is None:
        plt.show()
    else:
        plt.savefig(save_as)
    plt.close()

def save_layer_heatmaps(layer_no, in_path, out_path, model):
    """
    Args:
        layer_no (int):   number of the layer to be saved
        in_path (str):    path to the input file
        out_path (str):   path to the output file
        model:            sequential Keras model
    """
    output = count_intermediate_output(
        model,
        load_process_image(in_path),
        layer_no)
    try:
        n_feature_maps = output.shape[2]
    except IndexError:
        print('attempt to show output of non-convolutional layer')
        return
    feature_maps = list(range(n_feature_maps))
    images = get_feature_maps(output, feature_maps)
    show_images(
            images,
            title="Layer {}".format(layer_no),
            save_as=out_path,
            plot_width=math.ceil(len(feature_maps) /
                math.sqrt(len(feature_maps)))
            )

def save_all_layers_heatmaps(in_path, output_dir,
                             model_path=cnst.MODEL_FILE,
                             weight_path=cnst.WEIGHT_FILE):
    """
    Args:
        output_dir (str):  where to put all the files
        in_path (str):     path to the image to be shown
        model_path (str):  path to the model
        weight_path (str): path to the model's weights
    """
    model = None
    try:
        with open(model_path) as net_file:
            model = model_from_json(net_file.read())
            model.load_weights(weight_path)
    except Exception as e:
        print('Problem opening one of the files')
        print('Callback: {}'.format(e))
        return

    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)
    
    no_layers = len(model.layers)

    for i in range(no_layers):
        save_layer_heatmaps(i, in_path,
                            os.path.join(output_dir, "l{}".format(i)),
                            model)

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
