%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
%global pypi_name oslo.utils
%global pkg_name oslo-utils
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
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif
BuildArch:      noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
%endif

BuildRequires:  git-core
BuildRequires:  openstack-macros

%description
%{common_desc}

%package -n python3-%{pkg_name}
Summary:    OpenStack Oslo Utility library
%{?python_provide:%python_provide python3-%{pkg_name}}

BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-iso8601
BuildRequires:  python3-debtcollector
# test requirements
BuildRequires:  python3-eventlet
BuildRequires:  python3-hacking
BuildRequires:  python3-fixtures
BuildRequires:  python3-oslotest
BuildRequires:  python3-testtools
BuildRequires:  python3-ddt
BuildRequires:  python3-oslo-i18n
BuildRequires:  python3-pyparsing
BuildRequires:  python3-testscenarios
BuildRequires:  python3-testrepository
BuildRequires:  python3-netaddr
BuildRequires:  python3-packaging
BuildRequires:  python3-yaml
# Required to compile translation files
BuildRequires:  python3-babel
BuildRequires:  python3-netifaces
BuildRequires:  python3-pytz

Requires:       python3-oslo-i18n >= 3.15.3
Requires:       python3-iso8601
Requires:       python3-debtcollector >= 1.2.0
Requires:       python3-pyparsing
Requires:       python3-netaddr >= 0.7.18
Requires:       python3-pytz
Requires:       python3-netifaces >= 0.10.4
Requires:       python3-packaging >= 20.4
Requires:       python-%{pkg_name}-lang = %{version}-%{release}

%description -n python3-%{pkg_name}
%{common_desc}

%if 0%{?with_doc}
%package -n python-%{pkg_name}-doc
Summary:    Documentation for the Oslo Utility library

BuildRequires:  python3-sphinx
BuildRequires:  python3-openstackdocstheme

%description -n python-%{pkg_name}-doc
Documentation for the Oslo Utility library.
%endif

%package -n python3-%{pkg_name}-tests
Summary:    Tests for the Oslo Utility library

Requires: python3-%{pkg_name} = %{version}-%{release}
Requires: python3-eventlet
Requires: python3-hacking
Requires: python3-fixtures
Requires: python3-oslotest
Requires: python3-testtools
Requires: python3-ddt
Requires: python3-testscenarios
Requires: python3-testrepository

%description -n python3-%{pkg_name}-tests
%{common_desc_tests}

%package  -n python-%{pkg_name}-lang
Summary:   Translation files for Oslo utils library

%description -n python-%{pkg_name}-lang
Translation files for Oslo utils library

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{pypi_name}-%{upstream_version} -S git

# Let RPM handle the dependencies
%py_req_cleanup

%build
%{py3_build}

%if 0%{?with_doc}
# generate html docs
sphinx-build-3 -W -b html doc/source doc/build/html
# remove the sphinx-build-3 leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

# Generate i18n files
python3 setup.py compile_catalog -d build/lib/oslo_utils/locale --domain oslo_utils

%install
%{py3_install}

# Install i18n .mo files (.po and .pot are not required)
install -d -m 755 %{buildroot}%{_datadir}
rm -f %{buildroot}%{python3_sitelib}/oslo_utils/locale/*/LC_*/oslo_utils*po
rm -f %{buildroot}%{python3_sitelib}/oslo_utils/locale/*pot
mv %{buildroot}%{python3_sitelib}/oslo_utils/locale %{buildroot}%{_datadir}/locale

# Find language files
%find_lang oslo_utils --all-name

%check
python3 setup.py test

%files -n python3-%{pkg_name}
%doc README.rst
%license LICENSE
%{python3_sitelib}/oslo_utils
%{python3_sitelib}/*.egg-info
%exclude %{python3_sitelib}/oslo_utils/tests

%if 0%{?with_doc}
%files -n python-%{pkg_name}-doc
%doc doc/build/html
%license LICENSE
%endif

%files -n python3-%{pkg_name}-tests
%{python3_sitelib}/oslo_utils/tests

%files -n python-%{pkg_name}-lang -f oslo_utils.lang
%license LICENSE

%changelog
