%global pypi_name oslo.utils

%if 0%{?fedora}
%global with_python3 1
%endif

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:           python-oslo-utils
Version:        2.5.0
Release:        1%{?dist}
Summary:        OpenStack Oslo Utility library

License:        ASL 2.0
URL:            http://launchpad.net/oslo
Source0:        https://pypi.python.org/packages/source/o/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

%description
The OpenStack Oslo Utility library.
* Documentation: http://docs.openstack.org/developer/oslo.utils
* Source: http://git.openstack.org/cgit/openstack/oslo.utils
* Bugs: http://bugs.launchpad.net/oslo

%package -n python2-oslo-utils
Summary:        OpenStack Oslo Utility library
%{?python_provide:%python_provide python2-oslo-utils}
Provides:       python-oslo-utils = %{version}-%{release}
Obsoletes:      python-oslo-utils < 2.4.0-2

BuildRequires:  python2-devel
BuildRequires:  python-pbr

Requires:       python-oslo-config
Requires:       python-oslo-i18n
Requires:       python-babel
Requires:       python-iso8601
Requires:       python-six >= 1.9.0
Requires:       python-netaddr >= 0.7.12
Requires:       python-netifaces >= 0.10.4
Requires:       python-debtcollector >= 0.3.0
Requires:       pytz
Requires:       python-monotonic

%description -n python2-oslo-utils
The OpenStack Oslo Utility library.
* Documentation: http://docs.openstack.org/developer/oslo.utils
* Source: http://git.openstack.org/cgit/openstack/oslo.utils
* Bugs: http://bugs.launchpad.net/oslo

%package -n python2-oslo-utils-doc
Summary:    Documentation for the Oslo Utility library
%{?python_provide:%python_provide python2-oslo-utils-doc}
Provides:       python-oslo-utils-doc = %{version}-%{release}
Obsoletes:      python-oslo-utils-doc < 2.4.0-2

BuildRequires:  python-sphinx
BuildRequires:  python-oslo-sphinx
# for API autodoc
BuildRequires:  python-netifaces
BuildRequires:  python-debtcollector
BuildRequires:  python-oslo-i18n
BuildRequires:  python-netaddr

%description -n python2-oslo-utils-doc
Documentation for the Oslo Utility library.

# python3 subpackage
%if 0%{?with_python3}
%package -n python3-oslo-utils
Summary:        OpenStack Oslo Utility library
%{?python_provide:%python_provide python3-oslo-utils}

BuildRequires:  python3-devel
BuildRequires:  python3-pbr

Requires:       python3-oslo-config
Requires:       python3-oslo-i18n
Requires:       python3-babel
Requires:       python3-iso8601
Requires:       python3-six >= 1.9.0
Requires:       python3-netaddr >= 0.7.12
Requires:       python3-netifaces >= 0.10.4
Requires:       python3-debtcollector >= 0.3.0
Requires:       python3-pytz
Requires:       python3-monotonic

%description -n python3-oslo-utils
The OpenStack Oslo Utility library.
* Documentation: http://docs.openstack.org/developer/oslo.utils
* Source: http://git.openstack.org/cgit/openstack/oslo.utils
* Bugs: http://bugs.launchpad.net/oslo
%endif

%if 0%{?with_python3}
%package -n python3-oslo-utils-doc
Summary:    Documentation for the Oslo Utility library
%{?python_provide:%python_provide python3-oslo-utils-doc}

BuildRequires:  python3-sphinx
BuildRequires:  python3-oslo-sphinx
# for API autodoc
BuildRequires:  python3-netifaces
BuildRequires:  python3-debtcollector
BuildRequires:  python3-oslo-i18n
BuildRequires:  python3-netaddr

%description -n python3-oslo-utils-doc
Documentation for the Oslo Utility library.
%endif

%prep
%setup -q -n %{pypi_name}-%{upstream_version}

# Let RPM handle the dependencies
rm -f {test-,}requirements.txt


%build
%{__python2} setup.py build

# generate html docs
sphinx-build doc/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%if 0%{?with_python3}
%{__python3} setup.py build
sphinx-build-3 doc/source html
# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.buildinfo
%endif

%install
%{__python2} setup.py install --skip-build --root %{buildroot}

%if 0%{?with_python3}
%{__python3} setup.py install --skip-build --root %{buildroot}
%endif

%files -n python2-oslo-utils
%doc README.rst
%license LICENSE
%{python2_sitelib}/oslo_utils
%{python2_sitelib}/*.egg-info

%files -n python2-oslo-utils-doc
%doc html
%license LICENSE

%if 0%{?with_python3}
%files -n python3-oslo-utils
%doc README.rst
%license LICENSE
%{python3_sitelib}/oslo_utils
%{python3_sitelib}/*.egg-info

%files -n python3-oslo-utils-doc
%doc html
%license LICENSE
%endif

%changelog
* Fri Sep 18 2015 Alan Pevec <alan.pevec@redhat.com> 2.5.0-1
- Update to upstream 2.5.0

* Mon Sep 07 2015 Chandan Kumar <chkumar246@gmail.com> 2.4.0-2
- Added python2 and python3 subpackages

* Thu Sep 03 2015 Alan Pevec <alan.pevec@redhat.com> 2.4.0-1
- Update to upstream 2.4.0

* Fri Aug 21 2015 Matthias Runge <mrunge@redhat.com> 2.2.0-2
- add missing requires: python-monotonic

* Mon Aug 17 2015 Alan Pevec <alan.pevec@redhat.com> 2.2.0-1
- Update to upstream 2.2.0

* Mon Jun 29 2015 Alan Pevec <alan.pevec@redhat.com> 1.6.0-2
- Update to upstream 1.6.0

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Mar 31 2015 Alan Pevec <alan.pevec@redhat.com> 1.4.0-1
- Update to 1.4.0

* Tue Feb 24 2015 Alan Pevec <alan.pevec@redhat.com> 1.3.0-1
- Update to upstream 1.3.0

* Sun Sep 21 2014 Alan Pevec <alan.pevec@redhat.com> 1.0.0-1
- Update to upstream 1.0.0

* Thu Sep 11 2014 Alan Pevec <apevec@redhat.com> - 0.3.0-1
- update to 0.3.0

* Wed Aug 20 2014 Alan Pevec <apevec@redhat.com> - 0.2.0-1
- update to 0.2.0

* Thu Jul 31 2014 Alan Pevec <apevec@redhat.com> - 0.1.1-1
- Initial package.
