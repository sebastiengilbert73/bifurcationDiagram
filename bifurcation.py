import numpy
import matplotlib
import recursion
import argparse
import ast
from matplotlib import style
import matplotlib.pyplot

parser = argparse.ArgumentParser()
parser.add_argument('--recursionFunction', help="The recursion function. Default: 'LogisticMap'", default='LogisticMap')
parser.add_argument('--parametersDictionary', help="The dictionary of parameters to pass to the recursion function constructor. Default: '{"r":2.0}'", default='{"r":2.0}')
parser.add_argument('--parameterToSweep', help="The parameter to sweep. Default: 'r'", default='r')
parser.add_argument('--parameterSweepRange', help="The range of parameter sweep. Default: '[0, 4.0]'", default='[0, 4.0]')
parser.add_argument('--numberOfParameterSamples', help='The number of parameters to sample in the range. Default: 101', type=int, default=101)
parser.add_argument('--seriesIndicesToKeep', help="The range of indices in the series to keep, Default: '[10, 100]'", default='[10, 100]')
parser.add_argument('--startingValuesList', help="The list of initial values. Default: '[0.3]'", default='[0.3]')
args = parser.parse_args()

parametersDictionary = ast.literal_eval(args.parametersDictionary)
parameterSweepRange = ast.literal_eval(args.parameterSweepRange)
seriesIndicesToKeep = ast.literal_eval(args.seriesIndicesToKeep)
startingValuesList = ast.literal_eval(args.startingValuesList)

def main():
    print ("bifurcation.py main()")

    xValues = []
    yValues = []

    # Sweep the parameter
    sweptParameterValues = numpy.linspace(parameterSweepRange[0], parameterSweepRange[1], args.numberOfParameterSamples)
    for sweptParameterValue in sweptParameterValues:
        # Create recursion function
        if args.recursionFunction == 'LogisticMap':
            if args.parameterToSweep == 'r':
                r = sweptParameterValue
            else:
                raise ValueError("main(): With LogisticMap, unkown parameter '{}'".format(args.parameterToSweep))
            recursionFunction = recursion.LogisticMap(r=r)
        elif args.recursionFunction == 'RickerModel':
            r = parametersDictionary['r']
            k = parametersDictionary['k']
            if args.parameterToSweep == 'r':
                r = sweptParameterValue
            elif args.parameterToSweep == 'k':
                k = sweptParameterValue
            else:
                raise ValueError("main(): With RickerModel, unkown parameter '{}'".format(args.parameterToSweep))
            recursionFunction = recursion.RickerModel(r=r, k=k)
        elif args.recursionFunction == 'Triangle':
            center = parametersDictionary['center']
            height = parametersDictionary['height']
            if args.parameterToSweep == 'center':
                center = sweptParameterValue
            elif args.parameterToSweep == 'height':
                height = sweptParameterValue
            else:
                raise ValueError("main(): With Triangle, unkown parameter '{}'".format(args.parameterToSweep))
            recursionFunction = recursion.Triangle(center, height)
        else:
            raise ValueError("main(): Unknown recursion function '{}'".format(args.recursionFunction))

        maxSeriesIndex = seriesIndicesToKeep[1]
        seriesList = recursionFunction.Series(startingValuesList, maxSeriesIndex + 1)
        #print ("seriesList = {}".format(seriesList))
        for index in range(seriesIndicesToKeep[0], seriesIndicesToKeep[1] + 1):
            xValues.append(sweptParameterValue)
            yValues.append(seriesList[index])

    # Display the plot
    style.use('fivethirtyeight')

    fig = matplotlib.pyplot.figure()
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.plot(xValues, yValues, ',')

    matplotlib.pyplot.show()

if __name__ == '__main__':
    main()