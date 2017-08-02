from pc_steer.py import PygameDriver
import lib.constant as cnst

driver = PygameDriver(cnst.RASPI_IP, cnst.KEYBOARD_EVENTS_PORT,
                      cnst.PYGAME_WINDOW_SIZE)

print('Starting driver thread')
driver.start()

driver.join()
