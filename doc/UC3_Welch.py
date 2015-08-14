from openturns import *
from otfftw import *
from time import time

# Create a process sample
dim = 1
n = 8
tg = RegularGrid(0.0, 1.0, n)
process = SpectralNormalProcess(CauchyModel(NumericalPoint(dim, 1), NumericalPoint(dim, 1)), tg)

# Sample size
size = 3

# Sample the process
sample = process.getSample(size)

# Welch factory
factory = WelchFactory()

# FFT algorithm
fft = FFTW()

# Use this fft in the spectral process
factory.setFFTAlgorithm(fft)

# Estimate the spectral model
spectralModel = factory.build(sample)

print "spectral model=", spectralModel
