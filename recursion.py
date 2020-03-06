import numpy
import abc
import math


class RecursiveFunction(abc.ABC):
    """
    Abstract class that defines a recursive function
    """
    def __init__(self):
        super().__init__()

    @abc.abstractmethod
    def NextValue(self, precedingValuesList):
        pass  # return next value

    def Series(self, precedingValuesList, numberOfTerms):
        if numberOfTerms < len(precedingValuesList):
            raise ValueError("RecursiveFunction.Series(): numberOfTerms ({}) < len(precedingValuesList) ({})".format(numberOfTerms, len(precedingValuesList)))
        seriesList = precedingValuesList.copy()
        while len(seriesList) < numberOfTerms:
            nextValue = self.NextValue(seriesList)
            seriesList.append(nextValue)
        return seriesList



class LogisticMap(RecursiveFunction):
    def __init__(self, r):
        super(LogisticMap, self).__init__()

        self.r = r

    def NextValue(self, precedingValuesList):
        x0 = precedingValuesList[-1]
        x1 = self.r * x0 * (1.0 - x0)
        return x1

    def NextValueRule(self, numberOfSamples):
        xValues = numpy.linspace(0.0, 1.0, numberOfSamples)
        yValues = [self.NextValue([x]) for x in xValues]
        xyValues = list(zip(xValues, yValues))
        return xyValues


class RickerModel(RecursiveFunction):
    def __init__(self, r, k):
        super(RickerModel, self).__init__()

        self.r = r
        self.k = k

    def NextValue(self, precedingValuesList):
        N0 = precedingValuesList[-1]
        N1 = N0 * math.exp( self.r * (1.0 - N0/self.k) )
        return N1

    def NextValueRule(self, initial_N, final_N, numberOfSamples):
        xValues = numpy.linspace(initial_N, final_N, numberOfSamples)
        yValues = [self.NextValue([x]) for x in xValues]
        xyValues = list(zip(xValues, yValues))
        return xyValues



if __name__ == '__main__':
    print ("recursion.py __main__")

    logisticMap = LogisticMap(r=2.0)

    x0 = 0.1
    nextValue = logisticMap.NextValue([x0])
    print ("nextValue = {}".format(nextValue))

    series = logisticMap.Series([x0], 15)
    print ("series = {}".format(series))

    nextValueRule = logisticMap.NextValueRule(11)
    #print ("nextValueRule = {}".format(nextValueRule))

    rickerModel = RickerModel(1.3, 20)
    nextValueRule = rickerModel.NextValueRule(1, 40, 21)
    print ("nextValueRule = {}".format(nextValueRule))