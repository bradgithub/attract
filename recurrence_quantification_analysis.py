import numpy as np

class RecurrenceQuantificationAnalysis:
    def __init__(self,
                 xyPoints,
                 recurrenceRadius=10,
                 mostVisitedAreaRadius=40,
                 minimumLineLength=2):
        self._N = len(xyPoints)
        self._recurrencePoints = []
        self._diagonalLineFrequency = {}
        self._verticalLineFrequency = {}
        self._horizontalLineFrequency = {}

        indexedXyPoints = self._indexXyPoints(xyPoints)
        self._setRecurrencePoints(indexedXyPoints, recurrenceRadius)
        self._setRecurrenceLineFrequencies(minimumLineLength)

        self._calculateRecurrenceCount()
        self._calculateRecurrenceRate()
        self._calculateDeterminism()
        self._calculateLaminarity()
        self._calculatePredictabilityTime()
        self._calculateTrappingTime()
        self._calculateDivergence()
        self._calculateEntropy()
        
        self._calculateMostVisitedArea(indexedXyPoints, mostVisitedAreaRadius)
        
        self._calculateGazePathLength(xyPoints)
                
    def getFeatures(self):
        return (
            self._recurrenceCount,
            self._recurrenceRate,
            self._determinism,
            self._laminarity,
            self._predictabilityTime,
            self._trappingTime,
            self._divergence,
            self._entropy,
            self._maxFixationTime,
            self._mostVisitedArea,
            self._gazePathLengthMean,
            self._gazePathLengthStdDev,
            self._centerOfRecurrenceMass
        )
        
    def _indexXyPoints(self,
                       xyPoints):
        index = 0
        indexedXyPoints = []
        for x, y in xyPoints:
            indexedXyPoints.append([ index, x, y ])
            index = index + 1
        return indexedXyPoints

    def _setRecurrencePoints(self,
                             indexedXyPoints,
                             radius):
        i = 0
        radius2 = radius * radius
        centerOfRecurrenceMass = 0
        indexedXyPoints.sort(key=lambda indexedXyPoint: indexedXyPoint[1])
        for indexa, xa, ya in indexedXyPoints:
            j = i + 1
            while j < self._N:
                indexb, xb, yb = indexedXyPoints[j]
                xDistance = xb - xa
                yDistance = yb - ya
                if xDistance <= radius:
                    if yDistance >= -radius and yDistance <= radius:
                        if xDistance * xDistance + yDistance * yDistance <= radius2:
                            self._recurrencePoints.append([ indexa, indexb, xa, ya, xb, yb ])
                            centerOfRecurrenceMass = centerOfRecurrenceMass + j - i
                else:
                    break
                j = j + 1
            i = i + 1
        self._centerOfRecurrenceMass = float(centerOfRecurrenceMass) / (self._N - 1) / len(self._recurrencePoints)

    def _setRecurrenceLineFrequencies(self,
                                      minimumLineLength):
        i = 0
        diagonalLineLengths = {}
        verticalLineLengths = {}
        horizontalLineLengths = {}
        self._recurrencePoints.sort(key=lambda recurrencePoint: (recurrencePoint[0], recurrencePoint[1]))
        for indexa, indexb, xa, ya, xb, yb in self._recurrencePoints:
            count = 0
            if indexa in verticalLineLengths:
                count = verticalLineLengths[indexa]
            verticalLineLengths[indexa] = count + 1
            count = 0
            if indexb in horizontalLineLengths:
                count = horizontalLineLengths[indexb]
            horizontalLineLengths[indexb] = count + 1
            count = 0
            if indexb - indexa in diagonalLineLengths:
                count = diagonalLineLengths[indexb - indexa]
            diagonalLineLengths[indexb - indexa] = count + 1
            
        for count in verticalLineLengths.values():
            if count >= minimumLineLength:
                frequency = 0
                if count in self._verticalLineFrequency:
                    frequency = self._verticalLineFrequency[count]
                self._verticalLineFrequency[count] = frequency + 1
        for count in horizontalLineLengths.values():
            if count >= minimumLineLength:
                frequency = 0
                if count in self._horizontalLineFrequency:
                    frequency = self._horizontalLineFrequency[count]
                self._horizontalLineFrequency[count] = frequency + 1
        for count in diagonalLineLengths.values():
            if count >= minimumLineLength:
                frequency = 0
                if count in self._diagonalLineFrequency:
                    frequency = self._diagonalLineFrequency[count]
                self._diagonalLineFrequency[count] = frequency + 1
        
        index = 0
        self._maxFixationTime = 0
        self._maxFixationIndex = None
        while index < self._N:
            fixationTime = 0
            if index in verticalLineLengths:
                fixationTime = fixationTime + verticalLineLengths[index]
            if index in horizontalLineLengths:
                fixationTime = fixationTime + horizontalLineLengths[index]
            if fixationTime > self._maxFixationTime:
                self._maxFixationTime = fixationTime
                self._maxFixationIndex = index
            index = index + 1
                
    def _calculateRecurrenceCount(self):
        self._recurrenceCount = 2 * len(self._recurrencePoints) + self._N

    def _calculateRecurrenceRate(self):
        self._recurrenceRate = float(self._recurrenceCount) / self._N / self._N
    
    def _calculateDeterminism(self):
        value = 0
        for count in self._diagonalLineFrequency:
            value = value + count * self._diagonalLineFrequency[count]
        value = 2 * value + self._N
        self._determinism = float(value) / self._recurrenceCount
        
    def _calculateLaminarity(self):
        value = 0
        for count in self._verticalLineFrequency:
            value = value + count * self._verticalLineFrequency[count]
        for count in self._horizontalLineFrequency:
            value = value + count * self._horizontalLineFrequency[count]
        value = value + self._N
        self._laminarity = float(value) / self._recurrenceCount

    def _calculatePredictabilityTime(self):
        numerator = 0
        denominator = 0
        for count in self._diagonalLineFrequency:
            numerator = numerator + count * self._diagonalLineFrequency[count]
            denominator = denominator + self._diagonalLineFrequency[count]
        self._predictabilityTime = float(numerator) / denominator

    def _calculateTrappingTime(self):
        numerator = 0
        denominator = 0
        for count in self._verticalLineFrequency:
            numerator = numerator + count * self._verticalLineFrequency[count]
            denominator = denominator + self._verticalLineFrequency[count]
        for count in self._horizontalLineFrequency:
            numerator = numerator + count * self._horizontalLineFrequency[count]
            denominator = denominator + self._horizontalLineFrequency[count]
        self._trappingTime = float(numerator) / denominator

    def _calculateDivergence(self):
        maxDiagonalCount = 1
        for count in self._diagonalLineFrequency:
            if count > maxDiagonalCount:
                maxDiagonalCount = count
        self._divergence = 1.0 / maxDiagonalCount

    def _calculateEntropy(self):
        countSum = 0.0
        for count in self._diagonalLineFrequency:
            countSum = countSum + count
        value = 0
        for count in self._diagonalLineFrequency:
            p = count / countSum
            value = value - p * np.log(p)
        self._entropy = value
        
    def _calculateMostVisitedArea(self,
                                  indexedXyPoints,
                                  radius):
        xCenter = None
        yCenter = None
        for index, x, y in indexedXyPoints:
            if index == self._maxFixationIndex:
                xCenter = x
                yCenter = y
                break
        value = 0
        radius2 = radius * radius
        for index, x, y in indexedXyPoints:
            xDistance = x - xCenter
            yDistance = y - yCenter
            if xDistance * xDistance + yDistance * yDistance <= radius2:
                value = value + 1
        self._mostVisitedArea = value
        
    def _calculateGazePathLength(self,
                                 xyPoints):
        lengthMean = None
        lengthVariance = 0
        i = 1
        while i < self._N:
            xa, ya = xyPoints[i - 1]
            xb, yb = xyPoints[i]
            xDistance = xb - xa
            yDistance = yb - ya
            length = np.sqrt(xDistance * xDistance + yDistance * yDistance)
            if lengthMean is None:
                lengthMean = length
            else:
                newLengthMean = lengthMean + (length - lengthMean) / i
                lengthVariance = lengthVariance + (length - lengthMean) * (length - newLengthMean)
                lengthMean = newLengthMean
            i = i + 1
        self._gazePathLengthMean = lengthMean
        self._gazePathLengthStdDev = np.sqrt(lengthVariance / (i - 2))
