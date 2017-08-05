from raspi.steering import Steering
from raspi.video import VideoStreaming


driver = Steering()
streamer = VideoStreaming()

streamer.start()
driver.start()

streamer.join()
driver.join()
