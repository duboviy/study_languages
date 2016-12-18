# need to install python-opencv, pygame, numpy, scipy, PIL
import sys

import pygame
from pygame.locals import QUIT, KEYDOWN

import opencv
#this is important for capturing/displaying images
from opencv import highgui


def get_image(camera):
    img = highgui.cvQueryFrame(camera)
    # Add the line below if you need it (Ubuntu 8.04+)
    # im = opencv.cvGetMat(im)
    # convert Ipl image to PIL image
    return opencv.adaptors.Ipl2PIL(img)


def render_flipped_camera():
    camera = highgui.cvCreateCameraCapture(0)

    fps = 30.0
    pygame.init()
    pygame.display.set_mode((640, 480))
    pygame.display.set_caption("WebCam Demo")
    screen = pygame.display.get_surface()

    while True:
        events = pygame.event.get()

        for event in events:
            if event.type == QUIT or event.type == KEYDOWN:
                sys.exit(0)

        im = get_image(camera)
        pg_img = pygame.image.frombuffer(im.tostring(), im.size, im.mode)
        screen.blit(pg_img, (0, 0))
        pygame.display.flip()
        pygame.time.delay(int(1000 * 1.0/fps))


if __name__ == "__main__":
    render_flipped_camera()
