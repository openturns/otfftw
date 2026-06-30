Architecture considerations
===========================

Dependencies
------------

Several dependencies are needed in order to build the module:

 - OpenTURNS >=1.26
 - FFTW >=3.3
 - Sphinx-doc (optional for this doc)

Compilation
-----------

.. code-block:: bash

    cd otfftw
    cmake \
      -DCMAKE_INSTALL_PREFIX=$PWD/install \
      -DOpenTURNS_DIR=$PWD/../../openturns/build/install/lib/cmake/openturns \
      -B build .
    cmake --build build --target install

Source code structure
---------------------

The module consists of a C++ library wrapped for Python via SWIG. The main class
is :class:`~otfftw.FFTW` which inherits from
:class:`openturns:openturns.FFTImplementation` and provides an interface to the
FFTW library for fast discrete Fourier transforms. Multi-dimensional transforms
are implemented using the row-column algorithm.
