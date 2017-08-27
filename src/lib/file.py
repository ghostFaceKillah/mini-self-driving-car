import os

def mkdir_p(dir):
    """ Check if directory exists and if not, make it."""
    if not os.path.exists(dir):
        os.makedirs(dir)
