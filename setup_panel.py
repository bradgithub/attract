from Tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
import tkSimpleDialog

class SetupPanel():
    def __init__(self, parent):
        self.trainingDataFilename = ""
        self.saveDataFilename = ""
        self.arousalQuery = ""
        self.nonArousalQuery = ""
        self.mode = "single"

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
            self.trainingDataFilename = askopenfilename(title="Open training data file",
                                                        filetypes=(("CSV files","*.csv"),("all files","*.*")))
            if not (self.trainingDataFilename is None):
                labelTrainingData["text"] = self.trainingDataFilename
            else:
                labelTrainingData["text"] = ""

        def setResponseDataFile():
            self.saveDataFilename = asksaveasfilename(title="Save response data file",
                                                      filetypes=(("CSV files","*.csv"),("all files","*.*")))
            if not (self.saveDataFilename is None):
                labelResponseData["text"] = self.saveDataFilename
            else:
                labelResponseData["text"] = ""

        def setArousalQuery():
            self.arousalQuery = entryPositiveQuery.get()

            return True

        def setNonArousalQuery():
            self.nonArousalQuery = entryNegativeQuery.get()

            return True
        
        def startSingleMode():
            self.mode = "single"
            
            parent.destroy()

        def startDualMode():
            self.mode = "dual"
            
            parent.destroy()

        buttonTrainingData = Button(container)
        buttonTrainingData["command"] = setTrainingDataFile
        buttonTrainingData["width"] = buttonWidth
        buttonTrainingData["text"]= "Set Training Data File" 
        buttonTrainingData.grid(row=0, column=0, sticky=W)

        labelTrainingData = Label(container)
        labelTrainingData.grid(row=0, column=1)

        buttonResponseData = Button(container)
        buttonResponseData["command"] = setResponseDataFile
        buttonResponseData["width"] = buttonWidth
        buttonResponseData["text"]= "Set Response Data File" 
        buttonResponseData.grid(row=1, column=0, sticky=W)

        labelResponseData = Label(container)
        labelResponseData.grid(row=1, column=1, sticky=W)

        labelPositiveQuery = Label(container)
        labelPositiveQuery["text"] = "Arousal Pixabay query:"
        labelPositiveQuery["anchor"] = W
        labelPositiveQuery.grid(row=2, column=0, sticky=W)

        entryPositiveQuery = Entry(container)
        entryPositiveQuery["validate"] = ALL
        entryPositiveQuery["validatecommand"] = setArousalQuery
        entryPositiveQuery["width"] = entryWidth
        entryPositiveQuery.grid(row=2, column=1, sticky=W)

        labelNegativeQuery = Label(container)
        labelNegativeQuery["text"] = "Non-arousal Pixabay query:"
        labelNegativeQuery["anchor"] = W
        labelNegativeQuery.grid(row=3, column=0, sticky=W)

        entryNegativeQuery = Entry(container)
        entryNegativeQuery["validate"] = ALL
        entryNegativeQuery["validatecommand"] = setNonArousalQuery
        entryNegativeQuery["width"] = entryWidth
        entryNegativeQuery.grid(row=3, column=1, sticky=W)

        buttonStartSingleMode = Button(container)
        buttonStartSingleMode["command"] = startSingleMode
        buttonStartSingleMode["width"] = buttonWidth
        buttonStartSingleMode["text"]= "Start sequential task" 
        buttonStartSingleMode.grid(row=4, column=0)
        
        buttonStartDualMode = Button(container)
        buttonStartDualMode["command"] = startDualMode
        buttonStartDualMode["width"] = buttonWidth
        buttonStartDualMode["text"]= "Start parallel task" 
        buttonStartDualMode.grid(row=4, column=1)
