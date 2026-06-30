//                                               -*- C++ -*-
/**
 *  @brief FFTW is an OpenTURNS interface to the fftw library for fast discrete Fourier transform
 *
 *  Copyright 2005-2018 Airbus-EDF-IMACS-Phimeca
 *
 *  OTFFTW is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  OTFFTW is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with OTFFTW.  If not, see <http://www.gnu.org/licenses/>.
 *
 */

#include <fftw3.h>
#include <openturns/OTtypes.hxx>
#include <openturns/OSS.hxx>
#include <openturns/Exception.hxx>
#include "otfftw/FFTW.hxx"
#include <openturns/PersistentObjectFactory.hxx>

namespace OTFFTW
{

CLASSNAMEINIT(FFTW)

static const OT::Factory<FFTW> Factory_FFTW;

/* Constructor with parameters */
FFTW::FFTW()
  : OT::FFTImplementation()
{
  // Nothing to do
}

/* Virtual constructor */
FFTW * FFTW::clone() const
{
  return new FFTW(*this);
}

/* OT::String converter */
OT::String FFTW::__repr__() const
{
  OT::OSS oss;
  oss << "class=" << FFTW::GetClassName();
  return oss;
}

/* OT::String converter */
OT::String FFTW::__str__(const OT::String & offset) const
{
  OT::OSS oss;
  oss << offset << FFTW::GetClassName();
  return oss;
}


/* FFT transformation on complex */
FFTW::ComplexCollection FFTW::transform(const ComplexCollection & collection) const
{
  return transform(collection, 0, collection.getSize());
}

FFTW::ComplexCollection FFTW::transform(const ComplexCollection & collection,
                                        const OT::UnsignedInteger first,
                                        const OT::UnsignedInteger size) const
{
  if (first + size > collection.getSize())
    throw OT::InvalidArgumentException(HERE) << "The sub-sequence [first, first+size) is out of bounds";
  ComplexCollection result(size);
  fftw_plan pForward(fftw_plan_dft_1d(size, reinterpret_cast<fftw_complex *>(const_cast<OT::Complex*>(&collection[first])), reinterpret_cast<fftw_complex *>(&result[0]), FFTW_FORWARD, FFTW_ESTIMATE));
  if (pForward == NULL) throw OT::InternalException(HERE) << "FFTW plan creation failed for size=" << size;
  fftw_execute(pForward);
  fftw_destroy_plan(pForward);
  return result;
}

/* FFT T transformation */
FFTW::ComplexCollection FFTW::inverseTransform(const ComplexCollection & collection) const
{
  return inverseTransform(collection, 0, collection.getSize());
}

FFTW::ComplexCollection FFTW::inverseTransform(const ComplexCollection & collection,
    const OT::UnsignedInteger first,
    const OT::UnsignedInteger size) const
{
  if (first + size > collection.getSize())
    throw OT::InvalidArgumentException(HERE) << "The sub-sequence [first, first+size) is out of bounds";
  ComplexCollection result(size);
  fftw_plan pBackward(fftw_plan_dft_1d(size, reinterpret_cast<fftw_complex *>(const_cast<OT::Complex*>(&collection[first])), reinterpret_cast<fftw_complex *>(&result[0]), FFTW_BACKWARD, FFTW_ESTIMATE));
  if (pBackward == NULL) throw OT::InternalException(HERE) << "FFTW plan creation failed for size=" << size;
  fftw_execute(pBackward);
  fftw_destroy_plan(pBackward);
  for (OT::UnsignedInteger i = 0; i < size; ++i)
    result[i] /= size;
  return result;
}

/* FFT ND transformation on complex data stored as a flat array */
FFTW::ComplexCollection FFTW::transformND(const ComplexCollection & data,
    const OT::Indices & dimensions) const
{
  return fftND(data, dimensions, FFTW_FORWARD);
}

/* FFT ND transformation on real data stored as a flat array */
FFTW::ComplexCollection FFTW::transformND(const OT::Point & data,
    const OT::Indices & dimensions) const
{
  const OT::UnsignedInteger totalSize = data.getSize();
  ComplexCollection complexData(totalSize);
  for (OT::UnsignedInteger i = 0; i < totalSize; ++i)
    complexData[i] = OT::Complex(data[i], 0.0);
  return fftND(complexData, dimensions, FFTW_FORWARD);
}

/* IFFT ND transformation on complex data stored as a flat array */
FFTW::ComplexCollection FFTW::inverseTransformND(const ComplexCollection & data,
    const OT::Indices & dimensions) const
{
  return fftND(data, dimensions, FFTW_BACKWARD);
}

/* IFFT ND transformation on real data stored as a flat array */
FFTW::ComplexCollection FFTW::inverseTransformND(const OT::Point & data,
    const OT::Indices & dimensions) const
{
  const OT::UnsignedInteger totalSize = data.getSize();
  ComplexCollection complexData(totalSize);
  for (OT::UnsignedInteger i = 0; i < totalSize; ++i)
    complexData[i] = OT::Complex(data[i], 0.0);
  return fftND(complexData, dimensions, FFTW_BACKWARD);
}

/* ND FFT helper */
FFTW::ComplexCollection FFTW::fftND(const ComplexCollection & data,
                                     const OT::Indices & dimensions,
                                     const int sign) const
{
  const OT::UnsignedInteger nDims = dimensions.getSize();
  OT::UnsignedInteger totalSize = 1;
  for (OT::UnsignedInteger i = 0; i < nDims; ++i)
    totalSize *= dimensions[i];
  if (data.getSize() != totalSize)
    throw OT::InvalidArgumentException(HERE) << "In FFTW::fftND: data size (" << data.getSize()
                                             << ") does not match product of dimensions (" << totalSize << ")";

  ComplexCollection result(totalSize);
  int *revDims = new int[nDims];
  for (OT::UnsignedInteger i = 0; i < nDims; ++i)
    revDims[i] = static_cast<int>(dimensions[nDims - 1 - i]);

  fftw_plan p(fftw_plan_dft(static_cast<int>(nDims), revDims,
                             reinterpret_cast<fftw_complex *>(const_cast<OT::Complex *>(&data[0])),
                             reinterpret_cast<fftw_complex *>(&result[0]),
                             sign, FFTW_ESTIMATE));
  delete[] revDims;
  if (p == NULL) throw OT::InternalException(HERE) << "FFTW plan creation failed for ND transform";
  fftw_execute(p);
  fftw_destroy_plan(p);

  if (sign == FFTW_BACKWARD)
  {
    const OT::Complex factor(1.0 / totalSize);
    for (OT::UnsignedInteger i = 0; i < totalSize; ++i)
      result[i] *= factor;
  }
  return result;
}

} /* Namespace OTFFTW */
