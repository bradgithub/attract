import io
import sys
import math
import json
import time
import urllib
import pygame
import numpy as np
from threading import Lock, Thread
from os import listdir
from os.path import isfile, join

class LocalImageLoader:
    def __init__(self,
                 imagePaths,
                 randomize,
                 infoCallback):
        if imagePaths is None or len(imagePaths) == 0:
            return
        
        images = []
        lastImageChoices = []
        lock = Lock()
        
        validExtensions = (
            "jpg",
            "jpeg",
            "png",
            "gif",
            "bmp",
            "pcx",
            "tga",
            "tif",
            "tiff",
            "lbm",
            "pbm"
            "pgm",
            "ppm",
            "xpm"
        )
        
        for i in range(len(imagePaths)):
            images.append([])
            lastImageChoices.append(None)
                
        def log(message):
            if not (infoCallback is None):
                infoCallback(message)
        
        def getImageFilenames(imagePath):
            filenames = []
            
            try:
                for filename in listdir(imagePath):
                    filename = join(imagePath, filename)
                    
                    if isfile(filename):
                        if filename.lower().endswith(validExtensions):
                            filenames.append(filename)
                        
                if randomize:
                    np.random.shuffle(filenames)
                        
                log("Found " + str(len(filenames)) + " possible image files in directory " + str(imagePath))
                        
                return filenames
            
            except Exception:
                log("Could not access directory " + str(imagePath))
                        
                return []

        def loadImageFilename(filename):
            try:
                with open(filename, "r") as f:
                    image = f.read()
                    image = io.BytesIO(image)
                    return pygame.image.load(image)
            except Exception:
                return None
        
        def loader():
            imagesToLoad= []
            classId = 0
            for imagePath in imagePaths:
                filenames = getImageFilenames(imagePath)
                
                count = 0
                for filename in filenames:
                    imagesToLoad.append([ count, classId, filename])
                    count = count + 1
                classId = classId + 1
                
            log("Retrieving images")
            
            imagesToLoad.sort(key=lambda x: (x[0], x[1]))
            for imageToLoad in imagesToLoad:
                filename = imageToLoad[2]
                image = loadImageFilename(filename)
                if not (image is None):
                    log("Retrieved class " + str(imageToLoad[1]) + " image filename " + filename)
                    with lock:
                        images[imageToLoad[1]].append(image)

        loaderThread = Thread(target=loader,
                              name="Image loader thread",
                              args=[])
        loaderThread.daemon = True
        loaderThread.start()

        def getImage(classId,
                     width,
                     height):
            image = None
            
            with lock:
                try:
                    _images = images[classId]
                    imageIds = range(len(_images))
                    np.random.shuffle(imageIds)
                    imageId = None
                    for imageId in imageIds:
                        if len(imageIds) == 1 or not (imageId == lastImageChoices[classId]):
                            break
                    lastImageChoices[classId] = imageId
                    if not (imageId is None):
                        image = _images[imageId]
                        if not (width == image.get_width()) or not (height == image.get_height()):
                            imageAspect = float(image.get_width()) / float(image.get_height())
                            newWidth = imageAspect * height
                            newHeight = width / imageAspect
                            if newWidth > width:
                                newWidth = width
                            elif newHeight > height:
                                newHeight = height
                            image = pygame.transform.smoothscale(image, (int(newWidth), int(newHeight)))
                            _images[imageId] = image
                            
                except Exception:
                    image = None

            return image
        
        self.getImage = getImage
            
if __name__ == "__main__":
    def log(message):
        print(message)
                
    loader = LocalImageLoader([
        "/tmp/aaa",
        "/tmp/bbb"
    ], True, log)

    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    height = screen.get_height()
    width = screen.get_width()

    count = 0
    while True:
        if count % 30 == 0:
            screen.fill((0, 0, 0))
            imageA = loader.getImage(0, 400,600)
            imageB = loader.getImage(1, 400,600)
            imageAx = int(float(400 - imageA.get_width()) / 2.0)
            imageBx = int(float(400 - imageB.get_width()) / 2.0) + 400
            imageAy = int(float(600 - imageA.get_height()) / 2.0)
            imageBy = int(float(600 - imageB.get_height()) / 2.0)
            if not (imageA is None):
                screen.blit(imageA, (imageAx,imageAy))
            if not (imageB is None):
                screen.blit(imageB, (imageBx,imageBy))
            pygame.display.flip()
        count = count + 1
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("exiting...")
                    sys.exit(0)
                    
            elif event.type == pygame.QUIT:
                print("exiting...")
                sys.exit(0)
        
        #pygame.time.delay(100)
        time.sleep(0.100)
