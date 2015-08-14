from openturns import *
from otfftw import *
from math import *
from time import time

# Create the input process
# first, the time grid
tMin = 0.0
tStep = 0.5
nStep = 2002
timeGrid = RegularGrid(tMin, tStep, nStep)
# second, the process
inputProcess = SpectralNormalProcess(CauchyModel(), timeGrid)

# Create the FFT algorithm
myFFT = FFTW()
inputProcess.setFFTAlgorithm(myFFT)

# Create the linear model
alpha = 2.0
model = SpatialFunction(NumericalMathFunction("x", str(alpha) + "*x"))

# Create the output process
outputProcess = CompositeProcess(DynamicalFunction(model), inputProcess)
outputProcess.setTimeGrid(timeGrid)

# Sample the output process
size = 1000
t0 = time()
sample = outputProcess.getSample(size)
print "sampling time=", time() - t0, "s"

# Build an estimation of the output spectral density
factory = WelchFactory()
factory.setFFTAlgorithm(myFFT)
t0 = time()
outputSpectralModel = factory.build(sample)
print "estimation time=", time() - t0, "s"

# Graphical comparison of the output spectral models
referenceOutputSpectralModel = CauchyModel([alpha], [1.0])
frequencyGrid = outputSpectralModel.getFrequencyGrid()
nFrequency = frequencyGrid.getN()
dataEstimated = NumericalSample(nFrequency, 2)
dataReference = NumericalSample(nFrequency, 2)
for i in range(nFrequency):
    f = frequencyGrid.getValue(i)
    dataEstimated[i, 0] = f
    dataReference[i, 0] = f
    dataEstimated[i, 1] = outputSpectralModel.computeSpectralDensity(f)[0, 0].real
    dataReference[i, 1] = referenceOutputSpectralModel.computeSpectralDensity(f)[0, 0].real
g = Graph("Output DSP comparison", "f", "DSP", True, "topright")
estimated = Curve(dataEstimated)
estimated.setColor("red")
estimated.setLegendName("estimated")
estimated.setLineWidth(2)
g.add(estimated)
reference = Curve(dataReference)
reference.setColor("green")
reference.setLegendName("reference")
reference.setLineStyle("dashed")
reference.setLineWidth(2)
g.add(reference)
Show(g)
g.draw("DSPComparison", 640, 480, GraphImplementation.PDF)
