from pc_steer import PygameDriver
from pc_stream import VlcStreamClient

import lib.constant as cnst

driver = PygameDriver(cnst.RASPI_IP, cnst.KEYBOARD_EVENTS_PORT,
                      cnst.PYGAME_WINDOW_SIZE)
vlc = VlcStreamClient(cnst.RAPI_IP, cnst.VIDEOS_STREAMING_PORT)

print('Starting driver thread')
driver.start()

print('Starting streaming thread')
vlc.start()

driver.join()
vlc.join()
