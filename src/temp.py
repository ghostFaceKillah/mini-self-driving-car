from pc.image_getter import VideoStreamClient
from pc.pygame_driver import PygameDriver

from multiprocessing import Manager

# the_state = TheState()


with Manager() as manager:
    namespace = manager.Namespace()

    namespace.image = None

    stream = VideoStreamClient(namespace)
    pygame_display = PygameDriver(namespace)

    stream.start()
    pygame_display.start()

    stream.join()
    pygame_display.join()

