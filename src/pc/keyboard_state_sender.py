import multiprocessing

class KeyboardSender(multiprocessing.Process):
    """
    sends keboard state to Raspi 10 times per second

    while True:
        with lock:
            keyboard_state = state.keyboard_state
            send_keyboard_state_to_raspi
    """
    pass


