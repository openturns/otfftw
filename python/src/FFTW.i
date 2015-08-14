// SWIG file FFTW.i
// Author : $LastChangedBy: dutka $
// Date : $LastChangedDate: 2008-10-15 17:56:07 +0200 (Wed, 15 Oct 2008) $
// Id : $Id: FFTW.i 972 2008-10-15 15:56:07Z dutka $

%{
#include "FFTW.hxx"
%}

%include FFTW.hxx
namespace OTFFTW { %extend FFTW { FFTW(const FFTW & other) { return new OTFFTW::FFTW(other); } } }
