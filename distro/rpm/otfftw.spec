# norootforbuild
%global python_sitearch %{_libdir}/python%(python3 -c "import sysconfig; print(sysconfig.get_python_version())")/site-packages

Name:           otfftw
Version:        0.19
Release:        0%{?dist}
Summary:        OpenTURNS module
Group:          System Environment/Libraries
License:        LGPLv3+
URL:            http://www.openturns.org/
Source0:        http://downloads.sourceforge.net/openturns-modules/otfftw/otfftw-%{version}.tar.bz2
BuildRequires:  gcc-c++, cmake, swig
BuildRequires:  openturns-devel
BuildRequires:  python3-openturns
BuildRequires:  python3-devel
BuildRequires:  fftw-devel
Requires:       libotfftw0

%description
FFTW module for OpenTURNS.

%package -n libotfftw0
Summary:        OTFFTW dynamic libraries
Group:          Development/Libraries/C and C++

%description -n libotfftw0
Dynamic libraries for OTFFTW library.

%package devel
Summary:        OTFFTW development files
Group:          Development/Libraries/C and C++
Requires:       libotfftw0 = %{version}
Requires:       openturns-devel

%description devel
Development files for OTFFTW library.

%package -n python3-%{name}
Summary:        OTTemplate library
Group:          Productivity/Scientific/Math
Requires:       python3-openturns
%description -n python3-%{name}
Python textual interface to OTFFTW uncertainty library

%prep
%setup -q

%build
%cmake -DINSTALL_DESTDIR:PATH=%{buildroot} \
       -DCMAKE_SKIP_INSTALL_RPATH:BOOL=ON \
       -DCMAKE_UNITY_BUILD=ON .
%cmake_build

%install
%cmake_install

%check
export LD_LIBRARY_PATH=%{buildroot}%{_libdir}
%ctest --tests-regex pyinstallcheck --schedule-random

%post -n libotfftw0 -p /sbin/ldconfig 
%postun -n libotfftw0 -p /sbin/ldconfig 

%files -n libotfftw0
%defattr(-,root,root,-)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*.h*
%{_includedir}/%{name}/swig/
%{_libdir}/*.so
%{_libdir}/cmake/

%files -n python3-%{name}
%defattr(-,root,root,-)
%{python_sitearch}/%{name}/
%{python_sitearch}/%{name}-*.dist-info/


%changelog
* Wed Nov 28 2012 Julien Schueller <schueller at phimeca dot com> 0.0-1
- Initial package creation

