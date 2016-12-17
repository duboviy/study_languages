import argparse


def take_selfie_using_pygame(image_filename):
    # to capture a screen from camera, need to install pygame
    import pygame
    import pygame.camera

    pygame.camera.init()

    #Camera detected or not
    if not pygame.camera.list_cameras():
        raise RuntimeError("No camera detected. Can't take a selfie")

    cam = pygame.camera.Camera("/dev/video0", (640, 480))
    cam.start()
    img = cam.get_image()
    pygame.image.save(img, image_filename)


def take_selfie_using_simple_cv(image_filename):
    # to capture a screen from camera
    # need to install python-opencv, pygame, numpy, scipy, simplecv
    from SimpleCV import Camera

    cam = Camera()
    img = cam.getImage()
    img.save(image_filename)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('image_file', help='The image you\'d like to label.')
    args = parser.parse_args()

    take_selfie = take_selfie_using_pygame
    take_selfie(args.image_filename)


if __name__ == "__main__":
    # run with params, for example:
    # >>> python capture_image.py selfie.jpg
    main()
