import time
from collections import deque
from classifier import Records

class SampleHandler:
    def __init__(self,
                 requiredRecordsCount,
                 smoothingWindowLength=5,
                 smoothingFactor=10.0):
        gazePoint = [ None ]
        recordsFull = [ False ]
        readyToRecord = [ False ]
                
        xySmoothingWindow = deque()
        records = Records()
        
        def handleSample(sample)
            if not readyToRecord[0]:
                return
            
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
                    
            if records.count() == requiredRecordsCount:
                gazePoint = [ None ]
                recordsFull[0] = True
                readyToRecord[0] = [ False ]

        def saveRecords(classId,
                        outputFilename):
            if recordsFull[0]:
                records.save(classId, outputFilename)
        
        def getRecords():
            if recordsFull[0]:
                return records.get()
                
            else:
                return None
            
        def isRecordsFull():
            return recordsFull[0]
       
        def getGazePoint():
            return gazePoint[0]
       
        def startLogging():
            recordsFull[0] = False
            records.clear()
            readyToRecord[0] = [ True ]

        self.handleSample = handleSample
        self.saveRecords = saveRecords
        self.getRecords = getRecords
        self.isRecordsFull = isRecordsFull
        self.getGazePoint = getGazePoint
        self.startLogging = startLogging
