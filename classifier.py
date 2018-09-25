import time
import csv
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier

from recurrence_quantification_analysis import RecurrenceQuantificationAnalysis

class Classifier:
    def __init__(self,
                 trainingData,
                 screenWidth,
                 screenHeight,
                 useDualMode,
                 verificationTrials = 10,
                 recurrenceRadiusScreenFraction = 0.1,
                 mostVisitedAreaRadiusScreenFraction = 0.2,
                 useGazeFractionFeature = False,
                 infoCallback = None):
        halfScreenWidth = int(screenWidth / 2.0)
        recurrenceRadius = screenWidth * float(recurrenceRadiusScreenFraction)
        mostVisitedAreaRadius = screenWidth * float(mostVisitedAreaRadiusScreenFraction)
        
        trainX = []
        trainy = []
        gbc = None
        
        def log(message):
            if not (infoCallback is None):
                infoCallback(message)
            
        def getSingleModeFeatures(xyPoints):
            return RecurrenceQuantificationAnalysis(xyPoints, recurrenceRadius, mostVisitedAreaRadius).getFeatures()
    
        def getDualModeFeatures(xyPoints):
            xyPointsL = []
            xyPointsR = []
            for x, y in xyPoints:
                if x < halfScreenWidth:
                    xyPointsL.append(( x, y ))
                else:
                    xyPointsR.append(( x, y ))
                    
            leftPointsCount = len(xyPointsL)
            rightPointsCount = len(xyPointsR)
                        
            featuresL = getSingleModeFeatures(xyPointsL)
            featuresR = getSingleModeFeatures(xyPointsR)

            features = []
            if useGazeFractionFeature:
                features.append(leftPointsCount / float(leftPointsCount + rightPointsCount))
            for feature in featuresL:
                features.append(feature)
            for feature in featuresR:
                features.append(feature)
                
            featureSetA = features
            
            features = []
            if useGazeFractionFeature:
                features.append(leftPointsCount / float(leftPointsCount + rightPointsCount))
            for feature in featuresR:
                features.append(feature)
            for feature in featuresL:
                features.append(feature)
                
            featureSetB = features
            
            return [ featureSetA, featureSetB ]
    
        def getPixel(value, extent):
            intValue = int(value)
            floatValue = float(value)
            
            if not (floatValue == intValue) or (floatValue > 0.0 and floatValue < 1.0) or value.find(".") > -1:
                return int(floatValue * extent)

            else:
                return intValue
        
        def parseTrainingData():
            lastId = None
            lastRecord = None
            
            recordsX = []
            recordsy = []
            
            for record in trainingData:
                classId = int(record[0])
                recordId = int(record[1])
                timeStamp = float(record[2])
                x = getPixel(record[3], screenWidth)
                y = getPixel(record[4], screenHeight)

                if lastId == recordId:
                    lastRecord.append((x, y))
                    
                else:
                    lastId = recordId
                    lastRecord = [ (x, y) ]
                    
                    if classId == 1:
                        recordsX.append(lastRecord)
                        recordsy.append(1)
                        
                    elif classId == 0:
                        recordsX.append(lastRecord)
                        recordsy.append(0)

            i = 0
            while i < len(recordsX):
                if useDualMode:
                    featureSet = getDualModeFeatures(recordsX[i])
                    
                    trainX.append(featureSet[0])
                    trainX.append(featureSet[1])
                    
                    trainy.append(recordsy[i])
                    trainy.append(1 - recordsy[i])
                    
                else:
                    features = getSingleModeFeatures(recordsX[i])
                    
                    trainX.append(features)
                    trainy.append(recordsy[i])
                    
                i = i + 1
                        
        def verify():
            totalPositiveCorrect = 0
            totalPositiveExamples = 0
            totalNegativeCorrect = 0
            totalNegativeExamples = 0
            
            for trialId in np.arange(verificationTrials):
                indices = np.arange(len(trainX))
                np.random.shuffle(indices)

                trainX_ = []
                trainy_ = []

                i = 0
                while i < int(len(trainX) * 0.8):
                    trainX_.append(trainX[indices[i]])
                    trainy_.append(trainy[indices[i]])
                    
                    i = i + 1
                
                gbc = GradientBoostingClassifier()
                gbc.fit(trainX_, trainy_)

                testX = []

                j = i
                while j < len(trainX):
                    testX.append(trainX[indices[j]])
                    
                    j = j + 1
                    
                predictions = gbc.predict(testX)
                
                positiveExamples = 0
                positiveCorrect = 0
                negativeExamples = 0
                negativeCorrect = 0
                
                j = i
                while j < len(trainX):
                    predictionClass = predictions[j - i]
                    correctClass = trainy[indices[j]]
                    
                    if correctClass == 0:
                        negativeExamples = negativeExamples + 1
                        
                        if predictionClass == 0:
                            negativeCorrect = negativeCorrect + 1
                            
                    else:
                        positiveExamples = positiveExamples + 1
                        
                        if predictionClass == 1:
                            positiveCorrect = positiveCorrect + 1
                            
                    j = j + 1
                    
                totalPositiveCorrect = totalPositiveCorrect + positiveCorrect
                totalPositiveExamples = totalPositiveExamples + positiveExamples
                totalNegativeCorrect = totalNegativeCorrect + negativeCorrect
                totalNegativeExamples = totalNegativeExamples + negativeExamples
                
                log("Validation Trial %i: %i / %i correct positives (%f), %i / %i correct negatives (%f), %i / %i correct overall (%f)" % (
                    trialId + 1,
                    positiveCorrect, positiveExamples,float(positiveCorrect) / positiveExamples,
                    negativeCorrect, negativeExamples, float(negativeCorrect) / negativeExamples,
                    positiveCorrect + negativeCorrect, positiveExamples + negativeExamples,
                    float(positiveCorrect + negativeCorrect) / (positiveExamples + negativeExamples)))

            log("Validation Total: %i / %i correct positives (%f), %i / %i correct negatives (%f), %i / %i correct overall (%f)" % (
                totalPositiveCorrect, totalPositiveExamples,float(totalPositiveCorrect) / totalPositiveExamples,
                totalNegativeCorrect, totalNegativeExamples, float(totalNegativeCorrect) / totalNegativeExamples,
                totalPositiveCorrect + totalNegativeCorrect, totalPositiveExamples + totalNegativeExamples,
                float(totalPositiveCorrect + totalNegativeCorrect) / (totalPositiveExamples + totalNegativeExamples)))
        
        log("Parsing training data")

        parseTrainingData()

        log("Verifying training data")
        
        verify()

        log("Finalizing classifier")
        
        gbc = GradientBoostingClassifier()
        gbc.fit(trainX, trainy)

        log("Classifier ready")
        
        def classify(records):
            xyPoints = []
            
            for record in records:
                xyPoints.append(( record[0] * screenWidth, record[1] * screenHeight ))
                
            features = None
            
            if useDualMode:
                features = getDualModeFeatures(xyPoints)
                
            else:
                features = getSingleModeFeatures(xyPoints)
            
            return gbc.predict([ features ])[0]
        
        self.classify = classify
        
    def createRecord(self,
                     xPercentage,
                     yPercentage):
        return (
            float(xPercentage),
            float(yPercentage),
            time.time()
        )
    
    def compileRecords(self,
                       classId,
                       recordId,
                       records):
        classId = str(classId)
        recordId = str(recordId)

        output = []

        for record in records:
           output.append((
               classId,
               recordId,
               str(record[2]),
               str(record[0]),
               str(record[1])
            ))
           
        return output

if __name__ == "__main__":
    def log(message):
        print(message)

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
