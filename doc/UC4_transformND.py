from openturns import *
from otfftw import *

# Create a 2D complex dataset (4 rows, 6 columns in column-major order)
dims = Indices([4, 6])
totalSize = 24
data = ComplexCollection(totalSize)
for i in range(totalSize):
    data[i] = complex(i * 0.5, -0.1 * i)

print("dims=", dims)
print("data (first 8 values)=", data[0:8])

# Create a FFTW algorithm
myFFT = FFTW()

# Multi-dimensional direct transform
transformedData = myFFT.transformND(data, dims)
print("Transformed (first 8 values)=", transformedData[0:8])

# Multi-dimensional inverse transform (round-trip)
backData = myFFT.inverseTransformND(transformedData, dims)
print("Inverse (first 8 values)=", backData[0:8])

# Check the round-trip error
err = sum(abs(data[i] - backData[i]) for i in range(totalSize))
print("Round-trip error=", err)
