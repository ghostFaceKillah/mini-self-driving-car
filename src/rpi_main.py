from raspi.steering import Steering
from raspi.video import VideoStreaming


# driver = Steering()
# streamer = RpiStreamer(cnst.VIDEOS_STREAMING_PORT)
streamer = VideoStreaming()

streamer.start()

# print('starting driver thread')
# driver.start()

# driver.join()

# print('starting streamer thread')
# streamer.start()

# driver.join()
#streamer.join()
