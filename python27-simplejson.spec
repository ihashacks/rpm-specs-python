
%global pyver 27
%global pybasever 2.7
%global real_name simplejson

#global _use_internal_dependency_generator 0
%global __python /usr/bin/python%{pybasever}
#global __os_install_post %{__python26_os_install_post}

%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%endif

# python26-nose is not yet in epel-5 stable
%global _with_tests 0

Name:           python%{pyver}-simplejson
Version:        2.1.1
Release:        1%{?dist}
Summary:        Simple, fast, extensible JSON encoder/decoder for Python

Group:          System Environment/Libraries
License:        MIT
URL:            http://undefined.org/python/#simplejson
Source0:        http://pypi.python.org/packages/source/s/simplejson/simplejson-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:       python(abi) = %{pybasever}
BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-distribute

%if 0%{?_with_tests}
BuildRequires:  python%{pyver}-nose
%endif

%description
simplejson is a simple, fast, complete, correct and extensible JSON
<http://json.org> encoder and decoder for Python 2.4+.  It has no
external dependencies.

simplejson was formerly known as simple_json, but changed its name to
comply with PEP 8 module naming guidelines.

The encoder may be subclassed to provide serialization in any kind of
situation, without any special support by the objects to be serialized
(somewhat like pickle).

The decoder can handle incoming JSON strings of any specified encoding
(UTF-8 by default).

This package is built against python26.


%prep
%setup -q -n %{real_name}-%{version}

# remove unwanted provides, clears rpmlint warnings
cat << \EOF > %{name}-prov
#!/bin/sh
%{__find_provides} $* | sed -e "/_speedups.so()(64bit)/d"
EOF

%global __find_provides %{_builddir}/%{real_name}-%{version}/%{name}-prov
chmod +x %{__find_provides}


%build
%{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT

%{__python} setup.py install -O1 --skip-build --root=$RPM_BUILD_ROOT \
                                 --single-version-externally-managed

# rpmlint doesn't like, plus looks like an erroneous file
rm -f docs/._index.html


%check
%if 0%{?_with_tests}
nosetests -q
%endif

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc docs LICENSE.txt
%dir %{python_sitearch}/simplejson
%{python_sitearch}/%{real_name}-%{version}-py%{pybasever}.egg-info
%{python_sitearch}/%{real_name}/*.py*
%{python_sitearch}/%{real_name}/tests/*.py*

# fixes rpmlint warnings (default installs as 775)
%attr(0755,root,root) %{python_sitearch}/%{real_name}/_speedups.so 

%changelog
* Thu Sep 18 2014 Brandon Pierce <brandon@ihashacks.com - 2.1.1-1
- Rebuilt for CentOS 6

* Fri Oct 08 2010 BJ Dierkes <wdierkes@rackspace.com> - 2.1.1-1
- Latest sources from upstream.  
  
* Thu Oct 07 2010 BJ Dierkes <wdierkes@rackspace.com> - 2.0.9-4
- Porting from Fedora 13 to EPEL 5 (python26)
- Add fixes for rpmlint warnings

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jun  5 2009 Kyle VanderBeek <kylev@kylev.com> - 2.0.9-2
- Remove ill-advised gcc BuildRequires

* Thu Jun  4 2009 Kyle VanderBeek <kylev@kylev.com> - 2.0.9-1
- Update to 2.0.9
- Make sure to require gcc to the speedups get compiled
- Fix description since we're not "pure" python
- Change to pypi instead of cheesehop

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jan 06 2009 Luke Macken <lmacken@redhat.com> 2.0.7-1
- Update to 2.0.7

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.0.3-3
- Rebuild for Python 2.6

* Thu Oct 23 2008 Luke Macken <lmacken@redhat.com> 2.0.3-2
- Use nose to run the simplejson test suite

* Mon Oct 20 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.3-1
- update to 2.0.3

* Wed Oct 01 2008 Luke Macken <lmacken@redhat.com> - 2.0.1-1
- Update to 2.0.1, which contains many optimizations and bugfixes

* Wed Sep 24 2008 Luke Macken <lmacken@redhat.com> - 1.9.3-1
- Update to 1.9.3, which includes a significant decoding speed boost, and
  various bug fixes.

* Tue May 06 2008 Luke Macken <lmacken@redhat.com> - 1.9.1-1
- Update to 1.9.1

* Wed Apr 02 2008 Luke Macken <lmacken@redhat.com> - 1.8.1-1
- Update to 1.8.1

* Thu Feb 28 2008 Luke Macken <lmacken@redhat.com> - 1.7.4-1
- Update to 1.7.4

* Fri Feb  8 2008 Luke Macken <lmacken@redhat.com> - 1.7.3-3
- Rebuild for gcc 4.3

* Wed Oct 24 2007 Luke Macken <lmacken@redhat.com> - 1.7.3-2
- Include the LICENSE.txt

* Wed Oct  3 2007 Luke Macken <lmacken@redhat.com> - 1.7.3-1
- 1.7.3

* Sun Sep  2 2007 Luke Macken <lmacken@redhat.com> - 1.7.1-3
- Update for python-setuptools changes in rawhide

* Tue Aug 21 2007 Luke Macken <lmacken@redhat.com> - 1.7.1-2
- Rebuild

* Sun Jul  8 2007 Luke Macken <lmacken@redhat.com> - 1.7.1-1
- 1.7.1

* Wed Mar 21 2007 Luke Macken <lmacken@redhat.com> - 1.7-2
- Use python_sitearch instead of sitelib

* Tue Mar 20 2007 Luke Macken <lmacken@redhat.com> - 1.7-1
- 1.7 (Bug #233212)

* Sat Mar  3 2007 Luke Macken <lmacken@redhat.com> - 1.5
- 1.5

* Sat Dec  9 2006 Luke Macken <lmacken@redhat.com> - 1.4-4
- Add python-devel to BuildRequires

* Sat Dec  9 2006 Luke Macken <lmacken@redhat.com> - 1.4-2
- Rebuild for new python

* Fri Nov 24 2006 Luke Macken <lmacken@redhat.com> - 1.4-1
- 1.4

* Sun Sep  3 2006 Luke Macken <lmacken@redhat.com> - 1.3-4
- Rebuild for FC6

* Mon Aug 14 2006 Luke Macken <lmacken@redhat.com> - 1.3-3
- Include .pyo's instead of just ghosting them

* Wed Jul 12 2006 Luke Macken <lmacken@redhat.com> - 1.3-2
- Add --single-version-externally-managed flag to install

* Mon Jul 10 2006 Luke Macken <lmacken@redhat.com> - 1.3-1
- Initial package
