// SWIG file FFTW.i

#define OTFFTW_API
#define OTFFTW_LOCAL

%{
#include "otfftw/FFTW.hxx"
%}

%include otfftw/FFTW.hxx
namespace OTFFTW { %extend FFTW { FFTW(const FFTW & other) { return new OTFFTW::FFTW(other); } } }
