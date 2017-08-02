from rpi_steer import RpiDriver

import lib.constant as cnst

driver = RpiDriver(cnst.KEYBOARD_EVENTS_PORT)

print('starting driver thread')
driver.start()

driver.join()
