%define __python /usr/bin/python2.7
%global pyver 27
%global pybindir /usr/lib/python2.7/bin
#global pyver %{nil}

%global with_python3 0
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           python%{pyver}-mpmath
Version:        0.18
Release:        1%{?dist}
Summary:        A pure Python library for multiprecision floating-point arithmetic
Group:          Applications/Engineering
License:        BSD
URL:            http://code.google.com/p/mpmath/
# Source code
Source0:        http://mpmath.googlecode.com/files/mpmath-%{version}.tar.gz
# Documentation
Source1:        http://mpmath.googlecode.com/files/mpmath-docsrc-%{version}.tar.gz
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:      noarch

BuildRequires:  python%{pyver}-devel
%if 0%{?with_python3}
BuildRequires: python3-devel
%endif # with_python3

# For building documentation
BuildRequires:  dvipng
BuildRequires:  python%{pyver}-sphinx
BuildRequires:  tex(latex)
BuildRequires:  environment-modules

%description
Mpmath is a pure-Python library for multiprecision floating-point arithmetic.
It provides an extensive set of transcendental functions, unlimited exponent
sizes, complex numbers, interval arithmetic, numerical integration and
differentiation, root-finding, linear algebra, and much more. Almost any
calculation can be performed just as well at 10-digit or 1000-digit precision,
and in many cases mpmath implements asymptotically fast algorithms that scale
well for extremely high precision work. If available, mpmath will (optionally)
use gmpy to speed up high precision operations.

If you require plotting capabilities in mpmath, install python-matplotlib.


%if 0%{?with_python3}
%package -n python3-mpmath
Summary:        A pure Python library for multiprecision floating-point arithmetic

%description -n python3-mpmath
Mpmath is a pure-Python library for multiprecision floating-point arithmetic.
It provides an extensive set of transcendental functions, unlimited exponent
sizes, complex numbers, interval arithmetic, numerical integration and
differentiation, root-finding, linear algebra, and much more. Almost any
calculation can be performed just as well at 10-digit or 1000-digit precision,
and in many cases mpmath implements asymptotically fast algorithms that scale
well for extremely high precision work. If available, mpmath will (optionally)
use gmpy to speed up high precision operations.

If you require plotting capabilities in mpmath, install python3-matplotlib.
%endif # with_python3


%package doc
Summary:        HTML documentation for %{name}
Group:          Documentation
Requires:       %{name} = %{version}-%{release}

%description doc
This package contains the HTML documentation for %{name}.


%prep
%setup -q -n mpmath-%{version} -a 1
# Convert line encodings
for doc in LICENSE CHANGES PKG-INFO README.rst mpmath/tests/runtests.py; do
 sed "s|\r||g" $doc > $doc.new && \
 touch -r $doc $doc.new && \
 mv $doc.new $doc
done
find doc -name *.txt -exec sed -i "s|\r||g" {} \;

shebangs="mpmath/matrices/eigen.py mpmath/matrices/eigen_symmetric.py mpmath/tests/runtests.py mpmath/tests/test_eigen.py mpmath/tests/test_eigen_symmetric.py mpmath/tests/test_levin.py"
# Get rid of unnecessary shebangs
for lib in $shebangs; do
 sed '/^#!.*/d; 1q' $lib > $lib.new && \
 touch -r $lib $lib.new && \
 mv $lib.new $lib
done

%build
# we need to load the module for doc build to succeed
. /etc/profile.d/modules.sh
module load python
%{__python} setup.py build
# Build documentation
cd doc
%{__python} build.py

%install
%{__python} setup.py install --skip-build --root %{buildroot}
# Get rid of python 3 version that fails to byte-compile
%if 0%{?with_python3}
python3 setup.py install --skip-build --root %{buildroot}
%endif # with _python3

%check
export PYTHONPATH=`pwd`/build/lib
cd build/lib/mpmath/tests/
%{__python} runtests.py
%if 0%{?with_python3}
python3 runtests.py
%endif # with _python3

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc CHANGES LICENSE PKG-INFO README.rst
%{python_sitelib}/mpmath/
%{python_sitelib}/mpmath-%{version}-*.egg-info

%if 0%{?with_python3}
%files -n python3-mpmath
%doc CHANGES LICENSE PKG-INFO README.rst
%{python3_sitelib}/mpmath/
%{python3_sitelib}/mpmath-%{version}-*.egg-info
%endif # with _python3

%files doc
%defattr(-,root,root,-)
%doc doc/build/*

%changelog
* Thu Sep 18 2014 Brandon Pierce <brandon@ihashacks.com - 1:1.8.1-4
- Rebuilt for CentOS 6
- Make python3 optional

* Wed Jan 01 2014 Susi Lehtola <jussilehtola@fedoraproject.org> - 0.18-1
- Update to 0.18.

* Tue Aug 06 2013 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.17-8
- Add python3 package.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jul 23 2012 Jussi Lehtola <jussilehtola@fedoraproject.org> - 0.17-5
- Fix %%check phase.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Feb 06 2011 Jussi Lehtola <jussilehtola@fedoraproject.org> - 0.17-1
- Update to 0.17.

* Sun Sep 26 2010 Jussi Lehtola <jussilehtola@fedoraproject.org> - 0.16-1
- Update to 0.16.

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.15-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Mon Jun 07 2010 Jussi Lehtola <jussilehtola@fedoraproject.org> - 0.15-1
- Update to 0.15.

* Tue Apr 27 2010 Jussi Lehtola <jussilehtola@fedoraproject.org> - 0.14-1
- Update to 0.14.

* Tue Oct 06 2009 Jussi Lehtola <jussilehtola@fedoraproject.org> - 0.13-5
- Removed BR: python-matplotlib, since it didn't actually help in the missing
  image problem.
- Added versioned require in -doc.

* Tue Oct 06 2009 Jussi Lehtola <jussilehtola@fedoraproject.org> - 0.13-4
- Replaced R: python-matplotlib with a comment in %%description.
- Added missing BR: python-matplotlib.

* Tue Oct 06 2009 Jussi Lehtola <jussilehtola@fedoraproject.org> - 0.13-3
- Added missing BR: dvipng.
- Added %%check phase.

* Wed Sep 23 2009 Jussi Lehtola <jussilehtola@fedoraproject.org> - 0.13-2
- Add missing BR: tex(latex).

* Wed Sep 23 2009 Jussi Lehtola <jussilehtola@fedoraproject.org> - 0.13-1
- First release.
