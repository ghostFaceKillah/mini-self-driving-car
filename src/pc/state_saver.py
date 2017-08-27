import cv2
import datetime as dtm
import multiprocessing
import os
import time

import lib.file as file_util


class StateSaver(multiprocessing.Process):
    """
    Saves image and driving log
    """
    # TODO(mike): This is not great way to deal with saving path path
    DUMP_DIR = '../data'

    def __init__(self, the_state):
        super(StateSaver, self).__init__()

        self.state = the_state
        self.file = None

        self.counter = 0
        self.session_id = self.draw_session_identifier()

        self.set_up_dirs()


    @staticmethod
    def draw_session_identifier(length=6):
        """
        To make it easy to merge sessions, we add a random 6-char
        string session identifier. This way you can just copy-paste
        pictures from different sessions together into one directory,
        without name conflicts and still knowing which picture
        comes from which session.
        """
        import random
        import string

        return ''.join(
            random.choice(
                string.ascii_lowercase + string.digits
            ) for _ in range(length)
        )


    def set_up_dirs(self):
        """
        Set up directory structure used to save data
        """
        now = dtm.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
        dirname = "{}-{}".format(now, self.session_id)

        self.img_dir = os.path.join(StateSaver.DUMP_DIR, dirname, 'img')
        file_util.mkdir_p(self.img_dir)

        fname = os.path.join(StateSaver.DUMP_DIR, dirname, 'log.csv')
        self.file = open(fname, 'w')

        # write column names
        self.file.write('counter,')
        self.file.write('steering_horizontal,')
        self.file.write('steering_vertical,')
        self.file.write('short_fname\n')
        self.file.flush()

    def write_data_dot(self):
        img = self.state.image
        horizontal = self.state.horizontal.name
        vertical = self.state.vertical.name

        if img is not None:
            self.counter += 1

            short_img_fname = 'img_{}_{}.jpg'.format(
                self.counter,
                self.session_id
            )

            img_fname = os.path.join(self.img_dir, short_img_fname)

            cv2.imwrite(img_fname, img)

            self.file.write('{},'.format(self.counter))
            self.file.write('{},'.format(horizontal))
            self.file.write('{},'.format(vertical))
            self.file.write('{}\n'.format(short_img_fname))

    def run(self):
        try:
            while True:
                time.sleep(0.1)

                if self.state.recording:
                    self.write_data_dot()

                if self.state.done:
                    self.file.flush()
                    self.file.close()
                    print("Exiting state saver")
                    break

        except:
            self.file.flush()
            self.file.close()

