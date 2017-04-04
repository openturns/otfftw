//                                               -*- C++ -*-
/**
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

#include "fftw3.h"
#include <openturns/OTtypes.hxx>
#include "FFTW.hxx"
#include <openturns/PersistentObjectFactory.hxx>

namespace OTFFTW {

  CLASSNAMEINIT(FFTW);

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
    oss << "class=" << FFTW::GetClassName();
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
    ComplexCollection result(size);
    fftw_plan pForward(fftw_plan_dft_1d(size, reinterpret_cast<fftw_complex *>(const_cast<OT::Complex*>(&collection[first])), reinterpret_cast<fftw_complex *>(&result[0]), FFTW_FORWARD, FFTW_ESTIMATE));
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
    ComplexCollection result(size);
    fftw_plan pBackward(fftw_plan_dft_1d(size, reinterpret_cast<fftw_complex *>(const_cast<OT::Complex*>(&collection[first])), reinterpret_cast<fftw_complex *>(&result[0]), FFTW_BACKWARD, FFTW_ESTIMATE));
    fftw_execute(pBackward);
    fftw_destroy_plan(pBackward);
    for (OT::UnsignedInteger i = 0; i < size; ++i)
      result[i] /= size;
    return result;
  }

} /* Namespace OTFFTW */
