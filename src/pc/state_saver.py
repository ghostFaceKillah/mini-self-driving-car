import cv2
import datetime as dtm
import multiprocessing
import os
import time


def mkdir_p(dir):
    """ Check if directory exists and if not, make it."""
    if not os.path.exists(dir):
        os.makedirs(dir)


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
        self.set_up_dirs()

    def set_up_dirs(self):
        now = dtm.datetime.now().strftime("%Y-%m-%d--%H:%M:%S")

        self.img_dir = os.path.join(StateSaver.DUMP_DIR, now, 'img')
        mkdir_p(self.img_dir)

        fname = os.path.join(StateSaver.DUMP_DIR, now, 'log.csv')
        self.file = open(fname, 'w')

        # write column names
        self.file.write('"counter",')
        self.file.write('"steering_horizontal",')
        self.file.write('"steering_vertical",')
        self.file.write('"img_fname"\n')
        self.file.flush()

    def write_data_dot(self):
        img = self.state.image
        horizontal = self.state.horizontal.name
        vertical = self.state.vertical.name

        if img is not None:
            short_img_fname = 'img_{}.jpg'.format(self.counter)

            img_fname = os.path.join(self.img_dir, short_img_fname)

            cv2.imwrite(img_fname, img)

            self.file.write('{},'.format(self.counter))
            self.file.write('{},'.format(horizontal))
            self.file.write('{},'.format(vertical))
            self.file.write('{}\n'.format(img_fname))

    def run(self):
        try:
            while True:
                time.sleep(0.1)
                self.counter += 1
                self.write_data_dot()

                if self.state.done:
                    self.file.flush()
                    self.file.close()
                    print("Exiting state saver")
                    break

        except:
            self.file.flush()
            self.file.close()

