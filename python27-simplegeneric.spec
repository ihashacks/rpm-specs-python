%define __python /usr/bin/python2.7

%if 0%{?fedora} > 15 || 0%{?rhel} > 6
%global with_python3 0
%else
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print (get_python_lib())")}
%endif

%global modname simplegeneric

Name:           python27-simplegeneric
Version:        0.8
Release:        3%{?dist}
Summary:        Simple generic functions (similar to Python's own len(), pickle.dump(), etc.)

Group:          Development/Languages
License:        Python or ZPLv2.1
URL:            http://cheeseshop.python.org/pypi/simplegeneric
Source0:        http://pypi.python.org/packages/source/s/%{modname}/%{modname}-%{version}.zip
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python27-devel
BuildRequires:  python27-setuptools
%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  /usr/bin/2to3
%endif

%description
The simplegeneric module lets you define simple single-dispatch generic
functions, akin to Python's built-in generic functions like len(), iter() and
so on. However, instead of using specially-named methods, these generic
functions use simple lookup tables, akin to those used by e.g. pickle.dump()
and other generic functions found in the Python standard library.


%if 0%{?with_python3}
%package -n python3-%{modname}
Summary:        Simple generic functions (similar to Python's own len(), pickle.dump(), etc.)

Group:          Development/Languages
License:        Python or ZPLv2.1

%description -n python3-%{modname}
The simplegeneric module lets you define simple single-dispatch generic
functions, akin to Python's built-in generic functions like len(), iter() and
so on. However, instead of using specially-named methods, these generic
functions use simple lookup tables, akin to those used by e.g. pickle.dump()
and other generic functions found in the Python standard library.
%endif # with_python3


%prep
%setup -q -n %{modname}-%{version}

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
pushd %{py3dir}
    2to3 --write --nobackups .
    sed -i "s/file(/open(/g" setup.py
popd
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'
%endif # with_python3

find -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python}|'


%build
%{__python} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif # with_python3


%install
rm -rf %{buildroot}
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
popd
%endif # with_python3

%{__python} setup.py install --skip-build --root %{buildroot}

%check
%if 0%{?with_python3}
pushd %{py3dir}
PYTHONPATH=$(pwd) %{__python3} setup.py test
popd
%endif # with_python3

PYTHONPATH=$(pwd) %{__python} setup.py test

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README.txt
%{python_sitelib}/simplegeneric.py*
%{python_sitelib}/simplegeneric-%{version}-py?.?.egg-info

%if 0%{?with_python3}
%files -n python3-%{modname}
%defattr(-,root,root,-)
%doc README.txt
%{python3_sitelib}/__pycache__/simplegeneric.cpython*
%{python3_sitelib}/simplegeneric.py*
%{python3_sitelib}/simplegeneric-%{version}-py?.?.egg-info
%endif # with_python3

%changelog
* Thu Sep 18 2014 Brandon Pierce <brandon@ihashacks.com - 0.8-3
- Rebuilt for CentOS 6

* Fri Jan 27 2012 Thomas Spura <tomspur@fedoraproject.org> - 0.8-3
- be more explicit in files section
- add python3 subpackage (#785056)

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 14 2011 Luke Macken <lmacken@redhat.com> - 0.8-1
- Update to 0.8 (#735066)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Sep 30 2010 Luke Macken <lmacken@redhat.com> - 0.7-1
- Update to 0.7
- Run the unit tests

* Thu Jul 22 2010 Thomas Spura <tomspur@fedoraproject.org> - 0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild
- missing BR: python-devel

* Mon Apr 19 2010 Luke Macken <lmacken@redhat.com> - 0.6-2
- Change license from 'PSF or ZPL' to 'Python or ZPLv2.1'

* Tue Apr 13 2010 Luke Macken <lmacken@redhat.com> - 0.6-1
- Initial package
