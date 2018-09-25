import pygame
from Tkinter import Tk
from threading import Thread
import numpy as np
import math
import csv

from setup_panel import SetupPanel, SINGLE, DUAL, COMPETITION
from flickr_image_loader import FlickrImageLoader
from classifier import Classifier
from display import Display

class Controller:
    def __init__(self):
        def getParameters():
            root = Tk()
            root.title("Arousal Predictor")
            
            setupPanel = SetupPanel(root)
            
            root.lift()
            root.wm_attributes("-topmost", 1)
            root.focus_force()
            root.mainloop()

            self.parameters = setupPanel.parameters
            
        def getImageLoader():
            searchQueries = [
                self.parameters["arousalQuery"]
            ]
            
            groupIds = [
                None
            ]
            
            if len(self.parameters["arousalGroupId"]) > 0:
                groupIds[0] = self.parameters["arousalGroupId"]
            
            if self.parameters["mode"] == SINGLE or self.parameters["mode"] == DUAL:
                searchQueries.append(self.parameters["nonArousalQuery"])
                groupIds.append(None)
                if len(self.parameters["nonArousalGroupId"]) > 0:
                    groupIds[1] = self.parameters["nonArousalGroupId"]
            
            randomize = True
            if self.parameters["randomizeImages"] == 0:
                randomize = False
                
            maxImagesPerCategory = self.parameters["maxImagesPerCategory"]
            
            log("Starting image loader...")
            
            self.imageLoader = FlickrImageLoader(searchQueries,
                                                 groupIds,
                                                 randomize,
                                                 maxImagesPerCategory,
                                                 log)
        
        def getSounds():
            log("Creating sounds...")

            soundLengthSeconds = 2
            audioSampleFrequency = 11025

            amplitude = 4096.0
            sampleLength = int(audioSampleFrequency * soundLengthSeconds)
            
            tmp = np.zeros((sampleLength, 2), dtype = np.int16)

            pygame.mixer.init(audioSampleFrequency, -16, 2)
            
            sounds = []
            
            for toneFrequency in [ 440.00, 523.25 ]:
                x = 0
                while x < sampleLength:
                    value = amplitude * np.sin(x * toneFrequency / audioSampleFrequency * 2 * math.pi)
           
                    tmp[x][0] = value
                    tmp[x][1] = value
                    
                    x = x + 1
                
                sound = pygame.sndarray.array(tmp)
                sound = pygame.sndarray.make_sound(sound)
                sounds.append(sound)
            
            return sounds

        def getClassifier():
            if not (self.parameters["trainingDataFilename"] is None) and len(self.parameters["trainingDataFilename"]) > 0:
                log("Loading training data file " + self.parameters["trainingDataFilename"])
                
                trainingDataFile = open(self.parameters["trainingDataFilename"], "rb")
                reader = csv.reader(trainingDataFile,
                                    delimiter=",", quoting=csv.QUOTE_NONE)
                records = []
                for row, record in enumerate(reader):
                    records.append(record)

                trainingDataFile.close()
                                    
                useDualMode = self.parameters["mode"] == DUAL
                
                log("Loading and verifying classifier...")
                
                self.classifier = Classifier(records,
                                             screenWidth,
                                             screenHeight,
                                             useDualMode,
                                             infoCallback=log)
            
        def setup():
            getSounds()
            
            getClassifier()
            
            getImageLoader()

        getParameters()
        
        display = Display()
        
        log = display.log
        screenWidth = display.screenWidth
        screenHeight = display.screenHeight
        
        setupThread = Thread(target=setup,
                             name="Setup thread",
                             args=[])
        setupThread.daemon = True
        setupThread.start()

        display.mainloop()

if __name__ == "__main__":
    Controller()
