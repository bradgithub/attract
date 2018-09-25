import time
from collections import deque
from threading import Lock, Event
from classifier import Records

class SampleHandler:
    def __init__(self,
                 smoothingWindowLength=5,
                 smoothingFactor=10.0):
        self.lock = Lock()
        self.gazePoint = None
                
        xySmoothingWindow = deque()
        records = Records()
        
        def handle(sample)
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
                  
                    with self.lock:
                        self.gazePoint = (x, y)

                else:
                    xySmoothingWindow.clear()

                    with self.lock:
                        self.gazePoint = None
                    
            else:
                xySmoothingWindow.clear()

                with self.lock:
                    self.gazePoint = None
                
        def 
# after handle, check records count and if full, don't log anymore and set a flag for main thread to log and clear/restart logging
