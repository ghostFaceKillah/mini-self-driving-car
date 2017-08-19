"""
Data
"""

import cv2
import os
import numpy as np
import pandas as pd
import pygame
import sys
import time

import lib.constant as cnst


DATASET_DIR = 'data/turn_right'
IMG_PATH = os.path.join(DATASET_DIR, 'img')
LOG_PATH = os.path.join(DATASET_DIR, 'log.csv')


def load_img(short_im_fname):
    img = cv2.imread(os.path.join(IMG_PATH, short_im_fname))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(
        img,
        cnst.DISPLAY_VIDEO_RESOLUITION,
        interpolation=cv2.INTER_CUBIC
    )

    return img


class DatasetViewer():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(cnst.DISPLAY_VIDEO_RESOLUITION)
        self.df = pd.read_csv(LOG_PATH)
        self.pressing_state = None
        self.idx = 0

    def display(self, img):
        img = np.transpose(img, axes=(1, 0, 2))
        self.screen.blit(pygame.surfarray.make_surface(img), (0, 0))
        pygame.display.flip()

    def display_additional_information(self, img):
        steer = self.df.loc[self.idx].steering_horizontal

        txt = "idx: {} out of {}, steering: {}".format(
            self.idx, len(self.df), steer
        )

        out_img = cv2.putText(
            img,
            txt,
            (20, 30),                 # origin
            cv2.FONT_HERSHEY_SIMPLEX, # font
            0.7,                      # font scale
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

    def handle_events(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                # make saver here, I guess
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    self.pressing_state = 'next'
                if event.key == pygame.K_p:
                    self.pressing_state = 'previous'
            if event.type == pygame.KEYUP:
                self.pressing_state = None

    def run(self):
        while True:
            # handle events
            self.handle_events()
            self.update_display()

            if self.pressing_state == 'next':
                self.idx = (self.idx + 1) % len(self.df)
            if self.pressing_state == 'previous':
                self.idx = (self.idx - 1) % len(self.df)
            time.sleep(0.05)


if __name__ == '__main__':
    data_viewer = DatasetViewer()
    data_viewer.run()

