%define __python /usr/bin/python2.7
%global pyver 27
%global pybindir /usr/lib/python2.7/bin
#global pyver %{nil}

%global with_python3 0

%global srcname pyglet
%global srcversion 1.2
%global versionedname %{srcname}-%{srcversion}alpha1

Name: python%{pyver}-%{srcname}
Version: %{srcversion}
Release: 0.7.alpha1%{?dist}
Summary: A cross-platform windowing and multimedia library for Python

License: BSD
URL: http://www.pyglet.org/

# The upstream tarball includes some non-free files in the examples and tests,
# and a patented texture compression algorithm.
# Run the following (in rpmbuild/SOURCES) to generate the distributed tarball:
# $ sh pyglet-get-tarball.sh pyglet-1.2alpha1
# See the script for details.
Source0: %{versionedname}-repacked.tar.gz
Source1: pyglet-get-tarball.sh

BuildArch: noarch
BuildRequires: python%{pyver}-devel
BuildRequires: python3-devel

Requires: python%{pyver}
Requires: python%{pyver}-imaging
#Requires: python-pillow%{?_isa}

# The libraries are imported dynamically using ctypes, so rpm can't find them.
Requires: libGL
Requires: libX11


%description
This library provides an object-oriented programming interface for developing
games and other visually-rich applications with Python.
pyglet has virtually no external dependencies. For most applications and game
requirements, pyglet needs nothing else besides Python, simplifying
distribution and installation. It also handles multiple windows and
fully aware of multi-monitor setups.

pyglet might be seen as an alternative to PyGame.

%if 0%{?with_python3}
%package -n python3-%{srcname}
Summary: A cross-platform windowing and multimedia library for Python 3

Requires: python3
Requires: python3-pillow%{?_isa}

# The libraries are imported dynamically using ctypes, so rpm can't find them.
Requires: libGL
Requires: libX11

%description -n python3-%{srcname}
This library provides an object-oriented programming interface for developing
games and other visually-rich applications with Python 3.
pyglet has virtually no external dependencies. For most applications and game
requirements, pyglet needs nothing else besides Python, simplifying
distribution and installation. It also handles multiple windows and
fully aware of multi-monitor setups.

pyglet might be seen as an alternative to PyGame.

%endif


%prep
%setup -q -n %{versionedname}

# Remove the bundled pypng library python-pillow provides the same functionality)
rm pyglet/image/codecs/png.py
rm pyglet/image/codecs/pypng.py

# Get rid of hashbang lines. This is a library, it has no executable scripts.
# Also remove Windows newlines
find . -name '*.py' | xargs sed --in-place -e's|#!/usr/bin/\(env \)\?python||;s/\r//'

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif


%build
%{__python} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif

%install
%{__python} setup.py install --skip-build --root %{buildroot}
%py_byte_compile %{__python} %{buildroot}%{python_sitelib}/%{srcname}

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
%py_byte_compile %{__python3} %{buildroot}%{python3_sitelib}/%{srcname}
popd
%endif

%files
%doc LICENSE
%doc CHANGELOG
%doc README
%doc NOTICE
%doc PKG-INFO
%{python_sitelib}/%{versionedname}-py2.7.egg-info
%{python_sitelib}/%{srcname}

%if 0%{?with_python3}
%files -n python3-%{srcname}
%doc LICENSE
%doc CHANGELOG
%doc README
%doc NOTICE
%doc PKG-INFO
%{python3_sitelib}/%{versionedname}-py3.3.egg-info
%{python3_sitelib}/%{srcname}
%endif


%changelog
* Mon Oct 07 2013 Petr Viktorin <encukou@gmail.com> - 1.2-0.7.alpha1
- Enable Python 3 build

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-0.6.alpha1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jun 05 2013 Petr Viktorin <encukou@gmail.com> - 1.2-0.5.alpha1
- Add python3-devel to BuildRequires

* Wed Jun 05 2013 Petr Viktorin <encukou@gmail.com> - 1.2-0.4.alpha1
- Replace dos2unix by an additional sed command
- Remove bundled pypng, replace by a dependency in python-pillow
- Add a Python 3 build

* Fri Oct 19 2012 Petr Viktorin <encukou@gmail.com> - 1.2-0.1.alpha1
- initial version of package
