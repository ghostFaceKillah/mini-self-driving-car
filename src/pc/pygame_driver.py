import cv2
import multiprocessing
import numpy as np
import pygame

import lib.constant as cnst
import lib.log as log
import lib.state as state


class PygameDriver(multiprocessing.Process):
    """
    Process that handles the pygame window update
    and keyboard events. Writes them to state.

    1) on keyboard event, update state
    2) update pygame screen at set frequency based on state

    """
    def __init__(self, the_state):
        super(PygameDriver, self).__init__()

        self.logger = log.get(__name__)
        self.logger.info("Initializing...")

        self.state = the_state

        self.logger.info("Done.")

    def connect(self):
        """ Connect to RasPi in case we use TCP """
        self.logger.info('Connecting to steering server...')
        self.logger.info('Done')

    def toggle_recording_state(self):
        """
        In our multiprocessing-resistant state we have a variable
        that indicates if we are recording.
        """
        if self.state.recording:
            self.state.recording = False
            self.logger.info("Recording off.")
        else:
            self.state.recording = True
            self.logger.info("Recording on.")

    def keydown(self, event):
        """ Handle pressing key down """
        if event.key == pygame.K_UP:
            self.state.vertical = state.Vertical.up
        if event.key == pygame.K_DOWN:
            self.state.vertical = state.Vertical.down
        if event.key == pygame.K_RIGHT:
            self.state.horizontal = state.Horizontal.right
        if event.key == pygame.K_LEFT:
            self.state.horizontal = state.Horizontal.left
        if event.key == pygame.K_r:
            self.toggle_recording_state()


    def keyup(self, event):
        """ Handle key release """
        if event.key in [pygame.K_UP, pygame.K_DOWN]:
            self.state.vertical = state.Vertical.nothing
        if event.key in [pygame.K_RIGHT, pygame.K_LEFT]:
            self.state.horizontal = state.Horizontal.nothing

    def handle_key_events(self):
        """ Wrapper for handling key events """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state.done = True
                return
            if event.type == pygame.KEYDOWN:
                self.keydown(event)
            if event.type == pygame.KEYUP:
                self.keyup(event)

    def put_info_text_on_image(self, img):
        txt = "recording..."
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

    def display_image(self):
        """ Handles whole image displaying process """
        img = self.state.image
        recording = self.state.recording
        if img is not None:

            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = cv2.resize(
                img,
                cnst.DISPLAY_VIDEO_RESOLUITION,
                interpolation=cv2.INTER_CUBIC
            )

            if recording:
                img = self.put_info_text_on_image(img)

            img = np.transpose(img, axes=(1, 0, 2))

            self.screen.blit(pygame.surfarray.make_surface(img), (0, 0))
            pygame.display.flip()

    def run(self):
        """ Main function of this object """
        pygame.init()
        self.screen = pygame.display.set_mode(cnst.DISPLAY_VIDEO_RESOLUITION)
        self.connect()
        while True:
            self.handle_key_events()
            if self.state.done:
                print('exiting PyGame thread')
                pygame.display.quit()
                pygame.quit()
                return
            self.display_image()
