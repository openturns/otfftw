from openturns import *
from otfftw import *
from time import time

# Create a process sample
dim = 1
ResourceMap.SetAsUnsignedInteger("SpectralNormalProcess-CholeskyCacheSize", 1000000)
for In in range(1, 20):
    n = 2**In
    tg = RegularGrid(0.0, 1.0, n)
    process = SpectralNormalProcess(CauchyModel(NumericalPoint(dim, 1), NumericalPoint(dim, 1)), tg)

    # Sample size
    size = 50000 / n

    # FFT algorithm
    fft = FFTW()

    process.setFFTAlgorithm(fft)

    # Sample the process
    sample = process.getSample(size)

    # Welch factory
    factory = WelchFactory()

    # Use this fft in the spectral process
    factory.setFFTAlgorithm(fft)

    # Estimate the spectral model
    t0 = time()
    spectralModel = factory.build(sample)
    t1 = time() - t0

    # Welch factory
    factory = WelchFactory()
    spectralModel = factory.build(sample)
    t2 = time() - t0
    print "n=", n, "t1=", t1, "t2=", t2, "speedup=", 100.0 * (t2 / t1 - 1.0), "%"
