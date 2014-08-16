%{?scl:%scl_package blosc}
%{!?scl:%global pkg_name %{name}}

%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

Summary: A high performance compressor optimized for binary data
Name: %{?scl_prefix}blosc
Version: 1.4.1
Release: 1%{?dist}
License: MIT
Source: https://github.com/FrancescAlted/blosc/archive/v%{version}.tar.gz
URL:  https://github.com/FrancescAlted/blosc

%{?scl:Requires: %{scl}-runtime}

BuildRequires: cmake28
#BuildRequires: lz4-devel
BuildRequires: snappy-devel
BuildRequires: zlib-devel
%{?scl:BuildRequires: %{scl}-build %{scl}-runtime}

%description
Blosc is a compression library designed to transmit data to the processor
cache faster than the traditional non-compressed memory fetch.
Compression ratios are not very high, but the decompression is very fast.
Blosc is meant not only to reduce the size of large datasets on-disk or
in-memory, but also to accelerate memory-bound computations.

%package devel
Summary: Header files and libraries for Blosc development
Requires: %{?scl_prefix}%{pkg_name}%{?_isa} = %{version}-%{release}

%description devel
The blosc-devel package contains the header files and libraries needed
to develop programs that use the blosc meta-compressor.

# %package bench
# Summary: Benchmark for the Blosc compressor
# Requires: %{pkg_name} = %{version}-%{release}
# Requires: python-matplotlib

# %description bench
# The blosc-bench package contains a benchmark suite which evaluates
# the performance of Blosc, and compares it with memcpy.

%prep
%setup -q -n c-%{pkg_name}-%{version}
rm -r internal-complibs/snappy* internal-complibs/zlib*

# Fix rpath issue
sed -i '1i  set\(CMAKE_SKIP_RPATH true\)' bench/CMakeLists.txt

# Add python shebang and permission
sed -i '1i  #!/usr/bin/python' bench/plot-speeds.py

# Use the proper library path and SSE2 instruction on 64bits systems
%ifarch x86_64
%{?scl:scl enable %{scl} - << \EOF}
%cmake28 %{?_cmake_lib_suffix64} \
    -DCMAKE_BUILD_TYPE:STRING="Debug" \
    -DCMAKE_C_FLAGS:STRING="%{optflags}" \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DBUILD_STATIC:BOOL=OFF \
    -DTEST_INCLUDE_BENCH_SUITE:BOOL=OFF .
%else
%cmake28 -DCMAKE_C_FLAGS:STRING="%{optflags}" \
    -DCMAKE_BUILD_TYPE:STRING="Debug" \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DBUILD_STATIC:BOOL=OFF \
    -DTEST_INCLUDE_BENCH_SUITE:BOOL=OFF .
%endif
%{?scl:EOF}

%build
%{?scl:scl enable %{scl} - << \EOF}
make VERBOSE=1 %{?_smp_mflags}
%{?scl:EOF}

# %check
# %{?scl:scl enable %{scl} - << \EOF}
# # make test VERBOSE=1
# tests/test_api
# tests/test_basics
# for c in lz4 lz4hc snappy zlib; do
#     LD_LIBRARY_PATH=blosc bench/bench $c single 1
#     LD_LIBRARY_PATH=blosc bench/bench $c single
# done
# %{?scl:EOF}

%install

make install DESTDIR=${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}/%{_pkgdocdir}/bench
# install -p bench/plot-speeds.py* ${RPM_BUILD_ROOT}/%{_pkgdocdir}/bench/
install -pm 0644 bench/*.c ${RPM_BUILD_ROOT}/%{_pkgdocdir}/bench

mkdir -p ${RPM_BUILD_ROOT}/%{_bindir}
install -p bench/bench ${RPM_BUILD_ROOT}/%{_bindir}/%{pkg_name}-bench
# install -p bench/plot-speeds.py ${RPM_BUILD_ROOT}/%{_bindir}/%{pkg_name}-plot-times


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%exclude %{_pkgdocdir}/bench/
# Once the bench backage is built, the next line should go away!
%exclude %{_bindir}/%{pkg_name}-bench
%doc README.rst ANNOUNCE.rst RELEASE_NOTES.rst README_HEADER.rst README_THREADED.rst RELEASING.rst
%{_libdir}/libblosc.so.*


%files devel
%{_libdir}/libblosc.so
%{_includedir}/blosc.h

# %files bench
# %{_pkgdocdir}/bench/*.c
# %{_bindir}/%{pkg_name}-bench
# # %{_bindir}/%{pkg_name}-plot-times


%changelog
* Sat Aug 16 2014 Dmitrijs Milajevs <dimazest@gmail.com> - 1.4.1-1
- Cleanup and adoptations for Software collections.
- Update to 1.4.1
- Don't create bench package as the benchmark scripts are not Python 3 compatible.

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Mar 22 2014 Thibault North <tnorth@fedoraproject.org> - 1.3.5-1
- Update to 1.3.5

* Fri Mar 21 2014 Thibault North <tnorth@fedoraproject.org> - 1.3.4-1
- Update to 1.3.4

* Tue Jan 07 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.3.0-1.rc2
- Attempt to package new version

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
