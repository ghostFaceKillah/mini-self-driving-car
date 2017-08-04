import multiprocessing

import lib.constant as cnst
import lib.state as state


the_state = {
    state.StatePart.lock: multiprocessing.Lock(),
    state.StatePart.image: None,
    state.StatePart.keyboard: {
        state.Axis.up_down: None,
        state.Axis.left_right: None
    }
}



if __name__ == '__main__':
    pygame_handler = PygameHandler()
    pygame_handler.start()
    pygame_handler.join()


#########################################################################



from pc_steer import PygameDriver
from pc_stream import PygameStreamClient

import pygame

import lib.constant as cnst

pygame.init()
screen = pygame.display.set_mode((640, 480))

driver = PygameDriver(cnst.RASPI_IP, cnst.KEYBOARD_EVENTS_PORT,
                      cnst.PYGAME_WINDOW_SIZE, screen)
stream_client = PygameStreamClient(cnst.RASPI_IP, cnst.VIDEOS_STREAMING_PORT,
                                   screen)

print('Starting driver thread')
driver.start()

print('Starting streaming thread')
stream_client.start()

driver.join()
stream_client.join()
