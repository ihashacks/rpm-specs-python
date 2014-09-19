%define __python /usr/bin/python2.7
%global pybindir /usr/lib/python2.7/bin

%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif


Name:           python27-mglob
Version:        0.4
Release:        1%{?dist}.1
Summary:        Enhanced file name globbing module

Group:          Development/Libraries
License:        MIT
URL:            http://pypi.python.org/pypi/mglob
Source0:        http://pypi.python.org/packages/source/m/mglob/mglob-%{version}.zip
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python27-devel
BuildRequires:  python27-setuptools

%description
Usable as stand-alone utility (for xargs, backticks etc.), or as a globbing
library for own python programs.
Some enhanced features are recursion, exclusion, and directory omission.


%prep
%setup -q -n mglob-%{version}
sed -i -e '/^#!\//, 1d' mglob.py


%build
%{__python} setup.py build


%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
mv  %{buildroot}%{_bindir}/mglob %{buildroot}%{_bindir}/mglob27
mkdir -p %{buildroot}%{pybindir}
ln -s %{_bindir}/mglob27 %{buildroot}%{pybindir}/mglob
 
%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
# upstream has no docs
%doc
%{_bindir}/mglob27
%{pybindir}/mglob
%{python_sitelib}/mglob.py*
%{python_sitelib}/mglob-%{version}-py?.?.egg-info


%changelog
* Thu Sep 18 2014 Brandon Pierce <brandon@ihashacks.com - 0.4-1
- Rebuilt for CentOS 6

* Sat Jun 19 2010 Thomas Spura <tomspur@fedoraproject.org - 0.4-1
- initial packaging
