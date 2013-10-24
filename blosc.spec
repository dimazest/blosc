%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

Summary: A high performance compressor optimized for binary data
Name: blosc
Version: 1.2.3
Release: 9%{?dist}
License: MIT
Source: http://blosc.org/sources/%{version}/%{name}-%{version}.tar.gz
URL:  http://blosc.org
BuildRequires: cmake

%description
Blosc is a compression library designed to transmit data to the processor 
cache faster than the traditional non-compressed memory fetch. 
Compression ratios are not very high, but the decompression is very fast. 
Blosc is meant not only to reduce the size of large datasets on-disk or 
in-memory, but also to accelerate memory-bound computations.

%package devel
Summary: Header files and libraries for Blosc development
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
The blosc-devel package contains the header files and libraries needed
to develop programs that use the blosc meta-compressor.

%package bench
Summary: Benchmark for the Blosc compressor
Requires: %{name} = %{version}-%{release}
Requires: python-matplotlib

%description bench
The blosc-bench package contains a benchmark suite which evaluates
the performances of Blosc, and compare them with memcpy.

%prep
%setup -q

# Fix library version
sed -i 's|BLOSC_VERSION_MINOR 1|BLOSC_VERSION_MINOR 2|' CMakeLists.txt
sed -i 's|BLOSC_VERSION_PATCH 6|BLOSC_VERSION_PATCH 3|' CMakeLists.txt

# Fix rpath issue
sed -i '1i  set\(CMAKE_SKIP_RPATH true\)' bench/CMakeLists.txt

# Add python shebang and permission
sed -i '1i  #!/usr/bin/python' bench/plot-speeds.py

# Use the proper library path and SSE2 instruction on 64bits systems
%ifarch x86_64
%cmake %{?_cmake_lib_suffix64} \
    -DCMAKE_BUILD_TYPE:STRING="Debug" \
    -DCMAKE_C_FLAGS:STRING="%{optflags}" \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DBUILD_STATIC:BOOL=OFF \
    -DTEST_INCLUDE_BENCH_SUITE:BOOL=OFF .
%else
%cmake -DCMAKE_C_FLAGS:STRING="%{optflags}" \
    -DCMAKE_BUILD_TYPE:STRING="Debug" \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DBUILD_STATIC:BOOL=OFF \
    -DTEST_INCLUDE_BENCH_SUITE:BOOL=OFF .
%endif

%build
make VERBOSE=1 %{?_smp_mflags}

%check
make test VERBOSE=1


%install

make install DESTDIR=${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}/%{_pkgdocdir}/bench
install -p bench/plot-speeds.py* ${RPM_BUILD_ROOT}/%{_pkgdocdir}/bench/
install -pm 0644 bench/*.c ${RPM_BUILD_ROOT}/%{_pkgdocdir}/bench

mkdir -p ${RPM_BUILD_ROOT}/%{_bindir}
install -p bench/bench ${RPM_BUILD_ROOT}/%{_bindir}/%{name}-bench
install -p bench/plot-speeds.py ${RPM_BUILD_ROOT}/%{_bindir}/%{name}-plot-times 


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%exclude %{_pkgdocdir}/bench/
%doc README.rst ANNOUNCE.rst RELEASE_NOTES.rst README_HEADER.rst README_THREADED.rst RELEASING.rst
%{_libdir}/libblosc.so.*


%files devel
%{_libdir}/libblosc.so
%{_includedir}/blosc.h

%files bench
%{_pkgdocdir}/bench/*.c
%{_bindir}/%{name}-bench
%{_bindir}/%{name}-plot-times


%changelog
* Tue Oct 22 2013 Thibault North <tnorth@fedoraproject.org> - 1.2.3-9
- Fix flags and bench compilation

* Mon Oct 21 2013 Thibault North <tnorth@fedoraproject.org> - 1.2.3-8
- Fix docdir for F<20 and remove sse flag

* Mon Oct 21 2013 Thibault North <tnorth@fedoraproject.org> - 1.2.3-7
- Use install instead of cp, more fixes

* Mon Oct 21 2013 Thibault North <tnorth@fedoraproject.org> - 1.2.3-6
- Fixes

* Mon Oct 21 2013 Thibault North <tnorth@fedoraproject.org> - 1.2.3-5
- Use pkgdocdir, various fixes.

* Mon Oct 21 2013 Thibault North <tnorth@fedoraproject.org> - 1.2.3-4
- Fix docdir, add blosc-bench subpackage

* Fri Oct 18 2013 Thibault North <tnorth@fedoraproject.org> - 1.2.3-3
- Fixes (thanks Zbigniew Jędrzejewski-Szmek)

* Wed Oct 16 2013 Thibault North <tnorth@fedoraproject.org> - 1.2.3-2
- Various fixes

* Fri Sep 20 2013 Thibault North <tnorth@fedoraproject.org> - 1.2.3-1
- Sync upstream

* Fri Mar 22 2013 Thibault North <tnorth@fedoraproject.org> - 1.1.6-1
- Initial package