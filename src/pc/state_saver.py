import multiprocessing


class StateSaver(multiprocessing.Process):
    """
    orders saving data to the drive at wanted intervals
    Actually it will push data to a queue, from which
    a set of 3 or so another processes will take data
    and write to the actual drive.

    With frequency xx Hz, check what is in the state
    and put it in the saving queue
    """
    pass
