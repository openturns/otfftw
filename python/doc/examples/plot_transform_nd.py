"""
Multi-dimensional FFT transform
================================
"""
# %%
import openturns as ot
import otfftw

# %%
# Create a 2D complex dataset (4 rows, 6 columns in column-major order)
dims = ot.Indices([4, 6])
totalSize = 24
data = ot.ComplexCollection(totalSize)
for i in range(totalSize):
    data[i] = complex(i * 0.5, -0.1 * i)

print("dims=", dims)
print("data (first 8 values)=", [data[i] for i in range(8)])

# %%
# Create a FFTW algorithm
myFFT = otfftw.FFTW()

# %%
# Multi-dimensional direct transform
transformedData = myFFT.transformND(data, dims)
print("Transformed (first 8 values)=", [transformedData[i] for i in range(8)])

# %%
# Multi-dimensional inverse transform (round-trip)
backData = myFFT.inverseTransformND(transformedData, dims)
print("Inverse (first 8 values)=", [backData[i] for i in range(8)])

# %%
# Check the round-trip error
err = sum(abs(data[i] - backData[i]) for i in range(totalSize))
print("Round-trip error=", err)
