"""
DSP estimation with FFTW
=========================
"""
# %%
import openturns as ot
import otfftw

# %%
# Create a spectral Gaussian process
tMin = 0.0
tStep = 0.5
nStep = 200
timeGrid = ot.RegularGrid(tMin, tStep, nStep)
process = ot.SpectralGaussianProcess(ot.CauchyModel(), timeGrid)

# %%
# Set the FFT algorithm
myFFT = otfftw.FFTW()
process.setFFTAlgorithm(myFFT)

# %%
# Sample the process
size = 100
sample = process.getSample(size)

# %%
# Build an estimation of the spectral density
factory = ot.WelchFactory()
factory.setFFTAlgorithm(myFFT)
outputSpectralModel = factory.build(sample)
print("Estimated spectral model:", outputSpectralModel)

# %%
# Evaluate the spectral density at a few frequency points
for f in [0.0, 0.5, 1.0, 1.5]:
    value = outputSpectralModel(f)[0, 0]
    ref = ot.CauchyModel()(f)[0, 0]
    print(f"f={f:.1f}  estimated={value.real:.4f}  reference={ref.real:.4f}")
