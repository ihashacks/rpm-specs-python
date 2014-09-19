%define __python /usr/bin/python2.7
%global pybindir /usr/lib/python2.7/bin

%global with_python3 0

%global betaver b1

%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

# tracer.so is a private object, don't include it in the provides
%global _use_internal_dependency_generator 0
%global __find_provides /bin/sh -c "%{_rpmconfigdir}/find-provides | grep -v -E '(tracer.so)' || /bin/true"
%global __find_requires /bin/sh -c "%{_rpmconfigdir}/find-requires | grep -v -E '(tracer.so)' || /bin/true"

Name:           python27-coverage
Summary:        Code coverage testing module for Python
Version:        3.5.1
Release:        0.1.%{betaver}%{?dist}.2
License:        BSD and (MIT or GPLv2)
Group:          System Environment/Libraries
URL:            http://nedbatchelder.com/code/modules/coverage.html
Source0:        http://pypi.python.org/packages/source/c/coverage/coverage-%{version}%{betaver}.tar.gz
BuildRequires:  python27-setuptools, python27-devel
Requires:       python27-setuptools
%if 0%{?with_python3}
BuildRequires:  /usr/bin/2to3
BuildRequires:  python3-setuptools, python3-devel
%endif # with_python3

%description
Coverage.py is a Python module that measures code coverage during Python 
execution. It uses the code analysis tools and tracing hooks provided in the 
Python standard library to determine which lines are executable, and which 
have been executed.

%if 0%{?with_python3}
%package -n python3-coverage
Summary:        Code coverage testing module for Python 3
Group:          System Environment/Libraries
# As the "coverage" executable requires the setuptools at runtime (#556290),
# so the "python3-coverage" executable requires python3-setuptools:
Requires:       python3-setuptools

%description -n python3-coverage
Coverage.py is a Python 3 module that measures code coverage during Python
execution. It uses the code analysis tools and tracing hooks provided in the 
Python standard library to determine which lines are executable, and which 
have been executed.
%endif # with_python3

%prep
%setup -q -n coverage-%{version}%{betaver}

find . -type f -exec chmod 0644 \{\} \;
sed -i 's/\r//g' README.txt

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
pushd %{py3dir}
2to3 --nobackups --write .
popd
%endif # if with_python3

%build
%{__python} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif # if with_python3

%install
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}
mv %{buildroot}/%{_bindir}/coverage %{buildroot}/%{_bindir}/python3-coverage
popd
%endif # if with_python3

%{__python} setup.py install -O1 --skip-build --root %{buildroot}

mv %{buildroot}/%{_bindir}/coverage %{buildroot}/%{_bindir}/coverage2.7
mkdir -p %{buildroot}%{pybindir}
ln -s %{_bindir}/coverage2.7 %{buildroot}%{pybindir}/coverage

%files
%doc README.txt
%{_bindir}/coverage*
%{pybindir}/coverage*
%{python_sitearch}/coverage/
%{python_sitearch}/coverage*.egg-info/

%if 0%{?with_python3}
%files -n python3-coverage
%{_bindir}/python3-coverage
%{python3_sitearch}/coverage/
%{python3_sitearch}/coverage*.egg-info/
%endif # if with_python3


%changelog
* Thu Sep 18 2014 Brandon Pierce <brandon@ihashacks.com - 3.5.1-0.1.b1
- Rebuilt for CentOS 6

* Fri Sep  2 2011 Tom Callaway <spot@fedoraproject.org> - 3.5.1-0.1.b1
- update to 3.5.1b1

* Mon Jun  6 2011 Tom Callaway <spot@fedoraproject.org> - 3.5-0.1.b1
- update to 3.5b1

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 29 2010  <David Malcolm <dmalcolm@redhat.com>> - 3.4-2
- rebuild for newer python3

* Thu Oct 21 2010 Luke Macken <lmacken@redhat.com> - 3.4-1
- Update to 3.4 (#631751)

* Fri Sep 03 2010 Luke Macken <lmacken@redhat.com> - 3.3.1-4
- Rebuild against Python 3.2

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 3.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed May 9 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 3.3.1-2
- Fix license tag, permissions, and filtering extraneous provides

* Wed May 9 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 3.3.1-1
- Update to 3.3.1

* Fri Feb  5 2010 David Malcolm <dmalcolm@redhat.com> - 3.2-3
- add python 3 subpackage (#536948)

* Sun Jan 17 2010 Luke Macken <lmacken@redhat.com> - 3.2-2
- Require python-setuptools (#556290)

* Wed Dec  9 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 3.2-1
- update to 3.2

* Fri Oct 16 2009 Luke Macken <lmacken@redhat.com> - 3.1-1
- Update to 3.1

* Wed Aug 10 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 3.0.1-1
- update to 3.0.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.85-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri May 15 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2.85-2
- fix install invocation

* Wed May 6 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2.85-1
- Initial package for Fedora
