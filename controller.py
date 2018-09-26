import sys
import math
import csv
import time
import pygame
import numpy as np
from Tkinter import Tk
from collections import deque
from threading import Thread, Lock, Semaphore

from setup_panel import SetupPanel, SINGLE, DUAL, COMPETITION
from flickr_image_loader import FlickrImageLoader
from classifier import Classifier
from display import Display
from sample_handler import SampleHandler
from opengaze import OpenGazeTracker

class Controller:
    def __init__(self):
        self.classId = None
        self.parameters = None
        self.sounds = None
        self.samplerHandler = None
        self.classifier = None
        self.imageLoader = None
        self.imageUpdateNeeded = True
        
        handleRecordsLock = Lock()
        handleRecordsSemaphore = Semaphore(0)
        handleRecordsDeque = deque()
        
        def getParameters():
            root = Tk()
            root.title("Arousal Predictor")
            
            setupPanel = SetupPanel(root)
            
            root.lift()
            root.wm_attributes("-topmost", 1)
            root.focus_force()
            root.mainloop()

            self.parameters = setupPanel.parameters
            
            if not (self.parameters["mode"] == SINGLE) and not (self.parameters["mode"] == DUAL):
                sys.exit(0)
            
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
            
            self.sounds = []
            
            for toneFrequency in [ 440.00, 523.25 ]:
                x = 0
                while x < sampleLength:
                    value = amplitude * np.sin(x * toneFrequency / audioSampleFrequency * 2 * math.pi)
           
                    tmp[x][0] = value
                    tmp[x][1] = value
                    
                    x = x + 1
                
                sound = pygame.sndarray.array(tmp)
                sound = pygame.sndarray.make_sound(sound)
                
                self.sounds.append(sound)

        def getClassifier():
            self.classifier = None
            
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
                
        def getSampleHandler():
            self.samplerHandler = SampleHandler(self.parameters["requiredSamplesPerTrial"])
        
            if False:
                def fakeSampler():
                    while True:
                        sample = self.samplerHandler.getFakeSample()
                        
                        self.samplerHandler.handleSample(sample)
                        
                        #pygame.time.delay(16)
                        time.sleep(0.016)
                        
                sampleThread = Thread(target=fakeSampler,
                                    name="Fake sampler thread",
                                    args=[])
                sampleThread.daemon = True
                sampleThread.start()
            
            else:
                gazeTracker = OpenGazeTracker(self.samplerHandler.handleSample)
                gazeTracker.start_recording()
            
        def requestImageUpdate():
            self.imageUpdateNeeded = True
        
        def handleRecords():
            while True:
                handleRecordsSemaphore.acquire()
                
                with handleRecordsLock:
                    records, classId = handleRecordsDeque.popleft()
            
                if not (self.classifier is None):
                    if self.classifier.classify(records) == 1:
                        if self.parameters["mode"] == SINGLE:
                            log("Prediction: arousal")
                        
                        else:
                            log("Prediction: right image")
                        
                        self.sounds[1].play()
                        
                    else:
                        if self.parameters["mode"] == SINGLE:
                            log("Prediction: non-arousal")
                        
                        else:
                            log("Prediction: left image")

                        self.sounds[0].play()
        
                self.samplerHandler.saveRecords(classId, records, self.parameters["saveDataFilename"])
                
        def updateTrial():
            records, gazePoint = self.samplerHandler.getData()
            
            if not (records is None):
                with handleRecordsLock:
                    handleRecordsDeque.append((records, self.classId))
                
                handleRecordsSemaphore.release()
                
                self.imageUpdateNeeded = True
                
            display.setGazePoint(gazePoint)
            
            if self.imageUpdateNeeded:
                self.classId = np.random.choice([ 0, 1 ])
                
                if self.parameters["mode"] == SINGLE:
                    image = None
                    if not (self.imageLoader is None):
                        image = self.imageLoader.getImage(self.classId, screenWidth, screenHeight)

                    if not (image is None):
                        self.imageUpdateNeeded = False
                
                        display.setImage(image)
                    
                        return True
                    
                else:
                    imageA = self.imageLoader.getImage(1 - self.classId, int(screenWidth / 3.0), int(screenHeight * 5.0 / 6.0))
                    imageB = self.imageLoader.getImage(self.classId, int(screenWidth / 3.0), int(screenHeight * 5.0 / 6.0))
                    
                    if not (imageA is None) and not (imageB is None):
                        self.imageUpdateNeeded = False
                
                        display.setImage(imageA, imageB)
                    
                        return True
            
            return False
            
        def setup():
            getSounds()
            
            getClassifier()
            
            getImageLoader()
            
        getParameters()
        
        getSampleHandler()
        
        display = Display()
        
        log = display.log
        screenWidth = display.screenWidth
        screenHeight = display.screenHeight
        
        setupThread = Thread(target=setup,
                             name="Setup thread",
                             args=[])
        setupThread.daemon = True
        setupThread.start()

        display.setUpdateTrial(updateTrial)
        display.setRequestImageUpdate(requestImageUpdate)
        display.setStartLogging(self.samplerHandler.startLogging)
        display.setStopLogging(self.samplerHandler.stopLogging)

        handleRecordsThread = Thread(target=handleRecords,
                                     name="Handle records thread",
                                     args=[])
        handleRecordsThread.daemon = True
        handleRecordsThread.start()
        
        display.mainloop()

if __name__ == "__main__":
    Controller()
