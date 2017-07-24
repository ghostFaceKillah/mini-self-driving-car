trom client import ClientSocket

rpi = "192.168.192.51"
port = 4567
sock = ClientSocket(rpi, port, False)
sock.connect()
sock.send("uszanowanko ziomeczq!")
