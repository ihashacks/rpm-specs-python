%define __python /usr/bin/python2.7
%global pybindir /usr/lib/python2.7/bin

%if ! (0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif

%bcond_without run_testsuite

# where are all the python3 dependencies
%if 0%{?fedora} > 15
%global with_python3 0
%endif

# where are all the pypy dependencies
%if 0%{?fedora} > 15
%global with_pypy 0
%endif

Name:           ipython27
%define rname	ipython
Version:        0.13.2
Release:        1%{?dist}.1
Summary:        An enhanced interactive Python shell

Group:          Development/Libraries
# See bug #603178 for a quick overview for the choice of licenses
# most files are under BSD and just a few under Python or MIT
# There are some extensions released under GPLv2+
License:        (BSD and MIT and Python) and GPLv2+
URL:            http://ipython.org/
Source0:        http://archive.ipython.org/release/%{version}/%{rname}-%{version}.tar.gz
# will be in ipython-0.14
# https://github.com/ipython/ipython/pull/2681
Patch0:         ipython-0.13.1-dont-require-matplotlib.patch
Patch1:		ipython-0.13.2-print-syntax.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python27-devel
BuildRequires:  python27-simplegeneric

%if %{with run_testsuite}
# for checking/testing
BuildRequires:  python27-nose
BuildRequires:  python27-simplegeneric
# "Tools and libraries available at test time:"
BuildRequires:  python27-zmq
BuildRequires:  python27-zmq-tests
BuildRequires:  pexpect27
BuildRequires:  python27-matplotlib
#BuildRequires:  python-matplotlib-tk
BuildRequires:  pymongo27
BuildRequires:  PyQt427
# for frontend
BuildRequires:  python27-pygments
# for running qt/matplotlib tests
BuildRequires:  xorg-x11-server-Xvfb
%endif

# Require $current_python_interpreter-ipython
Requires:       python27-ipython

# add python3 packages
%if 0%{?with_python3}
BuildRequires:  python3-devel
# for checking/testing
BuildRequires:  python3-nose
BuildRequires:  python3-mglob
BuildRequires:  python3-simplegeneric
# "Tools and libraries available at test time:"
BuildRequires:  python3-zmq
BuildRequires:  python3-zmq-tests
BuildRequires:  python3-tornado
BuildRequires:  python3-pexpect
BuildRequires:  python3-matplotlib
#BuildRequires:  python3-matplotlib-tk
BuildRequires:  python3-pymongo
BuildRequires:  python3-PyQt4
# for frontend
BuildRequires:  python3-pygments

Requires:       python3-zmq
%endif

%global ipython_desc_base \
IPython provides a replacement for the interactive Python interpreter with\
extra functionality.\
\
Main features:\
 * Comprehensive object introspection.\
 * Input history, persistent across sessions.\
 * Caching of output results during a session with automatically generated\
   references.\
 * Readline based name completion.\
 * Extensible system of 'magic' commands for controlling the environment and\
   performing many tasks related either to IPython or the operating system.\
 * Configuration system with easy switching between different setups (simpler\
   than changing $PYTHONSTARTUP environment variables every time).\
 * Session logging and reloading.\
 * Extensible syntax processing for special purpose situations.\
 * Access to the system shell with user-extensible alias system.\
 * Easily embeddable in other Python programs.\
 * Integrated access to the pdb debugger and the Python profiler.

%description
%{ipython_desc_base}

%package -n python27-ipython
Summary:        An enhanced interactive Python shell
Requires:       python27-ipython-console = %{version}-%{release}
Requires:       python27-ipython-gui = %{version}-%{release}
Requires:       python27-ipython-notebook = %{version}-%{release}
Provides:       ipython27 = %{version}-%{release}
Obsoletes:      ipython27 < 0.13-1
%description -n python27-ipython
%{ipython_desc_base}

%package -n python27-ipython-console
Summary:        An enhanced interactive Python shell
Requires:       python27-zmq


#bundled libs
Requires:       pexpect27
Requires:       python27-mglob
Requires:       python27-simplegeneric

%description -n python27-ipython-console
%{ipython_desc_base}


%package -n python27-ipython-notebook
Summary:        An enhanced interactive Python shell
Requires:       python27-ipython-console = %{version}-%{release}
Requires:       python27-tornado
Requires:       python27-matplotlib
Provides:       ipython27-notebook = %{version}-%{release}

%description -n python27-ipython-notebook
%{ipython_desc_base}

This package contains the ipython notebook.


%package -n python27-ipython-tests
Summary:        Tests for %{name}
Group:          Documentation
Requires:       python27-nose
Requires:       python27-zmq-tests
Requires:       python27-ipython-console = %{version}-%{release}
Provides:       ipython27-tests = %{version}-%{release}
Obsoletes:      ipython27-tests < 0.13-1
%description -n python27-ipython-tests
This package contains the tests of %{name}.
You can check this way, if ipython works on your platform.

%package -n python27-ipython-doc
Summary:        Documentation for %{name}
Group:          Documentation
Provides:       ipython27-doc = %{version}-%{release}
Obsoletes:      ipython27-doc < 0.13-1
%description -n python27-ipython-doc
This package contains the documentation of %{name}.


%package -n python27-ipython-gui
Summary:        Gui applications from %{name}
Group:          Applications/Editors
Requires:       python27-ipython-console = %{version}-%{release}
Requires:       PyQt427
Requires:       python27-matplotlib
Requires:       python27-pygments
Provides:       ipython27-gui = %{version}-%{release}
Obsoletes:      ipython27-gui < 0.13-1
%description -n python27-ipython-gui
This package contains the gui of %{name}, which requires PyQt.



%if 0%{?with_python3}
# TODO revisit python3 packages again, once python2 restructuring is done
%package -n python3-ipython
Summary:        An enhanced interactive Python shell
Requires:       python3-ipython-console = %{version}-%{release}
Requires:       python3-ipython-gui = %{version}-%{release}
Requires:       python3-ipython-notebook = %{version}-%{release}
%description -n python3-ipython
%{ipython_desc_base}

%package -n python3-ipython-console
Summary:        An enhanced interactive Python shell
Requires:       python3-zmq


#bundled libs
Requires:       python3-pexpect
Requires:       python3-mglob
Requires:       python3-simplegeneric

%description -n python3-ipython-console
%{ipython_desc_base}


%package -n python3-ipython-notebook
Summary:        An enhanced interactive Python shell
Requires:       python3-ipython-console = %{version}-%{release}
Requires:       python3-tornado
Requires:       python3-matplotlib

%description -n python3-ipython-notebook
%{ipython_desc_base}

This package contains the ipython notebook.


%package -n python3-ipython-tests
Summary:        Tests for %{name}
Group:          Documentation
Requires:       python3-nose
Requires:       python3-zmq-tests
Requires:       python3-ipython-console = %{version}-%{release}
%description -n python3-ipython-tests
This package contains the tests of %{name}.
You can check this way, if ipython works on your platform.

%package -n python3-ipython-doc
Summary:        Documentation for %{name}
Group:          Documentation
%description -n python3-ipython-doc
This package contains the documentation of %{name}.

%package -n python3-ipython-gui
Summary:        Gui applications from %{name}
Group:          Applications/Editors
Requires:       python3-ipython-console = %{version}-%{release}
Requires:       python3-PyQt4
Requires:       python3-matplotlib
Requires:       python3-pygments
%description -n python3-ipython-gui
This package contains the gui of %{name}, which requires PyQt.

%endif # with_python3



%prep
%setup -q -n %{rname}-%{version}

%patch0 -p 1
%patch1 -p 0

# delete bundling libs
pushd IPython/external
# python's own modules
rm argparse/_argparse.py

# use decorators of numpy
rm decorators/_decorators.py

# other packages exist in fedora
rm simplegeneric/_simplegeneric.py
%if ! 0%{?with_python3}
# bundle this on python3 in experimental version for now
rm pexpect/_pexpect.py
%endif

# rejected in a PEP, probably no upstream
#rm Itpl/_Itpl.py

# available at pypi
#rm path/_path.py

# ssh modules from paramiko

popd

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'
%endif # with_python3


%build
%if 0%{?with_python3}
pushd %{py3dir}
    %{__python3} setup.py build
popd
%endif # with_python3

%{__python} setup.py build


%install
rm -rf %{buildroot}
%if 0%{?with_python3}
pushd %{py3dir}
    %{__python3} setup.py install -O1 --skip-build --root %{buildroot} 
    # ipython installs docs automatically, but in the wrong place
    #TODO verify this
    #mv %{buildroot}%{_datadir}/doc/python3-%{name} \
    #    %{buildroot}%{_datadir}/doc/python3-%{name}-%{version}

popd
%endif # with_python3

%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# ipython installs docs automatically, but in the wrong place
mv %{buildroot}%{_datadir}/doc/ipython \
    %{buildroot}%{_datadir}/doc/%{name}-%{version}

mkdir -p %{buildroot}%{pybindir}
for i in %{buildroot}%{_bindir}/*; do
	j=`basename $i`
	mv $i ${i}27
	#ln -s %{_bindir}/${j}27 %{buildroot}%{pybindir}/$j
	ln -s ../../../bin/${j}27 %{buildroot}%{pybindir}/$j
done
pushd %{buildroot}%{_mandir}/man1
	rename .1 27.1 *
popd

%clean
rm -rf %{buildroot}


%if %{with run_testsuite}
%check
# Ensure that the user's .pythonrc.py is not invoked during any tests.
export PYTHONSTARTUP=""
#####################################################################
# Reasons for ignoring tests below:
# * FAIL: Verify that plot is available when pylab_import_all = True
#----------------------------------------------------------------------
#Traceback (most recent call last):
#    File "/builddir/build/BUILDROOT/ipython-0.13.2-1.fc20.noarch/usr/lib/python2.7/site-packages/IPython/testing/decorators.py", line 228, in skipper_func
#        return f(*args, **kwargs)
#    File "/builddir/build/BUILDROOT/ipython-0.13.2-1.fc20.noarch/usr/lib/python2.7/site-packages/IPython/testing/decorators.py", line 228, in skipper_func
#        return f(*args, **kwargs)
#    File "/builddir/build/BUILDROOT/ipython-0.13.2-1.fc20.noarch/usr/lib/python2.7/site-packages/IPython/lib/tests/test_irunner_pylab_magic.py", line 92, in test_pylab_import_all_enabled
#        self._test_runner(runner,source,output)
#    File "/builddir/build/BUILDROOT/ipython-0.13.2-1.fc20.noarch/usr/lib/python2.7/site-packages/IPython/lib/tests/test_irunner_pylab_magic.py", line 53, in _test_runner
#        self.fail(message)
#    AssertionError: Mismatch in number of lines
#    Expected:
#    ~~~~~~~~~
#    In \[1\]: from IPython\.config\.application import Application
#    In \[2\]: app = Application\.instance\(\)
#    In \[3\]: app\.pylab_import_all = True
#    In \[4\]: pylab
#    ^Welcome to pylab, a matplotlib-based Python environment
#    For more information, type 'help\(pylab\)'\.
#    In \[5\]: ip=get_ipython\(\)
#    In \[6\]: 'plot' in ip\.user_ns
#    Out\[6\]: True
#    Got:
#    ~~~~~~~~~
#    In [1]: from IPython.config.application import Application
#    In [2]: app = Application.instance()
#    In [3]: app.pylab_import_all = True
#    In [4]: pylab
#    Xlib:  extension "RANDR" missing on display ":99".
#    Welcome to pylab, a matplotlib-based Python environment [backend: GTKAgg].
#    For more information, type 'help(pylab)'.
#    In [5]: ip=get_ipython()
#    In [6]: 'plot' in ip.user_ns
#    Out[6]: True
#        """Fail immediately, with the given message."""
#### -> ignoring test_pylab_import_all_disabled|test_pylab_import_all_enabled
#####################################################################
# No *EXCLUDE_TESTS may be empty. Write NONE in such a case.
# %global COMMON_EXCLUDE_TESTS NONE
%global COMMON_EXCLUDE_TESTS test_not_writable_ipdir
%global PYTHON3EXCLUDE_TESTS NONE
%global PYTHON2EXCLUDE_TESTS test_pylab_import_all_disabled|test_pylab_import_all_enabled


%global EXCLUDE_TESTS_3 "%{COMMON_EXCLUDE_TESTS}|%{PYTHON3EXCLUDE_TESTS}"
%global EXCLUDE_TESTS_2 "%{COMMON_EXCLUDE_TESTS}|%{PYTHON2EXCLUDE_TESTS}"

%if 0%{?with_python3}
pushd %{py3dir}
PYTHONPATH=%{buildroot}%{python3_sitelib} \
    PATH="%{buildroot}%{_bindir}:$PATH" \
    LC_ALL=en_US.UTF-8 \
    xvfb-run \
    %{buildroot}%{_bindir}/iptest3 -v -e %{EXCLUDE_TESTS_3}
popd
%endif

. /etc/profile.d/modules.sh; module load python
# TODO no ipython in path in koji
PYTHONPATH=%{buildroot}%{python_sitelib} \
    PATH="%{buildroot}%{_bindir}:%{buildroot}%{pybindir}:$PATH" \
    LC_ALL=en_US.UTF-8 \
    xvfb-run \
    %{buildroot}%{_bindir}/iptest27 -v -e %{EXCLUDE_TESTS_2}
%endif

%files -n python27-ipython
%defattr(-,root,root,-)

%files -n python27-ipython-console
%defattr(-,root,root,-)
%{_bindir}/ipython*
%{pybindir}/ipython*
%{_bindir}/irunner*
%{pybindir}/irunner*
%{_bindir}/pycolor*
%{pybindir}/pycolor*
%{_bindir}/ipcluster*
%{pybindir}/ipcluster*
%{_bindir}/ipcontroller*
%{pybindir}/ipcontroller*
%{_bindir}/ipengine*
%{pybindir}/ipengine*
%{_bindir}/iplogger*
%{pybindir}/iplogger*
%{_mandir}/man*/ipython*
%{_mandir}/man*/ipengine*
%{_mandir}/man*/irunner*
%{_mandir}/man*/pycolor*
%{_mandir}/man*/ipc*
%{_mandir}/man*/iplogger*

%dir %{python_sitelib}/IPython
%{python_sitelib}/IPython/external
%{python_sitelib}/IPython/*.py*
%dir %{python_sitelib}/IPython/kernel
%{python_sitelib}/IPython/kernel/*.py*
%dir %{python_sitelib}/IPython/testing
%{python_sitelib}/IPython/testing/*.py*
%{python_sitelib}/IPython/testing/plugin
%{python_sitelib}/ipython-%{version}-py?.?.egg-info

%{python_sitelib}/IPython/config/
%{python_sitelib}/IPython/core/
%{python_sitelib}/IPython/extensions/
%dir %{python_sitelib}/IPython/frontend/
%{python_sitelib}/IPython/frontend/terminal/
%{python_sitelib}/IPython/frontend/__init__.py*
%{python_sitelib}/IPython/frontend/consoleapp.py*
%{python_sitelib}/IPython/lib/
%{python_sitelib}/IPython/nbformat/
%{python_sitelib}/IPython/parallel/
%{python_sitelib}/IPython/scripts/
%{python_sitelib}/IPython/utils/
%{python_sitelib}/IPython/zmq/
%exclude %{python_sitelib}/IPython/zmq/gui/

# tests go into subpackage
%exclude %{python_sitelib}/IPython/*/tests/
%exclude %{python_sitelib}/IPython/*/*/tests


%files -n python27-ipython-tests
%defattr(-,root,root,-)
%{_bindir}/iptest*
%{pybindir}/iptest
%{python_sitelib}/IPython/*/tests
%{python_sitelib}/IPython/*/*/tests


%files -n python27-ipython-doc
%defattr(-,root,root,-)
# ipython installs its own documentation, but we need to own the directory
%{_datadir}/doc/%{name}-%{version}


%files -n python27-ipython-notebook
%defattr(-,root,root,-)
%{python_sitelib}/IPython/frontend/html/


%files -n python27-ipython-gui
%defattr(-,root,root,-)
%{python_sitelib}/IPython/zmq/gui
%{python_sitelib}/IPython/frontend/qt/

%if 0%{?with_python3}
%files -n python3-ipython
%defattr(-,root,root,-)

%files -n python3-ipython-console
%defattr(-,root,root,-)
%{_bindir}/ipython3
%{_bindir}/irunner3
%{_bindir}/pycolor3
%{_bindir}/ipcluster3
%{_bindir}/ipcontroller3
%{_bindir}/ipengine3
%{_bindir}/iplogger3
# no man pages (yet?)
#%{_mandir}/man*/ipython3.*
#%{_mandir}/man*/ipengine3*
#%{_mandir}/man*/irunner3*
#%{_mandir}/man*/pycolor3*
#%{_mandir}/man*/ipc*3*
#%{_mandir}/man*/iplogger3*

%dir %{python3_sitelib}/IPython
%{python3_sitelib}/IPython/external
%{python3_sitelib}/IPython/__pycache__/
%{python3_sitelib}/IPython/*.py*
%dir %{python3_sitelib}/IPython/kernel
%{python3_sitelib}/IPython/kernel/__pycache__/
%{python3_sitelib}/IPython/kernel/*.py*
%dir %{python3_sitelib}/IPython/testing
%{python3_sitelib}/IPython/testing/__pycache__/
%{python3_sitelib}/IPython/testing/*.py*
%{python3_sitelib}/IPython/testing/plugin
%{python3_sitelib}/ipython-%{version}-py?.?.egg-info

%{python3_sitelib}/IPython/config/
%{python3_sitelib}/IPython/core/
%{python3_sitelib}/IPython/extensions/
%dir %{python3_sitelib}/IPython/frontend/
%{python3_sitelib}/IPython/frontend/terminal/
%{python3_sitelib}/IPython/frontend/__pycache__/
%{python3_sitelib}/IPython/frontend/__init__.py*
%{python3_sitelib}/IPython/frontend/consoleapp.py*
%{python3_sitelib}/IPython/lib/
%{python3_sitelib}/IPython/nbformat/
%{python3_sitelib}/IPython/parallel/
%{python3_sitelib}/IPython/scripts/
%{python3_sitelib}/IPython/utils/
%{python3_sitelib}/IPython/zmq/
%exclude %{python3_sitelib}/IPython/zmq/gui/

# tests go into subpackage
%exclude %{python3_sitelib}/IPython/*/tests/
%exclude %{python3_sitelib}/IPython/*/*/tests


%files -n python3-ipython-tests
%defattr(-,root,root,-)
%{_bindir}/iptest3
%{python3_sitelib}/IPython/*/tests
%{python3_sitelib}/IPython/*/*/tests


##%files -n python3-ipython-doc
##%defattr(-,root,root,-)
# ipython installs its own documentation, but we need to own the directory
##%{_datadir}/doc/python3-%{name}-%{version}


%files -n python3-ipython-notebook
%defattr(-,root,root,-)
%{python3_sitelib}/IPython/frontend/html/


%files -n python3-ipython-gui
%defattr(-,root,root,-)
%{python3_sitelib}/IPython/zmq/gui
%{python3_sitelib}/IPython/frontend/qt/
%endif # with_python3

%changelog
* Thu Sep 18 2014 Brandon Pierce <brandon@ihashacks.com - 0.13.2-1
- Rebuilt for CentOS 6

* Sat Apr  6 2013 Thomas Spura <tomspur@fedoraproject.org> - 0.13.2-1
- update to 0.13.2 fixes #927169, #947633
- run tests in xvfb
- reword description of ipython-tests a bit

* Thu Feb 21 2013 Thomas Spura <tomspur@fedoraproject.org> - 0.13.1-4
- More changes to build for Python 3 (mostly by Andrew McNabb, #784947)
- Update package structure of python3-ipython subpackage to match python2-ipython one's
- enable python3 build of ipython
- exclude pylab tests for now, as it is broken on python3

* Thu Feb 21 2013 Thomas Spura <tomspur@fedoraproject.org> - 0.13.1-3
- obsolete old Thu Feb 21 2013 python packages (José Matos, #882724)
- notebook and gui subpackage require matplotlib not the console anymore (#872176)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Oct 24 2012 Thomas Spura <tomspur@fedoraproject.org> - 0.13.1-1
- update to 0.13.1 (#838031)
- run tests with en_US.UTF-8

* Thu Aug 30 2012 Thomas Spura <tomspur@fedoraproject.org> - 0.13-5
- add empty python-ipython files section
- obsolete ipython

* Wed Aug  8 2012 Thomas Spura <tomspur@fedoraproject.org> - 0.13-4
- use versioned requires/provides on ipython

* Sat Aug  4 2012 Thomas Spura <tomspur@fedoraproject.org> - 0.13-3
- use python-foo for python2-foo and provide ipython-foo

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 30 2012 Thomas Spura <tomspur@fedoraproject.org> - 0.13-1
- update to new version
- R on mglob/pyparsing is obsolete
- remove patch, as it's upstream

* Fri Jan 27 2012 Thomas Spura <tomspur@fedoraproject.org> - 0.12-3
- skip no X tests
- continue with python3 support

* Sun Jan  8 2012 Thomas Spura <tomspur@fedoraproject.org> - 0.12-2
- add missing R tornado
- add _bindir to PATH to more tests pass in koji

* Mon Dec 19 2011 Thomas Spura <tomspur@fedoraproject.org> - 0.12-1
- update to new version
- bcond_without run_testsuite

* Sun Oct 23 2011 Thomas Spura <tomspur@fedoraproject.org> - 0.11-3
- add more missing R (matplotlib and pygments) (#748141)

* Tue Sep 20 2011 Michel Salim <salimma@fedoraproject.org> - 0.11-2
- make -gui subpackage depend on PyQt4, not PyQt

* Mon Jul  4 2011 Thomas Spura <tomspur@fedoraproject.org> - 0.11-1
- update to 0.11
- patches included upstream
- ipython changed bundled pretty, so redistributes it in lib now
- run testsuite
- new upstream url

* Sat Apr  9 2011 Thomas Spura <tomspur@fedoraproject.org> - 0.10.2-1
- update to new version
- patch3 is included upstream
- fixes #663823, #649281

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov 15 2010 Thomas Spura <tomspur@fedoraproject.org> - 0.10.1-3
- add fix for #646079 and use upstream fix for #628742

* Mon Oct 18 2010 Thomas Spura <tomspur@fedoraproject.org> - 0.10.1-2
- argparse is in python 2.7 and 3.2

* Wed Oct 13 2010 Thomas Spura <tomspur@fedoraproject.org> - 0.10.1-1
- unbundle a bit differently
- update to new version

* Tue Aug 31 2010 Thomas Spura <tomspur@fedoraproject.org> - 0.10-8
- pycolor: wrong filename -> no crash (#628742)

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.10-7
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Mon Jul 19 2010 Thomas Spura <tomspur@fedoraproject.org> - 0.10-6
- add missing dependencies: pexpect and python-argparse

* Tue Jun 22 2010 Thomas Spura <tomspur@fedoraproject.org> - 0.10-5
- two more unbundled libraries in fedora

* Mon Jun 21 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 0.10-4
- Update patch for import in argparse

* Fri Jun 11 2010 Thomas Spura <tomspur@fedoraproject.org> - 0.10-3
- fix license tag (#603178)
- add requires on wxpython to gui subpackage (#515570)
- start unbundling the libraries - more to come (#603937)

* Tue Apr 13 2010 Thomas Spura <tomspur@fedoraproject.org> - 0.10-2
- move docs into a subpackage
- subpackage wxPython
- subpackage tests
- use proper %%{python_site*} definitions
- make %%{files} more explicit
- add some missing R (fixes #529185, #515570)

* Tue Sep 22 2009 James Bowes <jbowes@redhat.com> - 0.10-1
- Update to 0.10

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Dec 04 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.9.1-2
- Rebuild for Python 2.6

* Tue Dec 02 2008 James Bowes <jbowes@redhat.com> - 0.9.1-1
- Update to 0.9.1, specfile changes courtesy Greg Swift

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.8.4-2
- Rebuild for Python 2.6

* Wed Jun 11 2008 James Bowes <jbowes@redhat.com> - 0.8.4-1
- Update to 0.8.4

* Fri May 30 2008 James Bowes <jbowes@redhat.com> - 0.8.3-1
- Update to 0.8.3

* Wed Dec 12 2007 James Bowes <jbowes@redhat.com> - 0.8.2-1
- Update to 0.8.2

* Sun Aug 05 2007 James Bowes <jbowes@redhat.com> - 0.8.1-2
- Remove explicit requires on python-abi.

* Sun Aug 05 2007 James Bowes <jbowes@redhat.com> - 0.8.1-1
- Update to 0.8.1

* Thu Dec 14 2006 Jason L Tibbitts III <tibbs@math.uh.edu> - 0.7.2-4
- Rebuild for new Python

* Sat Sep 16 2006 Shahms E. King <shahms@shahms.com> - 0.7.2-3
- Rebuild for FC6

* Fri Aug 11 2006 Shahms E. King <shahms@shahms.com> - 0.7.2-2
- Include, don't ghost .pyo files per new guidelines

* Mon Jun 12 2006 Shahms E. King <shahms@shahms.com> - 0.7.2-1
- Update to new upstream version

* Mon Feb 13 2006 Shahms E. King <shahms@shahms.com> - 0.7.1.fix1-2
- Rebuild for FC-5

* Mon Jan 30 2006 Shahms E. King <shahms@shahms.com> - 0.7.1.fix1-1
- New upstream 0.7.1.fix1 which fixes KeyboardInterrupt handling

* Tue Jan 24 2006 Shahms E. King <shahms@shahms.com> - 0.7.1-1
- Update to new upstream 0.7.1

* Thu Jan 12 2006 Shahms E. King <shahms@shahms.com> - 0.7-1
- Update to new upstream 0.7.0

* Mon Jun 13 2005 Shahms E. King <shahms@shahms.com> - 0.6.15-1
- Add dist tag
- Update to new upstream (0.6.15)

* Wed Apr 20 2005 Shahms E. King <shahms@shahms.com> - 0.6.13-2
- Fix devel release number

* Mon Apr 18 2005 Shahms E. King <shahms@shahms.com> - 0.6.13-1
- Update to new upstream version

* Fri Apr  1 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.6.12-2
- Include IPython Extensions and UserConfig directories.

* Fri Mar 25 2005 Shahms E. King <shahms@shahms.com> - 0.6.12-1
- Update to 0.6.12
- Removed unused python_sitearch define

* Tue Mar 01 2005 Shahms E. King <shahms@shahms.com> - 0.6.11-2
- Fix up %%doc file specifications
- Use offical .tar.gz, not upstream .src.rpm .tar.gz

* Tue Mar 01 2005 Shahms E. King <shahms@shahms.com> - 0.6.11-1
- Initial release to meet Fedora packaging guidelines
