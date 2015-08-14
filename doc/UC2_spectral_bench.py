from openturns import *
from otfftw import *
from time import time

# Create a discretized spectral normal process
dim = 1
ResourceMap.SetAsUnsignedInteger("SpectralNormalProcess-CholeskyCacheSize", 10000000)
for In in range(1, 20):
    n = 2**In
    tg = RegularGrid(0.0, 1.0, n)
    process = SpectralNormalProcess(CauchyModel(NumericalPoint(dim, 1), NumericalPoint(dim, 1)), tg)

    # Sample size
    size = 500000 / n
    
    # FFT algorithm
    fft = FFTW()

    process.setFFTAlgorithm(fft)

    # Sample the process
    ts = process.getSample(1)
    t0 = time()
    sample = process.getSample(size)
    t1 = time() - t0
    
    process = SpectralNormalProcess(CauchyModel(NumericalPoint(dim, 1), NumericalPoint(dim, 1)), tg)
    ts = process.getSample(1)
    t0 = time()
    sample = process.getSample(size)
    t2 = time() - t0
    print "n=", n, "t1=", t1, "t2=", t2, "speedup=", 100.0 * (t2 / t1 - 1.0), "%"
