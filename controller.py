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
            
        def imageLoader():
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
            
            imageLoader = FlickrImageLoader(searchQueries,
                                            groupIds,
                                            randomize,
                                            maxImagesPerCategory,
                                            log)
        
