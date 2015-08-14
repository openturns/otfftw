from openturns import *
from otfftw import *
from time import time

# Create a discretized spectral normal process
dim = 1
n = 8
tg = RegularGrid(0.0, 1.0, n)
process = SpectralNormalProcess(CauchyModel(NumericalPoint(dim, 1), NumericalPoint(dim, 1)), tg)

# Sample size
size = 3

# FFT algorithm
fft = FFTW()

process.setFFTAlgorithm(fft)

# Sample the process
sample = process.getSample(size)

print "sample=", sample
