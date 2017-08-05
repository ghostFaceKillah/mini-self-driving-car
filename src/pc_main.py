from multiprocessing import Manager

import lib.state as state

import pc.image_getter as image_getter
import pc.pygame_driver as pygame_driver
import pc.keyboard_state_sender as keyboard_sender


with Manager() as manager:
    namespace = manager.Namespace()

    namespace.image = None
    namespace.horizontal = state.Horizontal.nothing
    namespace.vertical = state.Vertical.nothing

    jobs = [
        image_getter.VideoStreamClient(namespace),
        pygame_driver.PygameDriver(namespace),
        keyboard_sender.KeyboardSender(namespace)
    ]

    for job in jobs:
        job.start()

    for job in jobs:
        job.join()
