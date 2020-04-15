#include <iostream>
// OT includes
#include <openturns/OT.hxx>
#include "otfftw/FFTW.hxx"
using namespace OT;


int main()
{
  OTFFTW::FFTW myFFTW;
  std::cout << "myFFTW=" << myFFTW << std::endl;
  OT::UnsignedInteger size(8);
  OT::Collection<OT::Complex> data(size);
  for (OT::UnsignedInteger i = 0; i < size; ++i)
    data[i] = OT::Complex(i + 1.0, -0.2 * (i + 1.0));
  std::cout << "data=" << data << std::endl;
  OT::Collection<OT::Complex> result(myFFTW.transform(data));
  std::cout << "result=" << result << std::endl;
  std::cout << "ref   =" << OT::KissFFT().transform(data) << std::endl;
  std::cout << "back=" << myFFTW.inverseTransform(result) << std::endl;
  return 0;
}

