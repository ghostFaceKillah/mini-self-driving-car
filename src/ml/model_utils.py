from keras import backend as K
from keras.models import model_from_json

import lib.constant as cnst


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


def load_model(model_file=cnst.MODEL_FILE, weight_file=cnst.WEIGHT_FILE):
    try:
        with open(model_file) as net_file:
            model = model_from_json(net_file.read())
            model.load_weights(weight_file)
        return model

    except Exception as e:
        print('Problem opening one of the files')
        print('Callback: {}'.format(e))
        exit(1)

