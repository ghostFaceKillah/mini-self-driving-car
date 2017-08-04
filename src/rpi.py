from rpi_steer import RpiDriver
from rpi_stream import RpiStreamer

import lib.constant as cnst

driver = RpiDriver(cnst.KEYBOARD_EVENTS_PORT)
streamer = RpiStreamer(cnst.VIDEOS_STREAMING_PORT)

print('starting driver thread')
driver.start()

print('starting streamer thread')
streamer.start()

driver.join()
streamer.join()
