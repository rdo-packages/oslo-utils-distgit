%global pypi_name oslo.utils
%global pkg_name oslo-utils

%if 0%{?fedora} >= 24
%global with_python3 1
%endif

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:           python-oslo-utils
Version:        3.7.0
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

%package -n python2-%{pkg_name}
Summary:        OpenStack Oslo Utility library
%{?python_provide:%python_provide python2-%{pkg_name}}

BuildRequires:  python2-devel
BuildRequires:  python-funcsigs
BuildRequires:  python-pbr
# Required for documentation building
BuildRequires:  python-iso8601
BuildRequires:  python-monotonic
BuildRequires:  pytz

# test requirements
BuildRequires:  python-hacking
BuildRequires:  python-fixtures
BuildRequires:  python-oslo-config
BuildRequires:  python-oslotest
BuildRequires:  python-testscenarios
BuildRequires:  python-testtools
BuildRequires:  python-testrepository
BuildRequires:  python-funcsigs

Requires:       python-funcsigs
Requires:       python-oslo-config
Requires:       python-oslo-i18n
Requires:       python-babel
Requires:       python-funcsigs
Requires:       python-iso8601
Requires:       python-six >= 1.9.0
Requires:       python-netaddr >= 0.7.12
Requires:       python-netifaces >= 0.10.4
Requires:       python-debtcollector >= 0.3.0
Requires:       pytz
Requires:       python-monotonic

%description -n python2-%{pkg_name}
The OpenStack Oslo Utility library.
* Documentation: http://docs.openstack.org/developer/oslo.utils
* Source: http://git.openstack.org/cgit/openstack/oslo.utils
* Bugs: http://bugs.launchpad.net/oslo


%package -n python-%{pkg_name}-doc
Summary:    Documentation for the Oslo Utility library

BuildRequires:  python-sphinx
BuildRequires:  python-oslo-sphinx
# for API autodoc
BuildRequires:  python-iso8601
BuildRequires:  python-monotonic
BuildRequires:  python-netifaces
BuildRequires:  python-debtcollector
BuildRequires:  python-oslo-i18n
BuildRequires:  python-netaddr

%description -n python-%{pkg_name}-doc
Documentation for the Oslo Utility library.

%package -n python-%{pkg_name}-tests
Summary:    Tests for the Oslo Utility library

Requires: python-%{pkg_name} = %{version}-%{release}
Requires: python-hacking
Requires: python-fixtures
Requires: python-oslotest
Requires: python-testscenarios
Requires: python-testtools
Requires: python-testrepository

%description -n python-%{pkg_name}-tests
Tests for the Oslo Utility library.

%if 0%{?with_python3}
%package -n python3-%{pkg_name}
Summary:        OpenStack Oslo Utility library
%{?python_provide:%python_provide python3-%{pkg_name}}

BuildRequires:  python3-devel
BuildRequires:  python3-pbr

# test requirements
BuildRequires:  python3-hacking
BuildRequires:  python3-fixtures
BuildRequires:  python3-oslo-config
BuildRequires:  python3-oslotest
BuildRequires:  python3-testscenarios
BuildRequires:  python3-testtools
BuildRequires:  python3-testrepository
BuildRequires:  python3-funcsigs

Requires:       python3-funcsigs
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

%description -n python3-%{pkg_name}
The OpenStack Oslo Utility library.
* Documentation: http://docs.openstack.org/developer/oslo.utils
* Source: http://git.openstack.org/cgit/openstack/oslo.utils
* Bugs: http://bugs.launchpad.net/oslo
%endif

%prep
%setup -q -n %{pypi_name}-%{upstream_version}

# Let RPM handle the dependencies
rm -f {test-,}requirements.txt

%build
%py2_build

# generate html docs
sphinx-build doc/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%if 0%{?with_python3}
%py3_build
%endif

%install
%py2_install
%if 0%{?with_python3}
%py3_install
%endif

%check
%if 0%{?with_python3}
%{__python3} setup.py test
%endif
%{__python2} setup.py test

%files -n python2-%{pkg_name}
%doc README.rst
%license LICENSE
%{python2_sitelib}/oslo_utils
%{python2_sitelib}/*.egg-info
%exclude %{python2_sitelib}/oslo_utils/tests

%if 0%{?with_python3}
%files -n python3-%{pkg_name}
%doc README.rst
%license LICENSE
%{python3_sitelib}/oslo_utils
%{python3_sitelib}/*.egg-info
%exclude %{python3_sitelib}/oslo_utils/tests
%endif

%files -n python-%{pkg_name}-doc
%doc html
%license LICENSE

%files -n python-%{pkg_name}-tests
%{python2_sitelib}/oslo_utils/tests

%changelog
* Tue Mar 22 2016 Haikel Guemar <hguemar@fedoraproject.org> 3.7.0-
- Update to 3.7.0

