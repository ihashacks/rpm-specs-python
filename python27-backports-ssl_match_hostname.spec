%define __python /usr/bin/python2.7
%global pyver 27
%global pybindir /usr/lib/python2.7/bin
#global pyver %{nil}

%global module_name backports.ssl_match_hostname

Name:           python%{pyver}-backports-ssl_match_hostname
Version:        3.4.0.2
Release:        1%{?dist}
Summary:        The ssl.match_hostname() function from Python 3

License:        Python
URL:            https://bitbucket.org/brandon/backports.ssl_match_hostname
Source0:        http://pypi.python.org/packages/source/b/%{module_name}/%{module_name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-setuptools
Requires:       python%{pyver}-backports

%description
The Secure Sockets layer is only actually secure if you check the hostname in
the certificate returned by the server to which you are connecting, and verify
that it matches to hostname that you are trying to reach.

But the matching logic, defined in RFC2818, can be a bit tricky to implement on
your own. So the ssl package in the Standard Library of Python 3.2 now includes
a match_hostname() function for performing this check instead of requiring
every application to implement the check separately.

This backport brings match_hostname() to users of earlier versions of Python.
The actual code inside comes verbatim from Python 3.2.


%prep
%setup -qn %{module_name}-%{version}
mv src/backports/ssl_match_hostname/README.txt ./
mv src/backports/ssl_match_hostname/LICENSE.txt ./


%build
%{__python} setup.py build


%install
%{__python} setup.py install --skip-build --root %{buildroot}
rm %{buildroot}%{python_sitelib}/backports/__init__.py*

 
%files
%doc README.txt LICENSE.txt
%{python_sitelib}/*


%changelog
* Thu Sep 18 2014 Brandon Pierce <brandon@ihashacks.com - 3.4.0.2-1
- Rebuilt for CentOS 6

* Sun Oct 27 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 3.4.0.2-1
- Update to upstream 3.4.0.2 for a security fix
- http://bugs.python.org/issue17997

* Mon Sep 02 2013 Ian Weller <iweller@redhat.com> - 3.4.0.1-1
- Update to upstream 3.4.0.1

* Mon Aug 19 2013 Ian Weller <iweller@redhat.com> - 3.2-0.5.a3
- Use python-backports instead of providing backports/__init__.py

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2-0.4.a3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon May 20 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 3.2-0.3.a3
- Add patch for CVE 2013-2099 https://bugzilla.redhat.com/show_bug.cgi?id=963260

* Tue Feb 05 2013 Ian Weller <iweller@redhat.com> - 3.2-0.2.a3
- Fix Python issue 12000

* Fri Dec 07 2012 Ian Weller <iweller@redhat.com> - 3.2-0.1.a3
- Initial package build
