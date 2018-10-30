import time
import numpy as np
from collections import deque
from threading import Lock

from classifier import Records

class SampleHandler:
    def __init__(self,
                 requiredRecordsCount,
                 smoothingWindowLength=5,
                 smoothingFactor=10.0):
        lock = Lock()
        gazePoint = [ None ]
        readyToRecord = [ False ]
        xySmoothingWindow = deque()
        records = Records()
        
        def handleSample(sample):
            with lock:
                if readyToRecord[0]:
                    if sample["LPOGV"] == "1" and sample["RPOGV"] == "1" and sample["LPV"] == "1" and sample["RPV"] == "1":
                        xl = float(sample["LPOGX"])
                        yl = float(sample["LPOGY"])
                        
                        xr = float(sample["RPOGX"])
                        yr = float(sample["RPOGY"])
                        
                        if xl >= 0 and xl <= 1 and yl >= 0 and yl <= 1 and xr >= 0 and xr <= 1 and yr >= 0 and yr <= 1:
                            x = (xl + xr) / 2.0
                            y = (yr + yr) / 2.0
                            
                            records.append(x, y)
                
                            if len(xySmoothingWindow) == smoothingWindowLength:
                                xMean, yMean = np.mean(xySmoothingWindow, 0)
                                xLim, yLim = np.std(xySmoothingWindow, 0) * smoothingFactor
                                xySmoothingWindow.popleft()
                                
                                if x < xMean - xLim or x > xMean + xLim or y < yMean - yLim or y > yMean + yLim:
                                    xySmoothingWindow.clear()
                                    
                            xySmoothingWindow.append((x, y))
                            x, y = np.mean(xySmoothingWindow, 0)
                            
                            gazePoint[0] = (x, y)

                        else:
                            xySmoothingWindow.clear()
                            gazePoint[0] = None
                            
                    else:
                        xySmoothingWindow.clear()
                        gazePoint[0] = None
                            
                    if isRecordsFull():
                        xySmoothingWindow.clear()
                        gazePoint[0] = None
                        readyToRecord[0] = False

        def isRecordsFull():
            return records.count() == requiredRecordsCount

        def saveRecords(classId,
                        data,
                        outputFilename):
            records.save(classId, data, outputFilename)
        
        def getData():
            with lock:
                data = [ None, gazePoint[0] ]
                
                if isRecordsFull():
                    data[0] = records.get()
                    records.clear()
                
                return data
       
        def stopLogging():
            with lock:
                records.clear()
                xySmoothingWindow.clear()
                gazePoint[0] = None
                readyToRecord[0] = False
       
        def pauseLogging():
            with lock:
                xySmoothingWindow.clear()
                gazePoint[0] = None
                readyToRecord[0] = False
       
        def startLogging():
            with lock:
                records.clear()
                xySmoothingWindow.clear()
                gazePoint[0] = None
                readyToRecord[0] = True

        def getFakeSample():
            x, y = np.random.normal() * 0.1 + 0.25, np.random.normal() * 0.1 + 0.5
            
            if np.random.random() < 0.55:
                x = x + 0.5
            
            sample_ = {
                "LPOGV": "1",
                "RPOGV": "1",
                "LPV": "1",
                "RPV": "1",
                "LPOGX": x,
                "LPOGY": y,
                "RPOGX": x,
                "RPOGY": y
                
            }
            
            return sample_

        self.handleSample = handleSample
        self.saveRecords = saveRecords
        self.getData = getData
        self.stopLogging = stopLogging
        self.pauseLogging = pauseLogging
        self.startLogging = startLogging
        self.getFakeSample = getFakeSample
