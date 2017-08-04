import multiprocessing


class KeyboardSender(multiprocessing.Process):
    """
    sends keboard state to Raspi 10 times per second

    while True:
        with lock:
            keyboard_state = state.keyboard_state
            send_keyboard_state_to_raspi
    """

    def __init__(self, the_state):
        super(KeyboardSender, self).__init__()
        self.state = the_state


    def run(self):

        while True:
            time.sleep(0.1)

            # Send direction state
            if status['left_right'] == 'left':
                msg = cnst.msg('left', 'start')
            elif status['left_right'] == 'right':
                msg = cnst.msg('right', 'start')
            else:
                msg = cnst.msg('right', 'stop')

            send(msg)

            # Send start stop msg
            if status['up_down'] == 'forward':
                msg = cnst.msg('up', 'start')
            elif status['up_down'] == 'back':
                msg = cnst.msg('down', 'start')
            else:
                msg = cnst.msg('up', 'stop')

            send(msg)
