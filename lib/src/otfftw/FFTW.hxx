//                                               -*- C++ -*-
/**
 *  @brief FFTW is an OpenTURNS interface to the fftw library for fast discrete Fourier transform
 *
 *  Copyright 2005-2024 Airbus-EDF-IMACS-Phimeca
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

#ifndef OTFFTW_FFTW_HXX
#define OTFFTW_FFTW_HXX

#include <openturns/TypedInterfaceObject.hxx>
#include <openturns/StorageManager.hxx>
#include <openturns/FFTImplementation.hxx>
#include "otfftw/OTFFTWprivate.hxx"

namespace OTFFTW
{

/**
 * @class FFTW
 *
 * FFTW is an OpenTURNS interface to the fftw library for fast discrete Fourier transform
 */
class OTFFTW_API FFTW
  : public OT::FFTImplementation
{
  CLASSNAME

public:
  typedef OT::Collection<OT::Complex> ComplexCollection;

  /** Default constructor without parameters */
  FFTW();

  /** Virtual copy constructor */
  FFTW * clone() const override;

  /** FFT transformation on complex */
  ComplexCollection transform(const ComplexCollection & collection) const override;
  ComplexCollection transform(const ComplexCollection & collection,
                              const OT::UnsignedInteger first,
                              const OT::UnsignedInteger size) const override;

  /** FFT inverse transformation */
  ComplexCollection inverseTransform(const ComplexCollection & collection) const override;
  ComplexCollection inverseTransform(const ComplexCollection & collection,
                                     const OT::UnsignedInteger first,
                                     const OT::UnsignedInteger size) const override;

  /** String converter */
  OT::String __repr__() const override;

  /** String converter */
  OT::String __str__(const OT::String & offset = "") const override;

private:

} ; /* class FFTW */


} /* Namespace OTFFTW */

#endif /* OTFFTW_FFTW_HXX */
