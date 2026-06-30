#include <iostream>
#include <cmath>
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

  // --- ND transform tests ---
  const Scalar tol = 1e-12;

  // 1D via ND should match 1D transform
  {
    Indices dims(1);
    dims[0] = 8;
    OT::Collection<OT::Complex> resultND = myFFTW.transformND(data, dims);
    Scalar err = 0.0;
    for (UnsignedInteger i = 0; i < 8; ++i)
      err += std::abs(resultND[i] - result[i]);
    std::cout << "ND 1D vs 1D err=" << (err < tol ? "OK" : "FAIL") << std::endl;
  }

  // 2D round-trip
  {
    Indices dims(2);
    dims[0] = 4;
    dims[1] = 6;
    UnsignedInteger totalSize = 24;
    OT::Collection<OT::Complex> data2d(totalSize);
    for (UnsignedInteger i = 0; i < totalSize; ++i)
      data2d[i] = Complex(i * 0.5, -0.1 * i);
    OT::Collection<OT::Complex> fwd = myFFTW.transformND(data2d, dims);
    OT::Collection<OT::Complex> bak = myFFTW.inverseTransformND(fwd, dims);
    Scalar err = 0.0;
    for (UnsignedInteger i = 0; i < totalSize; ++i)
      err += std::abs(data2d[i] - bak[i]);
    std::cout << "ND 2D round-trip err=" << (err < tol ? "OK" : "FAIL") << std::endl;
  }

  // 3D round-trip
  {
    Indices dims(3);
    dims[0] = 3;
    dims[1] = 5;
    dims[2] = 4;
    UnsignedInteger totalSize = 60;
    OT::Collection<OT::Complex> data3d(totalSize);
    for (UnsignedInteger i = 0; i < totalSize; ++i)
      data3d[i] = Complex(i * 0.3, -0.05 * i);
    OT::Collection<OT::Complex> fwd = myFFTW.transformND(data3d, dims);
    OT::Collection<OT::Complex> bak = myFFTW.inverseTransformND(fwd, dims);
    Scalar err = 0.0;
    for (UnsignedInteger i = 0; i < totalSize; ++i)
      err += std::abs(data3d[i] - bak[i]);
    std::cout << "ND 3D round-trip err=" << (err < tol ? "OK" : "FAIL") << std::endl;
  }

  // 4D round-trip
  {
    Indices dims(4);
    dims[0] = 2;
    dims[1] = 3;
    dims[2] = 4;
    dims[3] = 5;
    UnsignedInteger totalSize = 120;
    OT::Collection<OT::Complex> data4d(totalSize);
    for (UnsignedInteger i = 0; i < totalSize; ++i)
      data4d[i] = Complex(i * 0.1, -0.02 * i);
    OT::Collection<OT::Complex> fwd = myFFTW.transformND(data4d, dims);
    OT::Collection<OT::Complex> bak = myFFTW.inverseTransformND(fwd, dims);
    Scalar err = 0.0;
    for (UnsignedInteger i = 0; i < totalSize; ++i)
      err += std::abs(data4d[i] - bak[i]);
    std::cout << "ND 4D round-trip err=" << (err < tol ? "OK" : "FAIL") << std::endl;
  }

  // Point (real data) round-trip
  {
    Indices dims(2);
    dims[0] = 4;
    dims[1] = 6;
    UnsignedInteger totalSize = 24;
    Point realData(totalSize);
    for (UnsignedInteger i = 0; i < totalSize; ++i)
      realData[i] = i * 0.5;
    OT::Collection<OT::Complex> fwd = myFFTW.transformND(realData, dims);
    OT::Collection<OT::Complex> bak = myFFTW.inverseTransformND(fwd, dims);
    Scalar err = 0.0;
    for (UnsignedInteger i = 0; i < totalSize; ++i)
      err += std::abs(Complex(realData[i], 0.0) - bak[i]);
    std::cout << "ND Point round-trip err=" << (err < tol ? "OK" : "FAIL") << std::endl;
  }

  // Bad size should throw
  {
    Indices dims(2);
    dims[0] = 4;
    dims[1] = 6;
    OT::Collection<OT::Complex> badData(10);
    bool caught = false;
    try {
      myFFTW.transformND(badData, dims);
    } catch (const InvalidArgumentException &) {
      caught = true;
    }
    std::cout << "ND bad size throws=" << (caught ? "OK" : "FAIL") << std::endl;
  }

  return 0;
}

