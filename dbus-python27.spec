%define __python /usr/bin/python2.7

%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%define dbus_glib_version 0.70
%define dbus_version 0.90

Summary: D-Bus Python Bindings 
Name: dbus-python27
Version: 0.83.0
Release: 6.2%{?dist}
URL: http://www.freedesktop.org/software/dbus/
Source0: http://dbus.freedesktop.org/releases/dbus-python/dbus-python-%{version}.tar.gz

License: MIT
Group: System Environment/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n) 
BuildRequires: dbus-devel >= %{dbus_version}
BuildRequires: dbus-glib-devel >= %{dbus_glib_version}
BuildRequires: python27-devel

Patch0: dbus-python-0.83.0-memleak.patch

%description

D-Bus python bindings for use with python programs.   

%package devel
Summary: Libraries and headers for dbus-python
Group: Development/Libraries
Requires: %name = %{version}-%{release}

%description devel

Headers and static libraries for hooking up custom mainloops to the dbus python
bindings.

%prep
%setup -q -n dbus-python-%{version}

%patch0 -p0 -b .memleak

%build
PYTHON=%{__python} export PYTHON
%configure

make

#CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build

%install
rm -rf %{buildroot}

PYTHON=%{__python} export PYTHON
make install DESTDIR=$RPM_BUILD_ROOT

#PKG_CONFIG_PATH=%{_libdir}/pkgconfig %{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT/%{python_sitearch}/*.la

# move away things so they do not conflict with dbus-*
mkdir -p $RPM_BUILD_ROOT%{_includedir}/python2.7
mv $RPM_BUILD_ROOT/%{_includedir}/dbus-1.0 $RPM_BUILD_ROOT%{_includedir}/python2.7/
mkdir -p $RPM_BUILD_ROOT%{_libdir}/python2.7/pkgconfig
mv $RPM_BUILD_ROOT%{_libdir}/pkgconfig/dbus-python.pc $RPM_BUILD_ROOT%{_libdir}/python2.7/pkgconfig/

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)

%doc COPYING ChangeLog README NEWS TODO
%doc doc/API_CHANGES.txt doc/HACKING.txt doc/tutorial.txt
%exclude %{_datadir}/doc/dbus-python

%dir %{python_sitelib}/dbus
%dir %{python_sitelib}/dbus/mainloop
%{python_sitearch}/*.so
%{python_sitelib}/*.py*
%{python_sitelib}/dbus/*.py*
%{python_sitelib}/dbus/mainloop/*.py*

%files devel
%defattr(-,root,root)
%{_includedir}/python2.7/dbus-1.0/dbus/dbus-python.h
%dir %{_libdir}/python2.7/pkgconfig
%{_libdir}/python2.7/pkgconfig/dbus-python.pc

%changelog
* Thu Sep 18 2014 Brandon Pierce <brandon@ihashacks.com - 0.83.0-6.1
- Rebuilt for CentOS 6

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 0.83.0-6.1
- Rebuilt for RHEL 6

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.83.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.83.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.83.0-4
- Rebuild for Python 2.6

* Tue Sep 16 2008 Marco Pesenti Gritti - 0.83.0-3
- Add patch for https://bugs.freedesktop.org/show_bug.cgi?id=17551 

* Tue Aug 05 2008  Huang Peng <phuang@redhat.com> - 0.83.0-2
- Update to 0.83.0.

* Wed Jul 16 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.82.4-3
- fix license tag

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.82.4-2
- Autorebuild for GCC 4.3

* Sun Jan 20 2008 Matthias Clasen <mclasen@redhat.com> - 0.82.4-1
- Update to 0.82.4

* Mon Oct 22 2007 Matthias Clasen <mclasen@redhat.com> - 0.82.0-3
- Rebuild against new dbus-glib

* Tue Aug 28 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 0.82.0-2
- Rebuild for selinux ppc32 issue.

* Fri Jun 22 2007 Matthias Clasen <mclasen@redhat.com> - 0.82.0-1
- Update to 0.82.0
- Put all docs in the usual place

* Tue Apr 03 2007 David Zeuthen <davidz@redhat.com> - 0.80.2-3
- Rebuild

* Tue Apr 03 2007 David Zeuthen <davidz@redhat.com> - 0.80.2-2
- Don't examine args for functions declared METH_NOARGS (#235017)

* Tue Feb 13 2007 John (J5) Palmieri <johnp@redhat.com> - 0.80.2-1
- upgrade to 0.80.2 which fixes some memleaks

* Wed Jan 24 2007 John (J5) Palmieri <johnp@redhat.com> - 0.80.1-1
- upgrade to 0.80.1
- remove dependency on Pyrex and libxml2
- some API breakage, 
  please see http://dbus.freedesktop.org/doc/dbus-python/NEWS.html
  for notes on changes 

* Wed Jan  3 2007 David Zeuthen <davidz@redhat.com> - 0.70-9%{?dist}
- rebuild against new Pyrex

* Wed Dec  6 2006 Jeremy Katz <katzj@redhat.com> - 0.70-8
- rebuild against python 2.5

* Tue Nov  7 2006 Matthias Clasen <mclasen@redhat.com> - 0.70-7
- Fix a typo in the spec file

* Fri Aug 18 2006 Karsten Hopp <karsten@redhat.com> - 0.70-6
- require libxml2-python for site-packages/dbus/introspect_parser.py

* Thu Jul 20 2006 Jesse Keating <jkeating@redhat.com> - 0.70-5
- Remove unnecessary obsoletes

* Tue Jul 18 2006 John (J5) Palmieri <johnp@redhat.com> - 0.70-4
- Try python_sitearch this time

* Tue Jul 18 2006 John (J5) Palmieri <johnp@redhat.com> - 0.70-3
- Add a BR on dbus-devel

* Tue Jul 18 2006 John (J5) Palmieri <johnp@redhat.com> - 0.70-2
- Spec file cleanups
- Add PKG_CONFIG_PATH

* Mon Jul 17 2006 John (J5) Palmieri <johnp@redhat.com> - 0.70-1
- Initial package import
