"""
Spectral process simulation with FFTW
======================================
"""
# %%
import openturns as ot
import otfftw

# %%
# Create a discretized spectral Gaussian process
dim = 1
n = 8
tg = ot.RegularGrid(0.0, 1.0, n)
process = ot.SpectralGaussianProcess(
    ot.CauchyModel(ot.Point(dim, 1), ot.Point(dim, 1)), tg
)

# %%
# Sample size
size = 3

# %%
# Set the FFT algorithm
fft = otfftw.FFTW()
process.setFFTAlgorithm(fft)

# %%
# Sample the process
sample = process.getSample(size)
print("sample=", sample)
