%define __python /usr/bin/python2.7

%{!?python_sitearch:%global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%{!?python_inc:%global python_inc %(%{__python} -c "from distutils.sysconfig import get_python_inc; print get_python_inc(1)")}

%global pylibdir /usr/lib/python2.7

Summary: SIP - Python/C++ Bindings Generator
Name: sip27
Version: 4.9.3
Release: 1.1%{?dist}.1
License: GPLv2 or GPLv3
Group: Development/Tools
Url: http://www.riverbankcomputing.com/software/sip/intro 
Source0: http://www.riverbankcomputing.com/static/Downloads/sip4/sip-%{version}%{?snap:-snapshot-%{snap}}.tar.gz
Patch1: sip27.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# extracted from sip.h, SIP_API_MAJOR_NR SIP_API_MINOR_NR defines
Source1: macros.sip
%global _sip_api_major 6
%global _sip_api_minor 0
%global _sip_api %{_sip_api_major}.%{_sip_api_minor}

Provides: sip-api(%{_sip_api_major}) = %{_sip_api}

BuildRequires: python27-devel
BuildRequires: sed

%description
SIP is a tool for generating bindings for C++ classes so that they can be
accessed as normal Python classes. SIP takes many of its ideas from SWIG but,
because it is specifically designed for C++ and Python, is able to generate
tighter bindings. SIP is so called because it is a small SWIG.

SIP was originally designed to generate Python bindings for KDE and so has
explicit support for the signal slot mechanism used by the Qt/KDE class
libraries. However, SIP can be used to generate Python bindings for any C++
class library.

%package devel
Summary: Files needed to generate Python bindings for any C++ class library
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: python27-devel 
Requires: rpm
%description devel
This package contains files needed to generate Python bindings for any C++
classes library.


%prep

%setup -q -n sip-%{version}%{?snap:-snapshot-%{snap}}
%patch1 -p1 -b .py27

%build
%{__python} configure.py -d %{python_sitearch} CXXFLAGS="%{optflags}" CFLAGS="%{optflags}"

make %{?_smp_mflags} 


%install
rm -rf %{buildroot}

make install DESTDIR=%{buildroot}
mkdir -p %{buildroot}%{_datadir}/sip27
mv %{buildroot}%{_bindir}/sip %{buildroot}%{_bindir}/sip27
mkdir -p %{buildroot}%{pylibdir}/bin
ln -s %{_bindir}/sip27 %{buildroot}%{pylibdir}/bin/sip

install -D -p -m644 %{SOURCE1} %{buildroot}%{_sysconfdir}/rpm/macros.sip27


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc ChangeLog LICENSE NEWS README
%doc LICENSE-GPL2.txt LICENSE-GPL3.txt
%{python_sitearch}/*

%files devel
%defattr(-,root,root,-)
%{_bindir}/sip27
%{pylibdir}/bin/sip
%{_datadir}/sip27/
%{python_inc}/*
%{_sysconfdir}/rpm/macros.sip27


%changelog
* Thu Sep 18 2014 Brandon Pierce <brandon@ihashacks.com - 4.9.3-1
- Rebuilt for CentOS 6

* Mon Nov 23 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.9.3-1
- sip-4.9.3

* Fri Nov 20 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.9.2-1
- sip-4.9.2

* Tue Nov 16 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.9.1-3
- move sip binary to -devel 

* Mon Nov 16 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.9.1-2
- Provides: sip-api(%%_sip_api_major) = %%_sip_api
- devel: /etc/rpm/macros.sip helper

* Fri Oct 23 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.9.1-1
- sip-4.9.1

* Thu Oct 15 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.9.1-0.1.20091014
- sip-4.9.1-snapshot-20091014

* Thu Oct 15 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.9-1
- sip-4.9
- License: GPLv2 or GPLv3

* Mon Aug 10 2009 Ville Skyttä <ville.skytta@iki.fi> - 4.8.2-2
- Convert specfile to UTF-8.

* Tue Jul 28 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.8.2-1
- sip-4.8.2

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun 16 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.8.1-1
- sip-4.8.1

* Fri Jun 05 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.8-1
- sip-4.8

* Thu May 21 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.8-0.1.20090430
- sip-4.8-snapshot-20090430

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.7.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 4.7.9-2
- Rebuild for Python 2.6

* Mon Nov 17 2008 Rex Dieter <rdieter@fedoraproject.org> 4.7.9-1
- sip-4.7.9

* Mon Nov 10 2008 Rex Dieter <rdieter@fedoraproject.org> 4.7.8-1
- sip-4.7.8

* Thu Sep 04 2008 Tom "spot" Callaway <tcallawa@redhat.com> 4.7.7-3
- fix license tag

* Tue Sep 02 2008 Than Ngo <than@redhat.com> 4.7.7-2
- get rid of BR on qt

* Tue Aug 26 2008 Rex Dieter <rdieter@fedoraproject.org> - 4.7.7-1
- sip-4.7.7

* Wed May 21 2008 Rex Dieter <rdieter@fedoraproject.org> - 4.7.6-1
- sip-4.7.6

* Wed May 14 2008 Rex Dieter <rdieter@fedoraproject.org> - 4.7.5-1
- sip-4.7.5

* Tue Mar 25 2008 Rex Dieter <rdieter@fedoraproject.org> - 4.7.4-3
- BR: qt3-devel (f9+)

* Tue Feb 12 2008 Rex Dieter <rdieter@fedoraproject.org> - 4.7.4-2
- fix 64bit patch

* Tue Feb 12 2008 Rex Dieter <rdieter@fedoraproject.org> - 4.7.4-1
- sip-4.7.4

* Thu Dec 06 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 4.7.3-1
- sip-4.7.3

* Wed Dec 05 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 4.7.2-1
- sip-4.7.2
- omit needless scriptlets

* Mon Nov 12 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 4.7.1-2
- License: Python Software Foundation License v2
- fix/cleanup some macro usage
- fix Source, Url. 

* Mon Oct 22 2007 Than Ngo <than@redhat.com> - 4.7.1-1
- 4.7.1

* Mon Oct 01 2007 Than Ngo <than@redhat.com> - 4.6-3
- fix rh#289321, sipconfig.py includes wrong py_lib_dir, thanks to Rex Dieter

* Thu Aug 30 2007 Than Ngo <than@redhat.com> - 4.6-2.fc7
- typo in description

* Thu Apr 12 2007 Than Ngo <than@redhat.com> - 4.6-1.fc7
- 4.6

* Thu Jan 18 2007 Than Ngo <than@redhat.com> - 4.5.2-1
- 4.5.2 

* Thu Dec  7 2006 Jeremy Katz <katzj@redhat.com> - 4.5-2
- rebuild against python 2.5
- cleanups for python packaging guidelines

* Mon Nov 06 2006 Than Ngo <than@redhat.com> 4.5-1
- 4.5

* Thu Sep 28 2006 Than Ngo <than@redhat.com> 4.4.5-3
- fix #207297, use qt qmake files

* Wed Sep 20 2006 Than Ngo <than@redhat.com> 4.4.5-2
- fix #206633, own %%_datadir/sip

* Wed Jul 19 2006 Than Ngo <than@redhat.com> 4.4.5-1
- update to 4.4.5

* Mon Jul 17 2006 Than Ngo <than@redhat.com> 4.4.3-2
- rebuild

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 4.4.3-1.1
- rebuild

* Thu Apr 27 2006 Than Ngo <than@redhat.com> 4.4.3-1
- update to 4.4.3
- built with %%{optflags}


* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 4.3.1-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 4.3.1-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Sep 12 2005 Than Ngo <than@redhat.com> 4.3.1-1
- update to 4.3.1

* Wed Mar 23 2005 Than Ngo <than@redhat.com> 4.2.1-1
- 4.2.1

* Fri Mar 04 2005 Than Ngo <than@redhat.com> 4.2-1
- 4.2

* Thu Nov 11 2004 Than Ngo <than@redhat.com> 4.1-2
- rebuild against python 2.4

* Fri Sep 24 2004 Than Ngo <than@redhat.com> 4.1-1
- update to 4.1

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu May 27 2004 Than Ngo <than@redhat.com> 3.10.2-1
- update to 3.10.2

* Fri Mar 12 2004 Than Ngo <than@redhat.com> 3.10.1-1
- update to 3.10.1

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Feb 19 2004 Than Ngo <than@redhat.com> 3.10-6 
- fix Requires issue, bug #74004

* Thu Feb 19 2004 Than Ngo <than@redhat.com> 3.10-5
- fix lib64 issue

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Feb 12 2004 Than Ngo <than@redhat.com> 3.10-3
- use new method of building SIP

* Wed Feb 11 2004 Than Ngo <than@redhat.com> 3.10-2
- rebuilt against qt 3.3.0

* Wed Feb 04 2004 Than Ngo <than@redhat.com> 3.10-1
- 3.10

* Thu Nov 27 2003 Than Ngo <than@redhat.com> 3.8-2
- rebuild against python 2.3 and Qt 3.2.3

* Fri Sep 26 2003 Harald Hoyer <harald@redhat.de> 3.8-1
- 3.8

* Mon Jul 21 2003 Than Ngo <than@redhat.com> 3.7-1
- 3.7

* Tue Jun 24 2003 Than Ngo <than@redhat.com> 3.6-3
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue May  6 2003 Than Ngo <than@redhat.com> 3.6-1.1
- 3.6

* Tue Mar  4 2003 Than Ngo <than@redhat.com> 3.5.1-0.20030301.0
- snapshot 20030301, support qt 3.1.2

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Dec 11 2002 Than Ngo <than@redhat.com> 3.5-1
- 3.5 release

* Mon Nov 18 2002 Than Ngo <than@redhat.com> 3.5-0.20021114.1
- update RC, which supports qt 3.1.0
- fix dependency problem with python

* Thu Nov  7 2002 Than Ngo <than@redhat.com> 3.4-4
- update to 3.4

* Wed Aug 28 2002 Than Ngo <than@redhat.com> 3.3.2-4
- rpath issue

* Mon Aug 26 2002 Than Ngo <than@redhat.com> 3.3.2-3
- rebuild against new qt

* Sat Aug 10 2002 Elliot Lee <sopwith@redhat.com>
- rebuilt with gcc-3.2 (we hope)

* Tue Jul 23 2002 Than Ngo <than@redhat.com> 3.3.2-1
- 3.3.2 release for qt 3.0.5

* Mon Jul  1 2002 Than Ngo <than@redhat.com> 3.2.4-4
- move python modul libsip.so into sip (bug #67640)

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed May 22 2002 Harald Hoyer <harald@redhat.de>
- updated to release 3.2.4

* Thu May 02 2002 Than Ngo <than@redhat.com> 3.2-0.rc4
- 3.2rc4
- build against python 2

* Tue Apr 16 2002 Than Ngo <than@redhat.com> 3.1-2
- rebuild

* Fri Mar 29 2002 Than  Ngo <than@redhat.com> 3.1-1
- update 3.1 for qt 3.0.3

* Tue Mar  07 2002 Than Ngo <than@redhat.com> 3.0-6
- rebuild against qt3

* Fri Feb 22 2002 Than Ngo <than@redhat.com> 3.0-5
- build against python 1.5 and qt 2.3.2

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Jan 08 2002 Than Ngo <than@redhat.com> 3.0-3
- rebuild to get rid of libGL

* Mon Nov 19 2001 Than Ngo <than@redhat.com> 3.0-2
- build against qt3

* Sun Nov 18 2001 Than Ngo <than@redhat.com> 3.0-1
- update to 3.0

* Sun Nov 11 2001 Than Ngo <than@redhat.com> 3.0-0.20011110.1
- snapshot

* Tue Aug 14 2001 Than Ngo <than@redhat.com> 2.5-1
- update to 2.5
- requires python 2
- Updated URL

* Mon Jul 23 2001 Than Ngo <than@redhat.com>
- fix build dependency (bug #49698)

* Mon Jul 16 2001 Trond Eivind Glomsrød <teg@redhat.com>
- s/Copyright/License/
- Make devel subpackage depend on main

* Mon Apr 23 2001 Than Ngo <than@redhat.com>
- update to 2.4

* Wed Feb 28 2001 Tim Powers <timp@redhat.com>
- rebuilt against new libmng

* Fri Feb 23 2001 Than Ngo <than@redhat.com>
- fix to use python1.5

* Thu Feb 22 2001 Than Ngo <than@redhat.com>
- update to 2.3 release

* Fri Feb 02 2001 Than Ngo <than@redhat.com>
- rebuild in new envoroment

* Tue Dec 26 2000 Than Ngo <than@redhat.com>
- rebuilt against qt-2.2.3
- update Url

* Mon Nov 20 2000 Tim Powers <timp@redhat.com>
- rebuilt to fix bad dir perms

* Wed Nov 8 2000 Than Ngo <than@redhat.com>
- update to 2.2
- don't apply the patch, since the gcc-2.96-62 works correct

* Mon Oct 23 2000 Than Ngo <than@redhat.com>
- update to 2.1

* Thu Aug 3 2000 Than Ngo <than@redhat.de>
- add ldconfig in %post, %postun and Prereq (Bug #15136)

* Thu Jul 27 2000 Than Ngo <than@redhat.de>
- don't hardcode Qt version

* Mon Jul 25 2000 Prospector <prospector@redhat.com>
- rebuilt

* Mon Jul 17 2000 Tim Powers <timp@redhat.com>
- added defattr to both packages

* Wed Jul 12 2000 Than Ngo <than@redhat.de>
- fix to built withe gcc-2.96

* Mon Jul 03 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sat May 27 2000 Ngo Than <than@redhat.de>
- update 0.12 for 7.0

* Mon May  8 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 0.11.1
- Qt 2.1.0

* Wed Feb  2 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 0.10.1
- Qt 1.45
- handle RPM_OPT_FLAGS

* Tue Dec 21 1999 Ngo Than <than@redhat.de>
- updated 0.10

* Tue Dec 14 1999 Ngo Than <than@redhat.de>
- 0.10pre5

* Sun Nov 28 1999 Ngo Than <than@redhat.de>
- Initial packaging as RPM for powertools-6.2
