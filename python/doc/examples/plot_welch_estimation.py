"""
Spectral estimation with Welch factory
=======================================
"""
# %%
import openturns as ot
import otfftw

# %%
# Create a process sample
dim = 1
n = 8
tg = ot.RegularGrid(0.0, 1.0, n)
process = ot.SpectralGaussianProcess(
    ot.CauchyModel(ot.Point(dim, 1), ot.Point(dim, 1)), tg
)

# %%
# Sample size
size = 3
sample = process.getSample(size)

# %%
# Welch factory with FFTW
factory = ot.WelchFactory()
fft = otfftw.FFTW()
factory.setFFTAlgorithm(fft)

# %%
# Estimate the spectral model
spectralModel = factory.build(sample)
print("spectral model=", spectralModel)
