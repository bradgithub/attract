from Tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
import tkSimpleDialog
import re

SINGLE = "single"
DUAL = "dual"
COMPETITION = "competition"
TRUE = "1"
FALSE = "0"

class SetupPanel():
    def __init__(self, parent):
        self.parameters = {
            "trainingDataFilename": "",
            "saveDataFilename": "",
            "arousalQuery": "",
            "nonArousalQuery": "",
            "arousalGroupId": "",
            "nonArousalGroupId": "",
            "randomizeImages": "",
            "useGazeFractionFeature": "",
            "mode": ""
        }

        try:
            with open("parameters.csv", "rb") as parametersFile:
                for line in parametersFile:
                    match = re.match("^(?P<name>[^=]+)=(?P<value>.+)$", line)
                    if not (match is None):
                        parameterName = match.group("name").strip()
                        parameterValue = match.group("value").strip()
                        self.parameters[parameterName] = parameterValue
                        
        except Exception:
            pass

        buttonWidth = 20
        labelWidth = 25
        entryWidth = 30

        framePadx =  "3m"
        framePady =  "2m"
        frameIpadx = "0m"
        frameIpady = "0m"

        container = Frame(parent)
        container.pack(
            ipadx=frameIpadx,
            ipady=frameIpady,
            padx=framePadx,
            pady=framePady)    

        def setTrainingDataFile():
            self.parameters["trainingDataFilename"] = askopenfilename(title="Open training data file",
                                                        filetypes=(("CSV files","*.csv"),("all files","*.*")))
            if not (self.parameters["trainingDataFilename"] is None) and len(self.parameters["trainingDataFilename"]) > 0:
                labelTrainingData["text"] = self.parameters["trainingDataFilename"]
            else:
                labelTrainingData["text"] = ""

        def setResponseDataFile():
            self.parameters["saveDataFilename"] = asksaveasfilename(title="Save response data file",
                                                      filetypes=(("CSV files","*.csv"),("all files","*.*")))
            if not (self.parameters["saveDataFilename"] is None) and len(self.parameters["saveDataFilename"]) > 0:
                labelResponseData["text"] = self.parameters["saveDataFilename"]
            else:
                labelResponseData["text"] = ""

        def setParameters():
            self.parameters["trainingDataFilename"] = labelTrainingData["text"]
            self.parameters["saveDataFilename"] = labelResponseData["text"]
            self.parameters["arousalQuery"] = entryPositiveQuery.get()
            self.parameters["nonArousalQuery"] = entryNegativeQuery.get()
            self.parameters["arousalGroupId"] = entryPositiveGroupId.get()
            self.parameters["nonArousalGroupId"] = entryNegativeGroupId.get()
            self.parameters["randomizeImages"] = randomizeValue.get()
            self.parameters["useGazeFractionFeature"] = gazeFractionValue.get()
            
        def saveParameters():
            with open("parameters.csv", "wb") as parametersFile:
                lines = []
                for parameterName in self.parameters:
                    parameterValue = self.parameters[parameterName]
                    line = [ parameterName, str(parameterValue) ]
                    line = " = ".join(line)
                    lines.append(line)
                lines = "\n".join(lines) + "\n"
                parametersFile.write(lines)

        def startSingleMode():
            setParameters()
            self.parameters["mode"] = SINGLE
            saveParameters()
            
            parent.destroy()

        def startDualMode():
            setParameters()
            self.parameters["mode"] = DUAL
            saveParameters()
            
            parent.destroy()

        def startCompetitionMode():
            setParameters()
            self.parameters["mode"] = COMPETITION
            saveParameters()
            
            parent.destroy()

        buttonTrainingData = Button(container)
        buttonTrainingData["command"] = setTrainingDataFile
        buttonTrainingData["width"] = buttonWidth
        buttonTrainingData["text"]= "Set Training Data File" 
        buttonTrainingData.grid(row=0, column=0, sticky=W)

        labelTrainingData = Label(container)
        labelTrainingData["text"] = self.parameters["trainingDataFilename"]
        labelTrainingData.grid(row=0, column=1)


        buttonResponseData = Button(container)
        buttonResponseData["command"] = setResponseDataFile
        buttonResponseData["width"] = buttonWidth
        buttonResponseData["text"]= "Set Response Data File" 
        buttonResponseData.grid(row=1, column=0, sticky=W)

        labelResponseData = Label(container)
        labelResponseData["text"] = self.parameters["saveDataFilename"]
        labelResponseData.grid(row=1, column=1, sticky=W)


        labelPositiveQuery = Label(container)
        labelPositiveQuery["text"] = "Arousal/right image/king-of-the-hill Flickr query and Group ID:"
        labelPositiveQuery["anchor"] = W
        labelPositiveQuery.grid(row=2, column=0, sticky=W)

        entryPositiveQuery = Entry(container)
        entryPositiveQuery["width"] = entryWidth
        entryPositiveQuery["text"] = self.parameters["arousalQuery"]
        entryPositiveQuery.grid(row=2, column=1, sticky=W)

        entryPositiveGroupId = Entry(container)
        entryPositiveGroupId["width"] = int(entryWidth / 4.0)
        entryPositiveGroupId["text"] = self.parameters["arousalGroupId"]
        entryPositiveGroupId.grid(row=2, column=2, sticky=W)


        labelNegativeQuery = Label(container)
        labelNegativeQuery["text"] = "Non-arousal/left image Flickr query and Group ID:"
        labelNegativeQuery["anchor"] = W
        labelNegativeQuery.grid(row=3, column=0, sticky=W)

        entryNegativeQuery = Entry(container)
        entryNegativeQuery["width"] = entryWidth
        entryNegativeQuery["text"] = self.parameters["nonArousalQuery"]
        entryNegativeQuery.grid(row=3, column=1, sticky=W)

        entryNegativeGroupId = Entry(container)
        entryNegativeGroupId["width"] = int(entryWidth / 4.0)
        entryNegativeGroupId["text"] = self.parameters["nonArousalGroupId"]
        entryNegativeGroupId.grid(row=3, column=2, sticky=W)
        

        labelRandomize = Label(container)
        labelRandomize["text"] = "Randomize images:"
        labelRandomize["anchor"] = W
        labelRandomize.grid(row=4, column=0, sticky=W)
        
        randomizeValue = IntVar()
        if self.parameters["randomizeImages"] == "1":
            randomizeValue.set(1)
        else:
            randomizeValue.set(0)
        entryRandomize = Checkbutton(container, onvalue=1, offvalue=0, variable=randomizeValue)
        entryRandomize.grid(row=4, column=1, sticky=W)

        
        labelGazeFractionFeature = Label(container)
        labelGazeFractionFeature["text"] = "Use gaze fraction as feature:"
        labelGazeFractionFeature["anchor"] = W
        labelGazeFractionFeature.grid(row=5, column=0, sticky=W)
        
        gazeFractionValue = IntVar()
        if self.parameters["useGazeFractionFeature"] == "1":
            gazeFractionValue.set(1)
        else:
            gazeFractionValue.set(0)
        entryGazeFractionFeature = Checkbutton(container, onvalue=1, offvalue=0, variable=randomizeValue)
        entryGazeFractionFeature.grid(row=5, column=1, sticky=W)

        
        buttonStartSingleMode = Button(container)
        buttonStartSingleMode["command"] = startSingleMode
        buttonStartSingleMode["width"] = buttonWidth
        buttonStartSingleMode["text"]= "Start sequential mode" 
        buttonStartSingleMode.grid(row=6, column=0)
        
        buttonStartDualMode = Button(container)
        buttonStartDualMode["command"] = startDualMode
        buttonStartDualMode["width"] = buttonWidth
        buttonStartDualMode["text"]= "Start parallel mode" 
        buttonStartDualMode.grid(row=6, column=1)
        
        buttonStartCompetitionMode = Button(container)
        buttonStartCompetitionMode["command"] = startCompetitionMode
        buttonStartCompetitionMode["width"] = buttonWidth
        buttonStartCompetitionMode["text"]= "Start competition mode" 
        buttonStartCompetitionMode.grid(row=6, column=2)
        
if __name__ == "__main__":
    root = Tk()
    root.title("Arousal Predictor")
    setupPanel = SetupPanel(root)
    root.lift()
    root.wm_attributes("-topmost", 1)
    root.focus_force()
    root.mainloop()
    print(setupPanel.parameters)
