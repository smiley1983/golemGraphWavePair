#!/usr/bin/env python3
# Graph the interaction of waves
# Written by Jude Hungerford
import matplotlib
# Without this before import pyplot, matplotlib will try to connect to X Window
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
import sys


GOLEM_WORKDIR = '/golem/work/'

# MAX_DISTANCE refers to the maximum distance between the two waves.
# It's okay for it to be a bit larger than the actual maximum, but not smaller.
# To avoid pre-calculating this, selecting a likely number by hand works well.
# When this number is higher, you see more green and less red.
MAX_DISTANCE = 2.4

def interpolate(fromVal, toVal, t):

    return fromVal + ((toVal - fromVal) * t)


class GraphWavePair:
    def __init__(self, filename, offset, secondFrequency, smoothness):

        try:
            # There are two full waves.
            self.length = 4 * np.pi

            # One is a plain sine wave, unaffected by the parameters.
            steps = np.arange(0.0, self.length, 0.01)
            sinewave = np.sin(steps)

            # The other has a second sine wave added.
            # This one is affected by the parameters.
            steps2 = np.arange(offset, offset + self.length, 0.01)
            steps3 = np.multiply(steps2, secondFrequency)
            wave2 = np.add(np.sin(steps2), (np.divide(np.sin(steps3), smoothness)))

            # Plot both waves
            plt.plot(steps, sinewave)
            plt.plot(steps, wave2)
            ax = plt.axis([0, self.length, -2, 2])

            # Shade the area between the graphs.
            # Green when they are close fading to red as they move apart.
            for (t, val1, val2) in zip(steps, sinewave, wave2):
                distance = abs(val1 - val2) / MAX_DISTANCE
                red = interpolate(0, 1, distance)
                green = interpolate(1, 0, distance)
                plt.plot([t, t], [val1, val2], color=(red, green, 0, 1), lw=0.1)

            # Label the axes and display the parameters
            plt.xlabel('x')
            plt.ylabel('y')
            plt.annotate(xy=[0.2, 1.8], s=F'Offset                     = {offset:01f}')
            plt.annotate(xy=[0.2, 1.6], s=F'Second frequency = {secondFrequency:01f}')
            plt.annotate(xy=[0.2, 1.4], s=F'Smoothness           = {smoothness:01f}')
            plt.savefig(GOLEM_WORKDIR+filename)

        except Exception(e):
            with open('err.log', 'a') as f:
                f.write(str(e))


if __name__ == "__main__":

    args = sys.argv[1:]

    if len(args) < 4:
        with open('err.log', 'a') as f:
            f.write("graphWavePair requires 4 arguments. Arguments received: " + str(args))
        raise Exception("graphWavePair requires 4 arguments. Arguments received: " + str(args))

    else:
        GraphWavePair(str(args[0]), float(args[1]), float(args[2]), float(args[3]))

