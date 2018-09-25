import pygame
from Tkinter import Tk
from setup_panel import SetupPanel, SINGLE, DUAL, COMPETITION
from flickr_image_loader import FlickrImageLoader
from recurrence_quantification_analysis import RecurrenceQuantificationAnalysis

class Controller:
    def __init__(self):
        def log(message):
            print(message)
        
        def getParameters():
            root = Tk()
            root.title("Arousal Predictor")
            
            setupPanel = SetupPanel(root)
            
            root.lift()
            root.wm_attributes("-topmost", 1)
            root.focus_force()
            root.mainloop()

            self.parameters = setupPanel.parameters
            
            log(parameters)
            
        def getImageLoader():
            searchQueries = [
                self.parameters["arousalQuery"]
            ]
            
            groupIds = [
                None
            ]
            
            if len(self.parameters["arousalGroupId"]) > 0:
                groupIds[0] = self.parameters["arousalGroupId"]
            
            if self.parameters.mode == SINGLE or self.parameters.mode == DUAL:
                searchQueries.append(self.parameters["nonArousalQuery"])
                groupIds.append(None)
                if len(self.parameters["nonArousalGroupId"]) > 0:
                    groupIds[1] = self.parameters["nonArousalGroupId"]
            
            randomize = True
            if self.parameters["randomizeImages"] == 0:
                randomize = False
                
            maxImagesPerCategory = self.parameters["randomizeImages"]
            
            self.imageLoader = FlickrImageLoader(searchQueries,
                                            groupIds,
                                            randomize,
                                            maxImagesPerCategory,
                                            log)
        
        def getSounds():
            soundLengthSeconds = 2
            audioSampleFrequency = 11025

            sounds = []
            amplitude = 4096.0
            tmp = np.zeros((length, 2), dtype = np.int16)
            sampleLength = int(audioSampleFrequency * soundLengthSeconds)

            pygame.mixer.init(audioSampleFrequency, -16, 2)
            
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
            trainingDataFile = open("dual1.csv", "rb")
            reader = csv.reader(trainingDataFile,
                                delimiter=",", quoting=csv.QUOTE_NONE)
            records = []
            for row, record in enumerate(reader):
                records.append(record)

            trainingDataFile.close()
                                
            c = Classifier(records,
                            1080,
                            1920,
                            True,
                            infoCallback=log)
            
