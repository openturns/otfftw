#!/usr/bin/env python

from __future__ import print_function
from openturns import *
from otfftw import *
from time import *


myFFTW = FFTW()
print("myFFTW=", myFFTW)
size = 8
data = ComplexCollection(size)
for i in range(size):
    data[i] = (i + 1.0) -0.2j * (i + 1.0)
print("data=", data)
result = myFFTW.transform(data)
print("result=", result)
print("ref   =", KissFFT().transform(data))
print("back=", myFFTW.inverseTransform(result))

