#!/usr/bin/env python3
import matplotlib
# Without this being called before import pyplot, matplotlib will try 
# to connect to X Window
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
            self.length = 4 * np.pi

            steps = np.arange(0.0, self.length, 0.01)

            sinewave = np.sin(steps)

            steps2 = np.arange(offset, offset + self.length, 0.01)

            steps3 = np.multiply(np.arange(offset, offset + self.length, 0.01), secondFrequency)

            wave2 = np.add(np.sin(steps2), (np.divide(np.sin(steps3), smoothness)))

            unused = plt.plot(steps, sinewave)

            unused2 = plt.plot(steps, wave2)

            ax = plt.axis([0, self.length, -2, 2])

            # Convenient constant for intended inputs
            max_distance = MAX_DISTANCE

            # # To scale the distances relative to the max distance on each
            # # individual  graph
            #
            # for (val1, val2) in zip(sinewave, wave2):
            #     max_distance = max(max_distance, (abs (val1 - val2)))

            for (t, val1, val2) in zip(steps, sinewave, wave2):

                distance = abs(val1 - val2) / max_distance

                red = interpolate(0, 1, distance)

                green = interpolate(1, 0, distance)

                plt.plot([t, t], [val1, val2], color=(red, green, 0, 1), lw=0.1)


            #plt.show()

            plt.savefig(GOLEM_WORKDIR+filename)

        except Exception(e):
            with open('err.log', 'a') as f:
                f.write(str(e))

args = sys.argv[1:]
# with open(F'{GOLEM_WORKDIR}err2.log', 'w') as f:
#     f.write(str(args))
if len(args) < 4:
    with open('err.log', 'a') as f:
        f.write("graphWavePair requires 4 arguments. Arguments received: " + str(args))
    raise Exception("graphWavePair requires 4 arguments. Arguments received: " + str(args))
else:
    GraphWavePair(str(args[0]), float(args[1]), float(args[2]), float(args[3]))
