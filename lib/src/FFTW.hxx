//                                               -*- C++ -*-
/**
 *  @file  FFTW.hxx
 *  @brief FFTW is an OpenTURNS interface to the fftw library for fast discrete Fourier transform
 *
 *  (C) Copyright 2005-2012 EDF-EADS-Phimeca
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
 *  along with OTMixmod.  If not, see <http://www.gnu.org/licenses/>.
 *
 */

#ifndef OTFFTW_FFTW_HXX
#define OTFFTW_FFTW_HXX

#include <openturns/TypedInterfaceObject.hxx>
#include <openturns/StorageManager.hxx>
#include <openturns/FFTImplementation.hxx>
#include "OTFFTWprivate.hxx"

namespace OTFFTW
{

  /**
   * @class FFTW
   *
   * FFTW is an OpenTURNS interface to the fftw library for fast discrete Fourier transform
   */
  class OTFFTW_API FFTW
    : public OpenTURNS::FFTImplementation
  {
    CLASSNAME;

  public:


    /** Default constructor without parameters */
    FFTW();

    /** Virtual copy constructor */
    FFTW * clone() const;

    /** FFT transformation on complex */
    FFTW::NumericalComplexCollection transform(const NumericalComplexCollection & collection) const;
    FFTW::NumericalComplexCollection transform(const NumericalComplexCollection & collection,
                                               const OT::UnsignedInteger first,
                                               const OT::UnsignedInteger size) const;

    /** FFT inverse transformation */
    FFTW::NumericalComplexCollection inverseTransform(const NumericalComplexCollection & collection) const;
    FFTW::NumericalComplexCollection inverseTransform(const NumericalComplexCollection & collection,
                                                      const OT::UnsignedInteger first,
                                                      const OT::UnsignedInteger size) const;

    /** String converter */
    OT::String __repr__() const;

    /** String converter */
    OT::String __str__(const OT::String & offset = "") const;

  private:

  } ; /* class FFTW */


} /* Namespace OTFFTW */

#endif /* OTFFTW_FFTW_HXX */
