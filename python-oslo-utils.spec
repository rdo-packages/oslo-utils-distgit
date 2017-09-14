%global pypi_name oslo.utils
%global pkg_name oslo-utils

%if 0%{?fedora} >= 24
%global with_python3 1
%endif

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:           python-oslo-utils
Version:        XXX
Release:        XXX
Summary:        OpenStack Oslo Utility library

License:        ASL 2.0
URL:            http://launchpad.net/oslo
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz
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
BuildRequires:  git

# test requirements
BuildRequires:  pyparsing
BuildRequires:  python-hacking
BuildRequires:  python-fixtures
BuildRequires:  python-oslotest
BuildRequires:  python-testscenarios
BuildRequires:  python-testtools
BuildRequires:  python-testrepository
BuildRequires:  python-funcsigs
# Required to compile translation files
BuildRequires:  python-babel

Requires:       pyparsing
Requires:       python-funcsigs
Requires:       python-oslo-i18n >= 2.1.0
Requires:       python-iso8601
Requires:       python-six >= 1.9.0
Requires:       python-netaddr >= 0.7.12
Requires:       python-netifaces >= 0.10.4
Requires:       python-debtcollector >= 1.2.0
Requires:       pytz
Requires:       python-monotonic
Requires:       python-%{pkg_name}-lang = %{version}-%{release}

%description -n python2-%{pkg_name}
The OpenStack Oslo Utility library.
* Documentation: http://docs.openstack.org/developer/oslo.utils
* Source: http://git.openstack.org/cgit/openstack/oslo.utils
* Bugs: http://bugs.launchpad.net/oslo


%package -n python-%{pkg_name}-doc
Summary:    Documentation for the Oslo Utility library

BuildRequires:  python-sphinx
BuildRequires:  python-openstackdocstheme
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
%package -n python3-%{pkg_name}-tests
Summary:    Tests for the Oslo Utility library

Requires: python3-%{pkg_name} = %{version}-%{release}
Requires: python3-hacking
Requires: python3-fixtures
Requires: python3-oslotest
Requires: python3-testscenarios
Requires: python3-testtools
Requires: python3-testrepository

%description -n python3-%{pkg_name}-tests
Tests for the Oslo Utility library.
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
BuildRequires:  python3-oslotest
BuildRequires:  python3-testscenarios
BuildRequires:  python3-testtools
BuildRequires:  python3-testrepository
BuildRequires:  python3-funcsigs

Requires:       python3-pyparsing
Requires:       python3-funcsigs
Requires:       python3-oslo-i18n >= 2.1.0
Requires:       python3-iso8601
Requires:       python3-six >= 1.9.0
Requires:       python3-netaddr >= 0.7.12
Requires:       python3-netifaces >= 0.10.4
Requires:       python3-debtcollector >= 1.2.0
Requires:       python3-pytz
Requires:       python3-monotonic
Requires:       python-%{pkg_name}-lang = %{version}-%{release}

%description -n python3-%{pkg_name}
The OpenStack Oslo Utility library.
* Documentation: http://docs.openstack.org/developer/oslo.utils
* Source: http://git.openstack.org/cgit/openstack/oslo.utils
* Bugs: http://bugs.launchpad.net/oslo
%endif

%package  -n python-%{pkg_name}-lang
Summary:   Translation files for Oslo utils library

%description -n python-%{pkg_name}-lang
Translation files for Oslo utils library

%prep
%autosetup -n %{pypi_name}-%{upstream_version} -S git

# Let RPM handle the dependencies
rm -f {test-,}requirements.txt

%build
%py2_build

# generate html docs
%{__python2} setup.py build_sphinx -b html
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}

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

%files -n python-%{pkg_name}-doc
%doc doc/build/html
%license LICENSE

%files -n python-%{pkg_name}-tests
%{python2_sitelib}/oslo_utils/tests

%files -n python-%{pkg_name}-lang -f oslo_utils.lang
%license LICENSE

%if 0%{?with_python3}
%files -n python3-%{pkg_name}-tests
%{python3_sitelib}/oslo_utils/tests
%endif

%changelog
