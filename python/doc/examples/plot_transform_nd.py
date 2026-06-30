"""
Multi-dimensional FFT transform
================================
"""
# %%
import openturns as ot
import otfftw
import matplotlib.pyplot as plt
from math import exp, pi, cos

# %%
# 1D transform as a special case of ND
# -------------------------------------
# A 1D transform can be performed using the ND API by specifying
# a single-element dimension array.

n = 16
data1d = ot.ComplexCollection(n)
for i in range(n):
    data1d[i] = complex(cos(2.0 * pi * i / n), 0.0)

myFFT = otfftw.FFTW()
resultND = myFFT.transformND(data1d, [n])
result1D = myFFT.transform(data1d)
err1d = sum(abs(resultND[i] - result1D[i]) for i in range(n))
print(f"ND(1D) vs 1D error: {err1d:.2e}")

# %%
# 2D transform of real data
# --------------------------
# Create a real 2D dataset (8 rows, 12 columns) with a smooth pattern.
# The data is stored column-major: the first index varies fastest,
# matching OpenTURNS convention.

rows = 8
cols = 12
dims = [rows, cols]
totalSize = rows * cols
data2d = ot.Point(totalSize)
for j in range(cols):
    for i in range(rows):
        x = i / rows
        y = j / cols
        data2d[i + j * rows] = exp(-((x - 0.5)**2 + (y - 0.5)**2) / 0.05)

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(14, 4))
# Reshape for display (transpose to get row-major for imshow)
import numpy as np
img = np.array([data2d[i] for i in range(totalSize)]).reshape((rows, cols))
ax1.imshow(img.T, origin="lower", aspect="auto")
ax1.set_title("Original 2D data")

# %%
# Compute the 2D forward transform.
# The result is a flat ComplexCollection of the same size.
fwd = myFFT.transformND(data2d, dims)

# Visualise the magnitude spectrum (log scale)
mag = np.array([abs(fwd[i]) for i in range(totalSize)]).reshape((rows, cols))
ax2.imshow(np.log(mag.T + 1), origin="lower", aspect="auto")
ax2.set_title("Spectrum (log magnitude)")

# %%
# Back-transform to verify the round-trip
inv = myFFT.inverseTransformND(fwd, dims)
err2d = sum(abs(data2d[i] - inv[i]) for i in range(totalSize))
print(f"2D round-trip error: {err2d:.2e}")

# Visualise the recovered data
rec = np.array([inv[i].real for i in range(totalSize)]).reshape((rows, cols))
ax3.imshow(rec.T, origin="lower", aspect="auto")
ax3.set_title("Recovered (inverse)")

# %%
# 3D transform
# -------------
# A 3D example with a simpler pattern: compute the forward transform
# and verify the round-trip.

dims3d = [4, 6, 5]
totalSize3d = 4 * 6 * 5
data3d = ot.ComplexCollection(totalSize3d)
for i in range(totalSize3d):
    data3d[i] = complex(i * 0.5, -0.1 * i)

fwd3 = myFFT.transformND(data3d, dims3d)
inv3 = myFFT.inverseTransformND(fwd3, dims3d)
err3d = sum(abs(data3d[i] - inv3[i]) for i in range(totalSize3d))
print(f"3D round-trip error: {err3d:.2e}")

# %%
# Real vs complex input
# ----------------------
# Both Point (real-valued) and ComplexCollection inputs are accepted.
# For real input, the imaginary part is treated as zero.

dims = [4, 6]
real_data = ot.Point(24)
for i in range(24):
    real_data[i] = float(i)
compl_data = ot.ComplexCollection(24)
for i in range(24):
    compl_data[i] = complex(float(i), 0.0)
res_real = myFFT.transformND(real_data, dims)
res_compl = myFFT.transformND(compl_data, dims)
err_type = sum(abs(res_real[i] - res_compl[i]) for i in range(24))
print(f"Real vs complex input error: {err_type:.2e}")
