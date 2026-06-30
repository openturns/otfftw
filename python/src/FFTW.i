// SWIG file FFTW.i

#define OTFFTW_API
#define OTFFTW_LOCAL

%{
#include "otfftw/FFTW.hxx"
%}

%copyctor OTFFTW::FFTW;

%include otfftw/FFTW.hxx
