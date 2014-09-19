%define __python /usr/bin/python2.7
%global pybindir /usr/lib/python2.7/bin

%if 0%{?fedora} >= 18
%global with_python3            1
%global basepy3dir              %(echo ../`basename %{py3dir}`)
%else
%global with_python3            0
%endif
%global __provides_exclude_from	.*/site-packages/.*\\.so$
%global with_html               0

# On RHEL 7 onwards, don't build with wx:
%if 0%{?rhel} >= 7
%global with_wx 0
%else
%global with_wx 1
%endif


Name:           python27-matplotlib
Version:        1.2.0
Release:        8%{?dist}
Summary:        Python 2D plotting library
Group:          Development/Libraries
License:        Python
URL:            http://matplotlib.org
#Modified Sources to remove the one undistributable file
#See generate-tarball.sh in fedora cvs repository for logic
#sha1sum matplotlib-1.2.0-without-gpc.tar.gz
#92ada4ef4e7374d67e46e30bfb08c3fed068d680  matplotlib-1.2.0-without-gpc.tar.gz
Source0:        matplotlib-%{version}-without-gpc.tar.gz

Patch0:         python-matplotlib-noagg.patch
Patch1:         python-matplotlib-tk.patch
# http://sourceforge.net/mailarchive/message.php?msg_id=30202451
# https://github.com/matplotlib/matplotlib/pull/1666
# https://bugzilla.redhat.com/show_bug.cgi?id=896182
Patch2:         python-matplotlib-fontconfig.patch

BuildRequires:  agg-devel
BuildRequires:  freetype-devel
BuildRequires:  gtk2-devel
BuildRequires:  libpng-devel
BuildRequires:  numpy27
BuildRequires:  pycairo27-devel
BuildRequires:  pygtk227-devel
BuildRequires:  pyparsing27
BuildRequires:  python27-dateutil
BuildRequires:  python27-devel
BuildRequires:  pytz27
BuildRequires:  xorg-x11-server-Xvfb
BuildRequires:  zlib-devel
BuildRequires:	environment-modules
Requires:       dejavu-sans-fonts
Requires:       dvipng
Requires:       numpy27
Requires:       pycairo27
Requires:       pygtk227
Requires:       pyparsing27
Requires:       python27-dateutil
Requires:       pytz27

%description
Matplotlib is a python 2D plotting library which produces publication
quality figures in a variety of hardcopy formats and interactive
environments across platforms. matplotlib can be used in python
scripts, the python and ipython shell, web application servers, and
six graphical user interface toolkits.

Matplotlib tries to make easy things easy and hard things possible.
You can generate plots, histograms, power spectra, bar charts,
errorcharts, scatterplots, etc, with just a few lines of code.

%package        qt4
Summary:        Qt4 backend for python-matplotlib
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
BuildRequires:  PyQt427-devel
Requires:       PyQt427

%description    qt4
%{summary}

%package        tk
Summary:        Tk backend for python-matplotlib
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
BuildRequires:  tcl-devel
BuildRequires:  tkinter27
BuildRequires:  tk-devel
Requires:       tkinter27

%description    tk
%{summary}

%if %{with_wx}
%package        wx
Summary:        wxPython backend for python-matplotlib
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
BuildRequires:  wxPython27-devel
Requires:       wxPython27

%description    wx
%{summary}
%endif # with_wx

%package        doc
Summary:        Documentation files for python-matplotlib
Group:          Documentation
Requires:       %{name}%{?_isa} = %{version}-%{release}
%if %{with_html}
BuildRequires:  python27-sphinx
BuildRequires:  tex(latex)
BuildRequires:  dvipng
%endif

%description    doc
%{summary}

%if %{with_python3}
%package -n     python3-matplotlib
Summary:        Python 2D plotting library
Group:          Development/Libraries
BuildRequires:  python3-cairo
BuildRequires:  python3-dateutil
BuildRequires:  python3-devel
BuildRequires:  python3-gobject
BuildRequires:  python3-numpy
BuildRequires:  python3-pyparsing
BuildRequires:  python3-pytz
BuildRequires:  python3-six
Requires:       python3-numpy
Requires:       python3-cairo
Requires:       python3-pyparsing
Requires:       python3-dateutil
Requires:       python3-pytz

%description -n python3-matplotlib
Matplotlib is a python 2D plotting library which produces publication
quality figures in a variety of hardcopy formats and interactive
environments across platforms. matplotlib can be used in python
scripts, the python and ipython shell, web application servers, and
six graphical user interface toolkits.

Matplotlib tries to make easy things easy and hard things possible.
You can generate plots, histograms, power spectra, bar charts,
errorcharts, scatterplots, etc, with just a few lines of code.

%package -n     python3-matplotlib-qt4
Summary:        Qt4 backend for python3-matplotlib
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
BuildRequires:  python3-PyQt4-devel
Requires:       python3-PyQt4

%description -n python3-matplotlib-qt4
%{summary}

%package -n     python3-matplotlib-tk
Summary:        Tk backend for python3-matplotlib
Group:          Development/Libraries
Requires:       python3-matplotlib%{?_isa} = %{version}-%{release}
BuildRequires:  python3-tkinter
Requires:       python3-tkinter

%description -n python3-matplotlib-tk
%{summary}
%endif

%prep
%setup -q -n matplotlib-%{version}

# Remove bundled libraries
rm -r agg24 lib/matplotlib/pyparsing_py?.py

# Remove references to bundled libraries
%patch0 -p1 -b .noagg
sed -i -e s/matplotlib\.pyparsing_py./pyparsing/g lib/matplotlib/*.py

# Correct tcl/tk detection
%patch1 -p1 -b .tk
sed -i -e 's|@@libdir@@|%{_libdir}|' setupext.py

# Use fontconfig by default
%patch2 -p1 -b .fontconfig

chmod -x lib/matplotlib/mpl-data/images/*.svg

%if %{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif

%build
. /etc/profile.d/modules.sh
module load python/2.7
xvfb-run %{__python} setup.py build
%if %{with_html}
# Need to make built matplotlib libs available for the sphinx extensions:
pushd doc
    export PYTHONPATH=`cd ../build/lib.linux* && pwd`
    %{__python} make.py html
popd
%endif
# Ensure all example files are non-executable so that the -doc
# package doesn't drag in dependencies
find examples -name '*.py' -exec chmod a-x '{}' \;

%if %{with_python3}
pushd %{py3dir}
    xvfb-run %{__python3} setup.py build
    # documentation cannot be built with python3 due to syntax errors
    # and building with python 2 exits with cryptic error messages
popd
%endif

%install
%{__python} setup.py install -O1 --skip-build --root=$RPM_BUILD_ROOT
chmod +x $RPM_BUILD_ROOT%{python_sitearch}/matplotlib/dates.py
rm -rf $RPM_BUILD_ROOT%{python_sitearch}/matplotlib/mpl-data/fonts

%if %{with_python3}
pushd %{py3dir}
    %{__python3} setup.py install -O1 --skip-build --root=$RPM_BUILD_ROOT
    chmod +x $RPM_BUILD_ROOT%{python3_sitearch}/matplotlib/dates.py
    rm -rf $RPM_BUILD_ROOT%{python3_sitearch}/matplotlib/mpl-data/fonts
    rm -f $RPM_BUILD_ROOT%{python3_sitearch}/six.py
popd
%endif

%files
%doc README.txt
%doc lib/dateutil_py2/LICENSE
%doc lib/matplotlib/mpl-data/fonts/ttf/LICENSE_STIX
%doc lib/pytz/LICENSE.txt
%doc CHANGELOG
%doc CXX
%doc INSTALL
%doc PKG-INFO
%doc TODO
%{python_sitearch}/*egg-info
%{python_sitearch}/matplotlib/
%{python_sitearch}/mpl_toolkits/
%{python_sitearch}/pylab.py*
%exclude %{python_sitearch}/matplotlib/backends/backend_qt4.*
%exclude %{python_sitearch}/matplotlib/backends/backend_qt4agg.*
%exclude %{python_sitearch}/matplotlib/backends/backend_tkagg.*
%exclude %{python_sitearch}/matplotlib/backends/tkagg.*
%exclude %{python_sitearch}/matplotlib/backends/_tkagg.so
%exclude %{python_sitearch}/matplotlib/backends/backend_wx.*
%exclude %{python_sitearch}/matplotlib/backends/backend_wxagg.*

%files qt4
%{python_sitearch}/matplotlib/backends/backend_qt4.*
%{python_sitearch}/matplotlib/backends/backend_qt4agg.*

%files tk
%{python_sitearch}/matplotlib/backends/backend_tkagg.py*
%{python_sitearch}/matplotlib/backends/tkagg.py*
%{python_sitearch}/matplotlib/backends/_tkagg.so

%if %{with_wx}
%files wx
%{python_sitearch}/matplotlib/backends/backend_wx.*
%{python_sitearch}/matplotlib/backends/backend_wxagg.*
%endif # with_wx

%files doc
%doc examples
%if %{with_html}
%doc doc/build/html/*
%endif

%if %{with_python3}
%files -n python3-matplotlib
%doc %{basepy3dir}/README.txt
%doc %{basepy3dir}/lib/dateutil_py3/LICENSE
%doc %{basepy3dir}/lib/matplotlib/mpl-data/fonts/ttf/LICENSE_STIX
%doc %{basepy3dir}/lib/pytz/LICENSE.txt
%doc %{basepy3dir}/CHANGELOG
%doc %{basepy3dir}/CXX
%doc %{basepy3dir}/INSTALL
%doc %{basepy3dir}/PKG-INFO
%doc %{basepy3dir}/TODO
%{python3_sitearch}/*egg-info
%{python3_sitearch}/matplotlib/
%{python3_sitearch}/mpl_toolkits/
%{python3_sitearch}/pylab.py*
%{python3_sitearch}/__pycache__/*
%exclude %{python3_sitearch}/matplotlib/backends/backend_qt4.*
%exclude %{python3_sitearch}/matplotlib/backends/backend_qt4agg.*
%exclude %{python3_sitearch}/matplotlib/backends/backend_tkagg.*
%exclude %{python3_sitearch}/matplotlib/backends/backend_tkagg.*
%exclude %{python3_sitearch}/matplotlib/backends/tkagg.*
%exclude %{python3_sitearch}/matplotlib/backends/_tkagg.*

%files -n python3-matplotlib-qt4
%{python_sitearch}/matplotlib/backends/backend_qt4.*
%{python_sitearch}/matplotlib/backends/backend_qt4agg.*

%files -n python3-matplotlib-tk
%{python3_sitearch}/matplotlib/backends/backend_tkagg.py*
%{python3_sitearch}/matplotlib/backends/tkagg.*
%{python3_sitearch}/matplotlib/backends/_tkagg.*
%endif

%changelog
* Thu Sep 18 2014 Brandon Pierce <brandon@ihashacks.com - 1.2.0-8
- Rebuilt for CentOS 6

* Wed Jan 16 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 1.2.0-8
- Update fontconfig patch to apply issue found by upstream
- Update fontconfig patch to apply issue with missing afm fonts (#896182)

* Wed Jan 16 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 1.2.0-7
- Use fontconfig by default (#885307)

* Thu Jan  3 2013 David Malcolm <dmalcolm@redhat.com> - 1.2.0-6
- remove wx support for rhel >= 7

* Tue Dec 04 2012 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 1.2.0-5
- Reinstantiate wx backend for python2.x.
- Run setup.py under xvfb-run to detect and default to gtk backend (#883502)
- Split qt4 backend subpackage and add proper requires for it.
- Correct wrong regex in tcl libdir patch.

* Tue Nov 27 2012 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 1.2.0-4
- Obsolete python-matplotlib-wx for clean updates.

* Tue Nov 27 2012 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 1.2.0-3
- Enable python 3 in fc18 as build requires are now available (#879731)

* Thu Nov 22 2012 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 1.2.0-2
- Build python3 only on f19 or newer (#837156)
- Build requires python3-six if building python3 support (#837156)

* Thu Nov 22 2012 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 1.2.0-1
- Update to version 1.2.0
- Revert to regenerate tarball with generate-tarball.sh (#837156)
- Assume update to 1.2.0 is for recent releases
- Remove %%defattr
- Remove %%clean
- Use simpler approach to build html documentation
- Do not use custom/outdated setup.cfg
- Put one BuildRequires per line
- Enable python3 support
- Cleanup spec as wx backend is no longer supported
- Use default agg backend
- Fix bogus dates in changelog by assuming only week day was wrong

* Fri Aug 17 2012 Jerry James <loganjerry@gmail.com> - 1.1.1-1
- Update to version 1.1.1.
- Remove obsolete spec file elements
- Fix sourceforge URLs
- Allow sample data to have a different version number than the sources
- Don't bother removing problematic file since we remove entire agg24 directory
- Fix building with pygtk in the absence of an X server
- Don't install license text for bundled software that we don't bundle

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 3 2012 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 1.1.0-1
- Update to version 1.1.0.
- Do not regenerate upstream tarball but remove problematic file in %%prep.
- Remove non longer applicable/required patch0.
- Rediff/rename -noagg patch.
- Remove propagate-timezone-info-in-plot_date-xaxis_da patch already applied.
- Remove tkinter patch now with critical code in a try block.
- Remove png 1.5 patch as upstream is now png 1.5 aware.
- Update file list.

* Wed Apr 18 2012 David Malcolm <dmalcolm@redhat.com> - 1.0.1-20
- remove wx support for rhel >= 7

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-19
- Rebuilt for c++ ABI breakage

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec  6 2011 David Malcolm <dmalcolm@redhat.com> - 1.0.1-17
- fix the build against libpng 1.5

* Tue Dec  6 2011 David Malcolm <dmalcolm@redhat.com> - 1.0.1-16
- fix egg-info conditional for RHEL

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 1.0.1-15
- Rebuild for new libpng

* Mon Oct 31 2011 Dan Horák <dan[at]danny.cz> - 1.0.1-14
- fix build with new Tkinter which doesn't return an expected value in __version__

* Thu Sep 15 2011 Jef Spaleta <jspaleta@fedoraproject.org> - 1.0.1-13
- apply upstream bugfix for timezone formatting (Bug 735677) 

* Fri May 20 2011 Orion Poplawski <orion@cora.nwra.com> - 1.0.1-12
- Add Requires dvipng (Bug 684836)
- Build against system agg (Bug 612807)
- Use system pyparsing (Bug 702160)

* Sat Feb 26 2011 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 1.0.1-11
- Set PYTHONPATH during html doc building using find to prevent broken builds

* Sat Feb 26 2011 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 1.0.1-10
- Spec file cleanups for readability

* Sat Feb 26 2011 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 1.0.1-9
- Bump and rebuild

* Sat Feb 26 2011 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 1.0.1-8
- Fix spec file typos so package builds

* Fri Feb 25 2011 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 1.0.1-7
- Remove a debugging echo statement from the spec file
- Fix some line endings and permissions in -doc sub-package

* Fri Feb 25 2011 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 1.0.1-6
- Spec file cleanups to silence some rpmlint warnings

* Mon Feb 21 2011 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 1.0.1-5
- Add default attr to doc sub-package file list
- No longer designate -doc subpackage as noarch
- Add arch specific Requires for tk, wx and doc sub-packages

* Mon Feb 21 2011 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 1.0.1-4
- Enable wxPython backend
- Make -doc sub-package noarch

* Mon Feb 21 2011 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 1.0.1-3
- Add conditional for optionally building doc sub-package
- Add flag to build low res images for documentation
- Add matplotlib-1.0.1-plot_directive.patch to fix build of low res images
- Remove unused patches

* Sat Feb 19 2011 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 1.0.1-2
- Build and package HTML documentation in -doc sub-package
- Move examples to -doc sub-package
- Make examples non-executable

* Fri Feb 18 2011 Thomas Spura <tomspur@fedoraproject.org> - 1.0.1-1
- update to new bugfix version (#678489)
- set file attributes in tk subpackage
- filter private *.so

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu Jul 8 2010 Jef Spaleta <jspaleta AT fedoraproject DOT org> - 1.0.0-1
- New upstream release  
- Remove undistributable file from bundled agg library 

* Thu Jul 1 2010 Jef Spaleta <jspaleta AT fedoraproject DOT org> - 0.99.3-1
- New upstream release  

* Thu May 27 2010 Jef Spaleta <jspaleta AT fedoraproject DOT org> - 0.99.1.2-4
- Upstream patch to fix deprecated gtk tooltip warning.  

* Mon Apr 12 2010 Jef Spaleta <jspaleta AT fedoraproject DOT org> - 0.99.1.2-2
- Bump to rebuild against numpy 1.3  

* Thu Apr 1 2010 Jef Spaleta <jspaleta AT fedoraproject DOT org> - 0.99.1.2-1
- Bump to rebuild against numpy 1.4.0  

* Fri Dec 11 2009 Jon Ciesla <limb@jcomserv.net> - 0.99.1.2
- Update to 0.99.1.2

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.98.5.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Mar 06 2009 Jef Spaleta <jspaleta AT fedoraproject DOT org> - 0.98.5-4
- Fixed font dep after font guideline change

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.98.5.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Dec 23 2008 Jef Spaleta <jspaleta AT fedoraproject DOT org> - 0.98.5-2
- Add dep on DejaVu Sans font for default font support

* Mon Dec 22 2008 Jef Spaleta <jspaleta AT fedoraproject DOT org> - 0.98.5-1
- Latest upstream release
- Strip out included fonts

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.98.3-2
- Rebuild for Python 2.6

* Wed Aug  6 2008 Jef Spaleta <jspaleta AT fedoraproject DOT org> - 0.98.3-1
- Latest upstream release

* Tue Jul  1 2008 Jef Spaleta <jspaleta AT fedoraproject DOT org> - 0.98.1-1
- Latest upstream release

* Fri Mar  21 2008 Jef Spaleta <jspaleta[AT]fedoraproject org> - 0.91.2-2
- gcc43 cleanups

* Fri Mar  21 2008 Jef Spaleta <jspaleta[AT]fedoraproject org> - 0.91.2-1
- New upstream version
- Adding Fedora specific setup.cfg from included template
- removed numarry and numerics build requirements

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.90.1-6
- Autorebuild for GCC 4.3

* Fri Jan  4 2008 Alex Lancaster <alexlan[AT]fedoraproject org> - 0.90.1-5
- Fixed typo in spec.

* Fri Jan  4 2008 Alex Lancaster <alexlan[AT]fedoraproject org> - 0.90.1-4
- Support for Python Eggs for F9+

* Thu Jan  3 2008 Alex Lancaster <alexlan[AT]fedoraproject org> - 0.90.1-3
- Rebuild for new Tcl 8.5

* Thu Aug 23 2007 Orion Poplawski <orion@cora.nwra.com> 0.90.1-2
- Update license tag to Python
- Rebuild for BuildID

* Mon Jun 04 2007 Orion Poplawski <orion@cora.nwra.com> 0.90.1-1
- Update to 0.90.1

* Wed Feb 14 2007 Orion Poplawski <orion@cora.nwra.com> 0.90.0-2
- Rebuild for Tcl/Tk downgrade

* Sat Feb 10 2007 Jef Spaleta <jspaleta@gmail.com> 0.90.0-2
- Release bump for rebuild against new tk 

* Fri Feb 09 2007 Orion Poplawski <orion@cora.nwra.com> 0.90.0-1
- Update to 0.90.0

* Fri Jan  5 2007 Orion Poplawski <orion@cora.nwra.com> 0.87.7-4
- Add examples to %%docs

* Mon Dec 11 2006 Jef Spaleta <jspaleta@gmail.com> 0.87.7-3
- Release bump for rebuild against python 2.5 in devel tree

* Tue Dec  5 2006 Orion Poplawski <orion@cora.nwra.com> 0.87.7-2
- Force build of gtk/gtkagg backends in mock (bug #218153)
- Change Requires from python-numeric to numpy (bug #218154)

* Tue Nov 21 2006 Orion Poplawski <orion@cora.nwra.com> 0.87.7-1
- Update to 0.87.7 and fix up the defaults to use numpy
- Force build of tkagg backend without X server
- Use src.rpm from Jef Spaleta, closes bug 216578

* Fri Oct  6 2006 Orion Poplawski <orion@cora.nwra.com> 0.87.6-1
- Update to 0.87.6

* Thu Sep  7 2006 Orion Poplawski <orion@cora.nwra.com> 0.87.5-1
- Update to 0.87.5

* Thu Jul 27 2006 Orion Poplawski <orion@cora.nwra.com> 0.87.4-1
- Update to 0.87.4

* Wed Jun  7 2006 Orion Poplawski <orion@cora.nwra.com> 0.87.3-1
- Update to 0.87.3

* Mon May 15 2006 Orion Poplawski <orion@cora.nwra.com> 0.87.2-2
- Rebuild for new numpy

* Tue Mar  7 2006 Orion Poplawski <orion@cora.nwra.com> 0.87.2-1
- Update to 0.87.2

* Tue Mar  7 2006 Orion Poplawski <orion@cora.nwra.com> 0.87.1-1
- Update to 0.87.1
- Add pycairo >= 1.0.2 requires (FC5+ only)

* Fri Feb 24 2006 Orion Poplawski <orion@cora.nwra.com> 0.87-1
- Update to 0.87
- Add BR numpy and python-numarray
- Add patch to keep Numeric as the default numerix package
- Add BR tkinter and tk-devel for TkInter backend
- Make separate package for Tk backend

* Tue Jan 10 2006 Orion Poplawski <orion@cora.nwra.com> 0.86-1
- Update to 0.86

* Thu Dec 22 2005 Orion Poplawski <orion@cora.nwra.com> 0.85-2
- Rebuild

* Sun Nov 20 2005 Orion Poplawski <orion@cora.nwra.com> 0.85-1
- New upstream version 0.85

* Mon Sep 19 2005 Orion Poplawski <orion@cora.nwra.com> 0.84-1
- New upstream version 0.84

* Tue Aug 02 2005 Orion Poplawski <orion@cora.nwra.com> 0.83.2-3
- bump release 

* Tue Aug 02 2005 Orion Poplawski <orion@cora.nwra.com> 0.83.2-2
- Add Requires: python-numeric, pytz, python-dateutil

* Fri Jul 29 2005 Orion Poplawski <orion@cora.nwra.com> 0.83.2-1
- New upstream version matplotlib 0.83.2

* Thu Jul 28 2005 Orion Poplawski <orion@cora.nwra.com> 0.83.1-2
- Bump rel to fix botched tag

* Thu Jul 28 2005 Orion Poplawski <orion@cora.nwra.com> 0.83.1-1
- New upstream version matplotlib 0.83.1

* Tue Jul 05 2005 Orion Poplawski <orion@cora.nwra.com> 0.82-4
- BuildRequires: pytz, python-dateutil - use upstream
- Don't use INSTALLED_FILES, list dirs
- Fix execute permissions

* Fri Jul 01 2005 Orion Poplawski <orion@cora.nwra.com> 0.82-3
- Use %%{python_sitearch}

* Thu Jun 30 2005 Orion Poplawski <orion@cora.nwra.com> 0.82-2
- Rename to python-matplotlib
- Remove unneeded Requires: python
- Add private directories to %%files

* Tue Jun 28 2005 Orion Poplawski <orion@cora.nwra.com> 0.82-1
- Initial package for Fedora Extras
