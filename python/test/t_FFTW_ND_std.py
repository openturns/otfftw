#!/usr/bin/env python

from __future__ import print_function
import openturns as ot
import openturns.testing as ott
import otfftw

myFFTW = otfftw.FFTW()
tol = 1e-12

# 1D via ND should match 1D transform
size = 8
data = ot.ComplexCollection(size)
for i in range(size):
    data[i] = (i + 1.0) - 0.2j * (i + 1.0)
result1D = myFFTW.transform(data)
dims = ot.Indices([8])
resultND = myFFTW.transformND(data, dims)
err = sum(abs(resultND[i] - result1D[i]) for i in range(size))
print("ND 1D vs 1D err=", ("OK" if err < tol else "FAIL"))

# 2D round-trip
dims = ot.Indices([4, 6])
totalSize = 24
data2d = ot.ComplexCollection(totalSize)
for i in range(totalSize):
    data2d[i] = complex(i * 0.5, -0.1 * i)
fwd = myFFTW.transformND(data2d, dims)
bak = myFFTW.inverseTransformND(fwd, dims)
err = sum(abs(data2d[i] - bak[i]) for i in range(totalSize))
print("ND 2D round-trip err=", ("OK" if err < tol else "FAIL"))

# 3D round-trip
dims = ot.Indices([3, 5, 4])
totalSize = 60
data3d = ot.ComplexCollection(totalSize)
for i in range(totalSize):
    data3d[i] = complex(i * 0.3, -0.05 * i)
fwd = myFFTW.transformND(data3d, dims)
bak = myFFTW.inverseTransformND(fwd, dims)
err = sum(abs(data3d[i] - bak[i]) for i in range(totalSize))
print("ND 3D round-trip err=", ("OK" if err < tol else "FAIL"))

# Point (real data) round-trip
dims = ot.Indices([4, 6])
totalSize = 24
realData = ot.Point(totalSize)
for i in range(totalSize):
    realData[i] = i * 0.5
fwd = myFFTW.transformND(realData, dims)
bak = myFFTW.inverseTransformND(fwd, dims)
err = sum(abs(complex(realData[i], 0.0) - bak[i]) for i in range(totalSize))
print("ND Point round-trip err=", ("OK" if err < tol else "FAIL"))

# Bad size should throw (C++ InvalidArgumentException surfaces as TypeError)
dims = ot.Indices([4, 6])
with ott.assert_raises(TypeError):
    myFFTW.transformND(ot.ComplexCollection(10), dims)
print("ND bad size throws= OK")
