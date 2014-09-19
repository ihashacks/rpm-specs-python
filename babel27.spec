%define __python /usr/bin/python2.7
%global pybindir /usr/lib/python2.7/bin

%if 0%{?fedora} > 12 || 0%{?rhel} > 6
%global with_python3 0
%endif

Name:           babel27
Version:        0.9.6
Release:        2%{?dist}.1
Summary:        Tools for internationalizing Python applications

Group:          Development/Languages
License:        BSD
URL:            http://babel.edgewall.org/
Source0:        http://ftp.edgewall.com/pub/babel/Babel-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  python27-devel
BuildRequires:  python27-setuptools-devel

Requires:       python27-babel
Requires:       python27-setuptools

%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
# needed for 2to3
BuildRequires:  python-tools
%endif

%description
Babel is composed of two major parts:

* tools to build and work with gettext message catalogs

* a Python interface to the CLDR (Common Locale Data Repository),
  providing access to various locale display names, localized number
  and date formatting, etc.

%package -n python27-babel
Summary:        Library for internationalizing Python applications
Group:          Development/Languages

%description -n python27-babel
Babel is composed of two major parts:

* tools to build and work with gettext message catalogs

* a Python interface to the CLDR (Common Locale Data Repository),
  providing access to various locale display names, localized number
  and date formatting, etc.

%if 0%{?with_python3}
%package -n python3-babel
Summary:        Library for internationalizing Python applications
Group:          Development/Languages

%description -n python3-babel
Babel is composed of two major parts:

* tools to build and work with gettext message catalogs

* a Python interface to the CLDR (Common Locale Data Repository),
  providing access to various locale display names, localized number
  and date formatting, etc.
%endif

%prep
%setup0 -q -n Babel-%{version}
chmod a-x babel/messages/frontend.py doc/logo.png doc/logo_small.png
%{__sed} -i -e '/^#!/,1d' babel/messages/frontend.py

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -r . %{py3dir}
2to3 --write --nobackup %{py3dir}
%endif

%build
%{__python} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif

%install
rm -rf %{buildroot}
# install python3 build before python2 build so executables from the former
# don't overwrite those from the latter
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --no-compile --root %{buildroot}
popd
%endif

%{__python} setup.py install --skip-build --no-compile --root %{buildroot}

mkdir -p %{buildroot}%{pybindir}
mv %{buildroot}%{_bindir}/pybabel %{buildroot}%{_bindir}/pybabel2.7
ln -s %{_bindir}/pybabel2.7 %{buildroot}%{pybindir}/pybabel

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc ChangeLog COPYING README.txt doc/cmdline.txt
%{_bindir}/pybabel*
%{pybindir}/*

%files -n python27-babel
%defattr(-,root,root,-)
%doc doc
%{python_sitelib}/Babel-%{version}-py*.egg-info
%{python_sitelib}/babel

%if 0%{?with_python3}
%files -n python3-babel
%defattr(-,root,root,-)
%doc doc
%{python3_sitelib}/Babel-%{version}-py*.egg-info
%{python3_sitelib}/babel
%endif

%changelog
* Thu Sep 18 2014 Brandon Pierce <brandon@ihashacks.com - 0.9.6-2
- Rebuilt for CentOS 6

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 07 2011 Nils Philippsen <nils@redhat.com> - 0.9.6-1
- version 0.9.6:
  * Backport r493-494: documentation typo fixes.
  * Make the CLDR import script work with Python 2.7.
  * Fix various typos.
  * Fixed Python 2.3 compatibility (ticket #146, #233).
  * Sort output of list-locales.
  * Make the POT-Creation-Date of the catalog being updated equal to
    POT-Creation-Date of the template used to update (ticket #148).
  * Use a more explicit error message if no option or argument (command) is
    passed to pybabel (ticket #81).
  * Keep the PO-Revision-Date if it is not the default value (ticket #148).
  * Make --no-wrap work by reworking --width's default and mimic xgettext's
    behaviour of always wrapping comments (ticket #145).
  * Fixed negative offset handling of Catalog._set_mime_headers (ticket #165).
  * Add --project and --version options for commandline (ticket #173).
  * Add a __ne__() method to the Local class.
  * Explicitly sort instead of using sorted() and don't assume ordering
    (Python 2.3 and Jython compatibility).
  * Removed ValueError raising for string formatting message checkers if the
    string does not contain any string formattings (ticket #150).
  * Fix Serbian plural forms (ticket #213).
  * Small speed improvement in format_date() (ticket #216).
  * Fix number formatting for locales where CLDR specifies alt or draft
    items (ticket #217)
  * Fix bad check in format_time (ticket #257, reported with patch and tests by
    jomae)
  * Fix so frontend.CommandLineInterface.run does not accumulate logging
    handlers (#227, reported with initial patch by dfraser)
  * Fix exception if environment contains an invalid locale setting (#200)
- install python2 rather than python3 executable (#710880)

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Aug 26 2010 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.9.5-3
- Add python3 subpackage

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.9.5-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed Apr  7 2010 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.9.5-1
- This release contains a small number of bugfixes over the 0.9.4
- release.
-
- What's New:
- -----------
- * Fixed the case where messages containing square brackets would break
-  with an unpack error
- * Fuzzy matching regarding plurals should *NOT* be checked against
-  len(message.id) because this is always 2, instead, it's should be
-  checked against catalog.num_plurals (ticket #212).

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Mar 28 2009 Robert Scheck <robert@fedoraproject.org> - 0.9.4-4
- Added missing requires to python-setuptools for pkg_resources

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.9.4-2
- Rebuild for Python 2.6

* Mon Aug 25 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.9.4-1
- Update to 0.9.4

* Thu Jul 10 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.9.3-1
- Update to 0.9.3

* Sun Dec 16 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.9.1-1
- Update to 0.9.1

* Tue Aug 28 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.9-2
- BR python-setuptools-devel

* Mon Aug 27 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.9-1
- Update to 0.9

* Mon Jul  2 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.8.1-1
- Update to 0.8.1
- Remove upstreamed patch.

* Fri Jun 29 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.8-3
- Replace patch with one that actually applies.

* Fri Jun 29 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.8-2
- Apply upstream patch to rename command line script to "pybabel" - BZ#246208

* Thu Jun 21 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.8-1
- First version for Fedora

