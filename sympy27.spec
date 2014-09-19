%define __python /usr/bin/python2.7
%global pyver 27
%global pybindir /usr/lib/python2.7/bin
#global pyver %{nil}
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:           sympy27
%define rname	sympy
Version:        0.7.4
Release:        1%{?dist}
Summary:        A Python library for symbolic mathematics
License:        BSD
URL:            http://sympy.org/
Source0:        https://github.com/%{rname}/%{rname}/releases/download/%{rname}-%{version}/%{rname}-%{version}.tar.gz
# Upstream tried to graft in another project as a private copy; we rip
# it out (rhbz# 551576):
Patch0:         %{rname}-0.7.4-strip-internal-mpmath.patch
BuildArch:      noarch

BuildRequires:  gettext
BuildRequires:  graphviz
BuildRequires:  numpy python3-numpy
BuildRequires:  python%{pyver}-devel python3-devel
BuildRequires:  python%{pyver}-mpmath python3-mpmath
BuildRequires:  python%{pyver}-sphinx
BuildRequires:  tex(latex)
BuildRequires:  dvipng
BuildRequires:	environment-modules

Requires:       python%{pyver}-matplotlib
Requires:       python%{pyver}-mpmath
Requires:       python%{pyver}-pyglet


%description
SymPy aims to become a full-featured computer algebra system (CAS)
while keeping the code as simple as possible in order to be
comprehensible and easily extensible. SymPy is written entirely in
Python and does not require any external libraries.

%package -n python3-%{rname}
Summary:        A Python3 library for symbolic mathematics
Requires:       python3-matplotlib
Requires:       python3-mpmath
Requires:       python3-pyglet

%description -n python3-%{rname}
SymPy aims to become a full-featured computer algebra system (CAS)
while keeping the code as simple as possible in order to be
comprehensible and easily extensible. SymPy is written entirely in
Python and does not require any external libraries.

%package texmacs
Summary:        TeXmacs integration for sympy
Requires:       %{name} = %{version}-%{release}, TeXmacs

%description texmacs
This package contains a TeXmacs plugin for sympy.

%package examples
Summary:        Sympy examples
Requires:       %{name} = %{version}-%{release}

%description examples
This package contains example input for sympy.

%package doc
Summary:        Documentation for sympy
Requires:       %{name} = %{version}-%{release}

%description doc
HTML documentation for sympy.

%prep
%setup -q -n %{rname}-%{version}
%patch0 -b .mpmath
rm -rf sympy/mpmath doc/src/modules/mpmath
rm -rf %{rname}-%{version}/sympy/mpmath %{rname}-%{version}/doc/src/module/mpmath

# Help the dependency generator
sed 's/env python/python%{pyver}/' bin/isympy > bin/isympy.new
touch -r bin/isympy bin/isympy.new
mv -f bin/isympy.new bin/isympy

# Make a copy for building the python3 version
cp -a . ../foo
mv ../foo sympy-0.7.4

%build
# Build the python2 version
%{__python} setup.py build

# Build the python3 version
cd %{rname}-%{version}
python3 setup.py build

# Build the documentation
# we need to load the module for doc build to succeed
. /etc/profile.d/modules.sh
module load python
cd ../doc
make html
make cheatsheet
cd ../%{rname}-%{version}/doc
make cheatsheet

%install
# Install the python3 version
cd %{rname}-%{version}
python3 setup.py install -O1 --skip-build --root %{buildroot}
sed 's/python%{pyver}/python3/' %{buildroot}%{_bindir}/isympy > \
  %{buildroot}%{_bindir}/isympy3
touch -r %{buildroot}%{_bindir}/isympy %{buildroot}%{_bindir}/isympy3
rm -f %{buildroot}%{_bindir}/isympy
cd ..

# Install the python2 version
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

## Remove extra files
rm -f %{buildroot}%{_bindir}/{,doc}test

## Install the TeXmacs integration
cp -p data/TeXmacs/bin/tm_sympy %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/TeXmacs/plugins/sympy
cp -a data/TeXmacs/progs %{buildroot}%{_datadir}/TeXmacs/plugins/sympy

# Don't let an executable script go into the documentation
chmod a-x examples/all.py

# Install the HTML documentation
mkdir -p %{buildroot}%{_docdir}/%{name}-doc
cp -a doc/_build/html %{buildroot}%{_docdir}/%{name}-doc
rm -f %{buildroot}%{_docdir}/%{name}-doc/html/.buildinfo
rm -fr %{buildroot}%{_docdir}/%{name}-doc/i18n

mkdir -p %{buildroot}%{pybindir}
for i in %{buildroot}%{_bindir}/*py; do
        mv $i ${i}27
        j=`basename $i`
        ln -s %{_bindir}/${j}27 %{buildroot}%{pybindir}/${j}
done

%check
# The python3 tests fail with Unicode errors without this
export LC_ALL=en_US.UTF-8
%{__python} setup.py test
cd %{rname}-%{version}
python3 setup.py test
 
%files
%doc AUTHORS LICENSE PKG-INFO doc/_build/cheatsheet/cheatsheet.pdf
%{python_sitelib}/sympy/
%{python_sitelib}/sympy-%{version}-*.egg-info
%{_bindir}/isympy%{pyver}
%{pybindir}/*
%{_mandir}/man1/isympy*

%files -n python3-%{rname}
%doc %{rname}-%{version}/AUTHORS %{rname}-%{version}/LICENSE
%doc %{rname}-%{version}/PKG-INFO
%doc %{rname}-%{version}/doc/_build/cheatsheet/cheatsheet.pdf
%{python3_sitelib}/sympy/
%{python3_sitelib}/sympy-%{version}-*.egg-info
%{_bindir}/isympy3

%files texmacs
%doc data/TeXmacs/LICENSE
%{_bindir}/tm_sympy*
%{_datadir}/TeXmacs/plugins/sympy/

%files examples
%doc examples

%files doc
%docdir %{_docdir}/%{name}-doc/html
%{_docdir}/%{name}-doc/html

%changelog
* Mon Dec  9 2013 Jerry James <loganjerry@gmail.com> - 0.7.4-1
- Update to 0.7.4
- Python 2 and 3 sources are now in the same tarball

* Fri Oct 18 2013 Jerry James <loganjerry@gmail.com> - 0.7.3-2
- Build a python3 subpackage (bz 982759)

* Fri Aug  2 2013 Jerry James <loganjerry@gmail.com> - 0.7.3-1
- Update to 0.7.3
- Upstream dropped all tutorial translations
- Add graphviz BR for documentation
- Sources now distributed from github instead of googlecode
- Adapt to versionless _docdir in Rawhide

* Mon Jun 17 2013 Jerry James <loganjerry@gmail.com> - 0.7.2-1
- Update to 0.7.2 (bz 866044)
- Add python-pyglet R (bz 890312)
- Package the TeXmacs integration
- Build and provide documentation
- Provide examples
- Minor spec file cleanups

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Oct 11 2011 Jussi Lehtola <jussilehtola@fedoraproject.org> - 0.7.1-1
- Update to 0.7.1.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Aug 30 2010 Jussi Lehtola <jussilehtola@fedoraproject.org> - 0.6.7-5
- Patch around BZ #564504.

* Sat Jul 31 2010 David Malcolm <dmalcolm@redhat.com> - 0.6.7-4
- fix a python 2.7 incompatibility

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.6.7-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Apr 27 2010 Jussi Lehtola <jussilehtola@fedoraproject.org> - 0.6.7-2
- Added %%check phase.

* Tue Apr 27 2010 Jussi Lehtola <jussilehtola@fedoraproject.org> - 0.6.7-1
- Update to 0.6.7.

* Mon Feb 15 2010 Conrad Meyer <konrad@tylerc.org> - 0.6.6-3
- Patch around private copy nicely; avoid breakage from trying to replace
  a directory with a symlink.

* Mon Feb 15 2010 Conrad Meyer <konrad@tylerc.org> - 0.6.6-2
- Remove private copy of system lib 'mpmath' (rhbz #551576).

* Sun Dec 27 2009 Jussi Lehtola <jussilehtola@fedoraproject.org> - 0.6.6-1
- Update to 0.6.6.

* Sat Nov 07 2009 Jussi Lehtola <jussilehtola@fedoraproject.org> - 0.6.5-1
- Update to 0.6.5.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Dec 4 2008 Conrad Meyer <konrad@tylerc.org> - 0.6.3-1
- Bump to 0.6.3, supports python 2.6.

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.6.2-3
- Rebuild for Python 2.6

* Mon Oct 13 2008 Conrad Meyer <konrad@tylerc.org> - 0.6.2-2
- Patch to remove extraneous shebangs.

* Sun Oct 12 2008 Conrad Meyer <konrad@tylerc.org> - 0.6.2-1
- Initial package.
