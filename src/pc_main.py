from multiprocessing import Manager

import lib.state as state
import lib.constant as cnst

import pc.image_getter as image_getter
import pc.pygame_driver as pygame_driver
import pc.keyboard_state_sender as keyboard_sender
import pc.state_saver as state_saver
import pc.neural_network_computer as nn_computer


with Manager() as manager:
    namespace = manager.Namespace()

    # Set up the state variables
    namespace.image = None
    namespace.horizontal = state.Horizontal.nothing
    namespace.vertical = state.Vertical.nothing
    namespace.recording = False
    namespace.auto = False
    namespace.showpred = False
    namespace.direction_probabilities = None
    namespace.done = False

    jobs = [
        image_getter.VideoStreamClient(namespace),
        pygame_driver.PygameDriver(namespace),
        keyboard_sender.KeyboardSender(namespace),
        state_saver.StateSaver(namespace),
        nn_computer.NNFeedForwarder(namespace, cnst.MODEL_FILE, cnst.WEIGHT_FILE),
    ]

    for job in jobs:
        job.start()

    for job in jobs:
        job.join()
