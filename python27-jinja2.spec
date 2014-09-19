%define __python /usr/bin/python2.7
%if 0%{?fedora} > 12 || 0%{?rhel} > 6
%global with_python3 0
%else
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%endif

# Enable building without docs to avoid a circular dependency between this
# and python-sphinx:
%global with_docs 1

Name:		python27-jinja2
Version:	2.6
Release:	2%{?dist}
Summary:	General purpose template engine
Group:		Development/Languages
License:	BSD
URL:		http://jinja.pocoo.org/
Source0:	http://pypi.python.org/packages/source/J/Jinja2/Jinja2-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch
BuildRequires:	python27-devel
BuildRequires:	python27-setuptools
BuildRequires:	python27-markupsafe
%if 0%{?with_docs}
BuildRequires:	python27-sphinx
%endif # with_docs
Requires:	python27-babel >= 0.8
Requires:	python27-markupsafe
%if 0%{?with_python3}
BuildRequires:	python3-devel
BuildRequires:	python3-setuptools
BuildRequires:	python3-markupsafe
%endif # with_python3


%description
Jinja2 is a template engine written in pure Python.  It provides a
Django inspired non-XML syntax but supports inline expressions and an
optional sandboxed environment.

If you have any exposure to other text-based template languages, such
as Smarty or Django, you should feel right at home with Jinja2. It's
both designer and developer friendly by sticking to Python's
principles and adding functionality useful for templating
environments.


%if 0%{?with_python3}
%package -n python3-jinja2
Summary:	General purpose template engine
Group:		Development/Languages
Requires:	python3-markupsafe
# babel isn't py3k ready yet, and is only a weak dependency
#Requires:	 python3-babel >= 0.8


%description -n python3-jinja2
Jinja2 is a template engine written in pure Python.  It provides a
Django inspired non-XML syntax but supports inline expressions and an
optional sandboxed environment.

If you have any exposure to other text-based template languages, such
as Smarty or Django, you should feel right at home with Jinja2. It's
both designer and developer friendly by sticking to Python's
principles and adding functionality useful for templating
environments.
%endif # with_python3


%prep
%setup -q -n Jinja2-%{version}
perl -pi -e 's|python|/usr/bin/python2.7|' Makefile

# cleanup
find . -name '*.pyo' -o -name '*.pyc' -delete

# fix EOL
sed -i 's|\r$||g' LICENSE

%if 0%{?with_python3}
cp -a . %{py3dir}
%endif # with_python3


%build
%{__python} setup.py build

# for now, we build docs using Python 2.x and use that for both
# packages.
%if 0%{?with_docs}
make -C docs html SPHINXBUILD=sphinx-build2.7
%endif # with_docs

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif # with_python3


%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build \
	    --root %{buildroot}

# remove hidden file
rm -rf docs/_build/html/.buildinfo

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build \
	    --root %{buildroot}
popd
%endif # with_python3


%clean
rm -rf %{buildroot}


%check
make test


%if 0%{?with_python3}
pushd %{py3dir}
make test
popd
%endif # with_python3


%files
%defattr(-,root,root,-)
%doc AUTHORS CHANGES LICENSE
%if 0%{?with_docs}
%doc docs/_build/html
%endif # with_docs
%doc ext
%doc examples
%{python_sitelib}/*
%exclude %{python_sitelib}/jinja2/_debugsupport.c


%if 0%{?with_python3}
%files -n python3-jinja2
%defattr(-,root,root,-)
%doc AUTHORS CHANGES LICENSE
%if 0%{?with_docs}
%doc docs/_build/html
%endif # with_docs
%doc ext
%doc examples
%{python3_sitelib}/*
%exclude %{python3_sitelib}/jinja2/_debugsupport.c
%endif # with_python3


%changelog
* Thu Sep 18 2014 Brandon Pierce <brandon@ihashacks.com - 2.6-2
- Rebuilt for CentOS 6

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jul 25 2011 Thomas Moschny <thomas.moschny@gmx.de> - 2.6-1
- Update to 2.6.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 18 2011 Thomas Moschny <thomas.moschny@gmx.de> - 2.5.5-3
- Re-enable html doc generation.
- Remove conditional for F-12 and below.
- Do not silently fail the testsuite for with py3k.

* Mon Nov  1 2010 Michel Salim <salimma@fedoraproject.org> - 2.5.5-2
- Move python3 runtime requirements to python3 subpackage

* Wed Oct 27 2010 Thomas Moschny <thomas.moschny@gmx.de> - 2.5.5-1
- Update to 2.5.5.

* Wed Aug 25 2010 Thomas Moschny <thomas.moschny@gmx.de> - 2.5.2-4
- Revert to previous behavior: fail the build on failed test.
- Rebuild for Python 3.2.

* Wed Aug 25 2010 Dan Horák <dan[at]danny.cz> - 2.5.2-3
- %%ifnarch doesn't work on noarch package so don't fail the build on failed tests

* Wed Aug 25 2010 Dan Horák <dan[at]danny.cz> - 2.5.2-2
- disable the testsuite on s390(x)

* Thu Aug 19 2010 Thomas Moschny <thomas.moschny@gmx.de> - 2.5.2-1
- Update to upstream version 2.5.2.
- Package depends on python-markupsafe and is noarch now.

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 2.5-4
- add explicit build-requirement on python-setuptools
- fix doc disablement for python3 subpackage

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 2.5-3
- support disabling documentation in the build to break a circular build-time
dependency with python-sphinx; disable docs for now

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Jul 13 2010 Thomas Moschny <thomas.moschny@gmx.de> - 2.5-1
- Update to upstream version 2.5.
- Create python3 subpackage. 
- Minor specfile fixes.
- Add examples directory.
- Thanks to Gareth Armstrong for additional hints.

* Wed Apr 21 2010 Thomas Moschny <thomas.moschny@gmx.de> - 2.4.1-1
- Update to 2.4.1.

* Tue Apr 13 2010 Thomas Moschny <thomas.moschny@gmx.de> - 2.4-1
- Update to 2.4.

* Tue Feb 23 2010 Thomas Moschny <thomas.moschny@gmx.de> - 2.3.1-1
- Update to 2.3.1.
- Docs are built using Sphinx now.
- Run the testsuite.

* Sat Sep 19 2009 Thomas Moschny <thomas.moschny@gmx.de> - 2.2.1-1
- Update to 2.2.1, mainly a bugfix release.
- Remove patch no longer needed.
- Remove conditional for FC-8.
- Compilation of speedup module has to be explicitly requested now.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 10 2009 Thomas Moschny <thomas.moschny@gmx.de> - 2.1.1-1
- Update to 2.1.1 (bugfix release).

* Thu Dec 18 2008 Thomas Moschny <thomas.moschny@gmx.de> - 2.1-1
- Update to 2.1, which fixes a number of bugs.
  See http://jinja.pocoo.org/2/documentation/changelog#version-2-1.

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.0-3
- Rebuild for Python 2.6

* Tue Jul 22 2008 Thomas Moschny <thomas.moschny@gmx.de> - 2.0-2
- Use rpm buildroot macro instead of RPM_BUILD_ROOT.

* Sun Jul 20 2008 Thomas Moschny <thomas.moschny@gmx.de> - 2.0-1
- Upstream released 2.0.

* Sun Jun 29 2008 Thomas Moschny <thomas.moschny@gmx.de> - 2.0-0.1.rc1
- Modified specfile from the existing python-jinja package.