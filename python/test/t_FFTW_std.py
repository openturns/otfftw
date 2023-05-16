#!/usr/bin/env python

import openturns as ot
import otfftw

myFFTW = otfftw.FFTW()
print("myFFTW=", myFFTW)
size = 8
data = ot.ComplexCollection(size)
for i in range(size):
    data[i] = (i + 1.0) - 0.2j * (i + 1.0)
print("data=", data)
result = myFFTW.transform(data)
print("result=", result)
print("ref   =", ot.KissFFT().transform(data))
print("back=", myFFTW.inverseTransform(result))
