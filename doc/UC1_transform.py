from openturns import *
from otfftw import *

# Create the data
n = 16
collection = NumericalComplexCollection(n)
for i in range(n):
    collection[i] = (1.0 + i) * (1.0 - 0.2j)
first = 3
size = 8

print "collection=", collection
print "first=", first
print "size=", size

# Create a FFTW algorithm
myFFT = FFTW()

# Direct transform of the whole collection
transformedCollection = myFFT.transform(collection)
print "Direct transform of the whole collection=", transformedCollection

# Direct transform of a sub-sequence
transformedCollection = myFFT.transform(collection, first, size)
print "Direct transform of a sub-sequence=", transformedCollection

# Inverse transform of the whole collection
transformedCollection = myFFT.inverseTransform(collection)
print "Inverse transform of the whole collection=", transformedCollection

# Inverse transform of a sub-sequence
transformedCollection = myFFT.inverseTransform(collection, first, size)
print "Inverse transform of a sub-sequence=", transformedCollection

