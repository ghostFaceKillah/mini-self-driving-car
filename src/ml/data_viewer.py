"""
Data
"""

import cv2
import datetime as dtm
import numpy as np
import os
import pandas as pd
import pygame
import shutil
import sys
import time

import lib.constant as cnst
import lib.state as state


DATASET_DIR = 'data/turn_right'
IMG_PATH = os.path.join(DATASET_DIR, 'img')
LOG_PATH = os.path.join(DATASET_DIR, 'log.csv')
LOG_BACKUP_PATH_TEMPLATE = os.path.join(DATASET_DIR, "backup-log-{}.csv")

BLACKOUT_TOP = True


def load_img(short_im_fname):
    img = cv2.imread(os.path.join(IMG_PATH, short_im_fname))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    return img



class DatasetViewer():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(cnst.DISPLAY_VIDEO_RESOLUITION)
        self.df = pd.read_csv(LOG_PATH)
        self.df.loc[:, 'horizontal_override'] = self.df.steering_horizontal

        self.pressing_state = None
        self.override_state = None
        self.idx = 0

    def display(self, img):
        img = np.transpose(img, axes=(1, 0, 2))
        self.screen.blit(pygame.surfarray.make_surface(img), (0, 0))
        pygame.display.flip()

    def display_additional_information(self, img):
        steer = self.df.loc[self.idx].steering_horizontal
        override = self.df.loc[self.idx].horizontal_override

        txt = "idx: {} out of {}, steering: {}, override: {}".format(
            self.idx, len(self.df), steer, override
        )

        if BLACKOUT_TOP:
            img [:140, :] = np.array([0, 0, 0])

        # display two horizon guiding lines
        img[140, :] = np.array([255, 0, 0])
        img[120, :] = np.array([0, 255, 0])

        img = cv2.resize(
            img,
            cnst.DISPLAY_VIDEO_RESOLUITION,
            interpolation=cv2.INTER_CUBIC
        )

        out_img = cv2.putText(
            img,
            txt,
            (20, 30),                 # origin
            cv2.FONT_HERSHEY_SIMPLEX, # font
            1.0,                      # font scale
            (255, 0, 0),              # color
            2,                        # thickness
            cv2.LINE_AA               # Line type
        )

        return out_img

    def update_display(self):
        short_im_fname = self.df.loc[self.idx, 'short_fname']

        img = load_img(short_im_fname)
        img = self.display_additional_information(img)

        self.display(img)


    def handle_closing(self):
        # make saver here, I guess

        self.df.loc[:, 'steering_horizontal'] = self.df.horizontal_override
        self.df.to_csv(LOG_PATH)

        sys.exit(0)

    def handle_events(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.handle_closing()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    self.pressing_state = 'next'
                if event.key == pygame.K_p:
                    self.pressing_state = 'previous'
                if event.key == pygame.K_w:
                    self.override_state = 'nothing'
                    self.pressing_state = 'next'
                if event.key == pygame.K_a:
                    self.override_state = 'left'
                    self.pressing_state = 'next'
                if event.key == pygame.K_d:
                    self.override_state = 'right'
                    self.pressing_state = 'next'
            if event.type == pygame.KEYUP:
                self.pressing_state = None
                self.override_state = None

    def resolve_actions(self):
        if self.override_state is not None:
            self.df.loc[self.idx, 'horizontal_override'] = self.override_state

        if self.pressing_state == 'next':
            self.idx = (self.idx + 1) % len(self.df)
        if self.pressing_state == 'previous':
            self.idx = (self.idx - 1) % len(self.df)


    def backup_log_csv(self):
        now = dtm.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
        backup_filepath = LOG_BACKUP_PATH_TEMPLATE.format(now)
        shutil.copy(LOG_PATH, backup_filepath)

    def run(self):
        self.backup_log_csv()

        while True:
            # handle events
            self.update_display()
            self.handle_events()
            self.resolve_actions()

            time.sleep(1/60.)


if __name__ == '__main__':
    data_viewer = DatasetViewer()
    data_viewer.run()


