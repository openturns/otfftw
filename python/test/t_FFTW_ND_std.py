#!/usr/bin/env python

from __future__ import print_function
from openturns import *
from otfftw import *

myFFTW = FFTW()
tol = 1e-12

# 1D via ND should match 1D transform
size = 8
data = ComplexCollection(size)
for i in range(size):
    data[i] = (i + 1.0) - 0.2j * (i + 1.0)
result1D = myFFTW.transform(data)
dims = Indices([8])
resultND = myFFTW.transformND(data, dims)
err = sum(abs(resultND[i] - result1D[i]) for i in range(size))
print("ND 1D vs 1D err=", ("OK" if err < tol else "FAIL"))

# 2D round-trip
dims = Indices([4, 6])
totalSize = 24
data2d = ComplexCollection(totalSize)
for i in range(totalSize):
    data2d[i] = complex(i * 0.5, -0.1 * i)
fwd = myFFTW.transformND(data2d, dims)
bak = myFFTW.inverseTransformND(fwd, dims)
err = sum(abs(data2d[i] - bak[i]) for i in range(totalSize))
print("ND 2D round-trip err=", ("OK" if err < tol else "FAIL"))

# 3D round-trip
dims = Indices([3, 5, 4])
totalSize = 60
data3d = ComplexCollection(totalSize)
for i in range(totalSize):
    data3d[i] = complex(i * 0.3, -0.05 * i)
fwd = myFFTW.transformND(data3d, dims)
bak = myFFTW.inverseTransformND(fwd, dims)
err = sum(abs(data3d[i] - bak[i]) for i in range(totalSize))
print("ND 3D round-trip err=", ("OK" if err < tol else "FAIL"))

# Point (real data) round-trip
dims = Indices([4, 6])
totalSize = 24
realData = Point(totalSize)
for i in range(totalSize):
    realData[i] = i * 0.5
fwd = myFFTW.transformND(realData, dims)
bak = myFFTW.inverseTransformND(fwd, dims)
err = sum(abs(complex(realData[i], 0.0) - bak[i]) for i in range(totalSize))
print("ND Point round-trip err=", ("OK" if err < tol else "FAIL"))

# Bad size should throw
dims = Indices([4, 6])
caught = False
try:
    myFFTW.transformND(ComplexCollection(10), dims)
except InvalidArgumentException:
    caught = True
print("ND bad size throws=", ("OK" if caught else "FAIL"))
