#!/usr/bin/env python3
import numpy as np
import subprocess

def interpolate(fromVal, toVal, t):
    return fromVal + ((toVal - fromVal) * t)

def getParams():
    steps = np.arange(0.0, np.pi * 2, 0.1)
    numSteps = len(steps)
    inputs = []
    for (count, step) in enumerate(steps):
        filename = "graph-%04d" % (count,)
        # if (step < np.pi):
        #     secondFrequency = 64
        #     smoothness = 8192
        # else:
        distance = (count - numSteps / 2) / (numSteps / 2)
        secondFrequency = interpolate(10, 16, distance)
        smoothness = interpolate(10, 3, distance)
        inputs.append((filename, step, secondFrequency, smoothness))
    return inputs

for params in getParams():
    (filename, offset, secondFrequency, smoothness) = params
    print("Params = " + str(params))
    result = subprocess.run([F'/bin/sh', '-c', F'./graphWavePair.py {filename} {offset} {secondFrequency} {smoothness}'])
    print(result.check_returncode())

subprocess.run(['convert', '-delay', '10', '-loop', '0', '/golem/work/*.png', 'output.gif'])

