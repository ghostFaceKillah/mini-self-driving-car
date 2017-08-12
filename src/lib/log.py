import logging



class FakeLogger():
    def __init__(self, name):
        self.name = name

    def info(self, msg):
        print("[{}] {}".format(self.name, msg))


def get(name):
    # return logging.getLogger(name)
    return FakeLogger(name)
