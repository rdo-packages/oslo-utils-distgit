%global pypi_name oslo.utils
%global pkg_name oslo-utils

%if 0%{?fedora} >= 24 || 0%{?rhel} > 7
%global with_python3 1
%endif

%global with_doc 1

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global common_desc \
The OpenStack Oslo Utility library. \
* Documentation: http://docs.openstack.org/developer/oslo.utils \
* Source: http://git.openstack.org/cgit/openstack/oslo.utils \
* Bugs: http://bugs.launchpad.net/oslo

%global common_desc_tests Tests for the Oslo Utility library.

Name:           python-oslo-utils
Version:        XXX
Release:        XXX
Summary:        OpenStack Oslo Utility library

License:        ASL 2.0
URL:            http://launchpad.net/oslo
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz
BuildArch:      noarch

BuildRequires:  git
BuildRequires:  openstack-macros

%description
%{common_desc}

%package -n python2-%{pkg_name}
Summary:        OpenStack Oslo Utility library
%{?python_provide:%python_provide python2-%{pkg_name}}

BuildRequires:  python2-devel
BuildRequires:  python2-funcsigs
BuildRequires:  python2-pbr
BuildRequires:  python2-iso8601
BuildRequires:  python2-debtcollector
# test requirements
BuildRequires:  python2-hacking
BuildRequires:  python2-fixtures
BuildRequires:  python2-oslotest
BuildRequires:  python2-testtools
BuildRequires:  python2-funcsigs
BuildRequires:  python2-ddt
BuildRequires:  python2-oslo-i18n
# Required to compile translation files
BuildRequires:  python2-babel
%if 0%{?fedora} || 0%{?rhel} > 7
BuildRequires:  python2-pyparsing
BuildRequires:  python2-monotonic
BuildRequires:  python2-pytz
BuildRequires:  python2-testscenarios
BuildRequires:  python2-testrepository
BuildRequires:  python2-netaddr
BuildRequires:  python2-netifaces
%else
BuildRequires:  pyparsing
BuildRequires:  python-monotonic
BuildRequires:  python-netaddr
BuildRequires:  python-netifaces
BuildRequires:  pytz
BuildRequires:  python-testscenarios
BuildRequires:  python-testrepository
%endif

Requires:       python2-funcsigs
Requires:       python2-oslo-i18n >= 3.15.3
Requires:       python2-iso8601
Requires:       python2-six >= 1.10.0
Requires:       python2-debtcollector >= 1.2.0
%if 0%{?fedora} || 0%{?rhel} > 7
Requires:       python2-pyparsing
Requires:       python2-netaddr >= 0.7.18
Requires:       python2-monotonic
Requires:       python2-pytz
Requires:       python2-netifaces >= 0.10.4
%else
Requires:       pyparsing
Requires:       python-netaddr >= 0.7.18
Requires:       python-monotonic
Requires:       pytz
Requires:       python-netifaces >= 0.10.4
%endif
Requires:       python-%{pkg_name}-lang = %{version}-%{release}

%description -n python2-%{pkg_name}
%{common_desc}

%if 0%{?with_doc}
%package -n python-%{pkg_name}-doc
Summary:    Documentation for the Oslo Utility library

BuildRequires:  python2-sphinx
BuildRequires:  python2-openstackdocstheme

%description -n python-%{pkg_name}-doc
Documentation for the Oslo Utility library.
%endif

%package -n python2-%{pkg_name}-tests
Summary:    Tests for the Oslo Utility library
%{?python_provide:%python_provide python2-%{pkg_name}-tests}

Requires: python2-%{pkg_name} = %{version}-%{release}
Requires: python2-hacking
Requires: python2-fixtures
Requires: python2-oslotest
Requires: python2-testtools
Requires: python2-ddt
%if 0%{?fedora} || 0%{?rhel} > 7
Requires: python2-testscenarios
Requires: python2-testrepository
%else
Requires: python-testscenarios
Requires: python-testrepository
%endif

%description -n python2-%{pkg_name}-tests
%{common_desc_tests}

%if 0%{?with_python3}
%package -n python3-%{pkg_name}-tests
Summary:    Tests for the Oslo Utility library
%{?python_provide:%python_provide python3-%{pkg_name}-tests}

Requires: python3-%{pkg_name} = %{version}-%{release}
Requires: python3-hacking
Requires: python3-fixtures
Requires: python3-monotonic
Requires: python3-netaddr
Requires: python3-oslo-i18n
Requires: python3-oslotest
Requires: python3-testscenarios
Requires: python3-testtools
Requires: python3-testrepository
Requires: python3-ddt

%description -n python3-%{pkg_name}-tests
%{common_desc_tests}
%endif

%if 0%{?with_python3}
%package -n python3-%{pkg_name}
Summary:        OpenStack Oslo Utility library
%{?python_provide:%python_provide python3-%{pkg_name}}

BuildRequires:  python3-devel
BuildRequires:  python3-pbr

# test requirements
BuildRequires:  python3-pyparsing
BuildRequires:  python3-hacking
BuildRequires:  python3-fixtures
BuildRequires:  python3-monotonic
BuildRequires:  python3-netaddr
BuildRequires:  python3-oslo-i18n
BuildRequires:  python3-oslotest
BuildRequires:  python3-testscenarios
BuildRequires:  python3-testtools
BuildRequires:  python3-testrepository
BuildRequires:  python3-funcsigs
BuildRequires:  python3-ddt

Requires:       python3-pyparsing
Requires:       python3-funcsigs
Requires:       python3-oslo-i18n >= 3.15.3
Requires:       python3-iso8601
Requires:       python3-six >= 1.10.0
Requires:       python3-netaddr >= 0.7.18
Requires:       python3-netifaces >= 0.10.4
Requires:       python3-debtcollector >= 1.2.0
Requires:       python3-pytz
Requires:       python3-monotonic
Requires:       python-%{pkg_name}-lang = %{version}-%{release}

%description -n python3-%{pkg_name}
%{common_desc}
%endif

%package  -n python-%{pkg_name}-lang
Summary:   Translation files for Oslo utils library

%description -n python-%{pkg_name}-lang
Translation files for Oslo utils library

%prep
%autosetup -n %{pypi_name}-%{upstream_version} -S git

# Let RPM handle the dependencies
%py_req_cleanup

%build
%py2_build

%if 0%{?with_doc}
# generate html docs
sphinx-build -W -b html doc/source doc/build/html
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

# Generate i18n files
%{__python2} setup.py compile_catalog -d build/lib/oslo_utils/locale

%if 0%{?with_python3}
%py3_build
%endif

%install
%py2_install
%if 0%{?with_python3}
%py3_install
%endif

# Install i18n .mo files (.po and .pot are not required)
install -d -m 755 %{buildroot}%{_datadir}
rm -f %{buildroot}%{python2_sitelib}/oslo_utils/locale/*/LC_*/oslo_utils*po
rm -f %{buildroot}%{python2_sitelib}/oslo_utils/locale/*pot
mv %{buildroot}%{python2_sitelib}/oslo_utils/locale %{buildroot}%{_datadir}/locale
%if 0%{?with_python3}
rm -rf %{buildroot}%{python3_sitelib}/oslo_utils/locale
%endif

# Find language files
%find_lang oslo_utils --all-name


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

%if 0%{?with_doc}
%files -n python-%{pkg_name}-doc
%doc doc/build/html
%license LICENSE
%endif

%files -n python2-%{pkg_name}-tests
%{python2_sitelib}/oslo_utils/tests

%files -n python-%{pkg_name}-lang -f oslo_utils.lang
%license LICENSE

%if 0%{?with_python3}
%files -n python3-%{pkg_name}-tests
%{python3_sitelib}/oslo_utils/tests
%endif

%changelog
