"""
FFTW
====
"""
import openturns as ot
import otfftw
from math import pi
import matplotlib.pyplot as plt

# Create a test signal
n = 64
t = ot.RegularGrid(0.0, 0.1, n)
f_sin = ot.SymbolicFunction("t", "sin(" + str(2.0 * pi) + "*t)")
data = ot.ComplexCollection(n)
for i in range(n):
    data[i] = complex(f_sin([t.getValue(i)])[0], 0.0)

# Compute FFT
fft = otfftw.FFTW()
transformed = fft.transform(data)

# Plot using matplotlib directly
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
axes[0].plot([abs(data[i]) for i in range(n)])
axes[0].set_title("Original signal")
axes[0].set_xlabel("index")
axes[1].plot([abs(transformed[i]) for i in range(n)], color="red")
axes[1].set_title("FFT magnitude")
axes[1].set_xlabel("index")
