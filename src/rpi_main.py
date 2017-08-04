from raspi.steering import Steering


driver = Steering()
# streamer = RpiStreamer(cnst.VIDEOS_STREAMING_PORT)

print('starting driver thread')
driver.start()

driver.join()

# print('starting streamer thread')
# streamer.start()

# driver.join()
#streamer.join()
