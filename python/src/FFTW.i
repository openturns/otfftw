// SWIG file FFTW.i

%{
#include "otfftw/FFTW.hxx"
%}

%include otfftw/FFTW.hxx
namespace OTFFTW { %extend FFTW { FFTW(const FFTW & other) { return new OTFFTW::FFTW(other); } } }
