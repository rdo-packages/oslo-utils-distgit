# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility
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
Version:        3.41.3
Release:        1%{?dist}
Summary:        OpenStack Oslo Utility library

License:        ASL 2.0
URL:            http://launchpad.net/oslo
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz
BuildArch:      noarch

BuildRequires:  git
BuildRequires:  openstack-macros

%description
%{common_desc}

%package -n python%{pyver}-%{pkg_name}
Summary:    OpenStack Oslo Utility library
%{?python_provide:%python_provide python%{pyver}-%{pkg_name}}

BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-funcsigs
BuildRequires:  python%{pyver}-pbr
BuildRequires:  python%{pyver}-iso8601
BuildRequires:  python%{pyver}-debtcollector
# test requirements
BuildRequires:  python%{pyver}-eventlet
BuildRequires:  python%{pyver}-hacking
BuildRequires:  python%{pyver}-fixtures
BuildRequires:  python%{pyver}-oslotest
BuildRequires:  python%{pyver}-testtools
BuildRequires:  python%{pyver}-funcsigs
BuildRequires:  python%{pyver}-ddt
BuildRequires:  python%{pyver}-oslo-i18n
BuildRequires:  python%{pyver}-pyparsing
BuildRequires:  python%{pyver}-testscenarios
BuildRequires:  python%{pyver}-testrepository
BuildRequires:  python%{pyver}-netaddr
# Required to compile translation files
BuildRequires:  python%{pyver}-babel
# Handle python2 exception
%if %{pyver} == 2
BuildRequires:  python-netifaces
BuildRequires:  pytz
BuildRequires:  python%{pyver}-monotonic
%else
BuildRequires:  python%{pyver}-netifaces
BuildRequires:  python%{pyver}-pytz
%endif

Requires:       python%{pyver}-funcsigs
Requires:       python%{pyver}-oslo-i18n >= 3.15.3
Requires:       python%{pyver}-iso8601
Requires:       python%{pyver}-six >= 1.10.0
Requires:       python%{pyver}-debtcollector >= 1.2.0
Requires:       python%{pyver}-pyparsing
Requires:       python%{pyver}-netaddr >= 0.7.18
# Handle python2 exception
%if %{pyver} == 2
Requires:       pytz
Requires:       python-netifaces >= 0.10.4
Requires:       python%{pyver}-monotonic
%else
Requires:       python%{pyver}-pytz
Requires:       python%{pyver}-netifaces >= 0.10.4
%endif
Requires:       python-%{pkg_name}-lang = %{version}-%{release}

%description -n python%{pyver}-%{pkg_name}
%{common_desc}

%if 0%{?with_doc}
%package -n python-%{pkg_name}-doc
Summary:    Documentation for the Oslo Utility library

BuildRequires:  python%{pyver}-sphinx
BuildRequires:  python%{pyver}-openstackdocstheme

%description -n python-%{pkg_name}-doc
Documentation for the Oslo Utility library.
%endif

%package -n python%{pyver}-%{pkg_name}-tests
Summary:    Tests for the Oslo Utility library

Requires: python%{pyver}-%{pkg_name} = %{version}-%{release}
Requires: python%{pyver}-eventlet
Requires: python%{pyver}-hacking
Requires: python%{pyver}-fixtures
Requires: python%{pyver}-oslotest
Requires: python%{pyver}-testtools
Requires: python%{pyver}-ddt
Requires: python%{pyver}-testscenarios
Requires: python%{pyver}-testrepository

%description -n python%{pyver}-%{pkg_name}-tests
%{common_desc_tests}

%package  -n python-%{pkg_name}-lang
Summary:   Translation files for Oslo utils library

%description -n python-%{pkg_name}-lang
Translation files for Oslo utils library

%prep
%autosetup -n %{pypi_name}-%{upstream_version} -S git

# Let RPM handle the dependencies
%py_req_cleanup

%build
%{pyver_build}

%if 0%{?with_doc}
# generate html docs
sphinx-build-%{pyver} -W -b html doc/source doc/build/html
# remove the sphinx-build-%{pyver} leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

# Generate i18n files
%{pyver_bin} setup.py compile_catalog -d build/lib/oslo_utils/locale

%install
%{pyver_install}

# Install i18n .mo files (.po and .pot are not required)
install -d -m 755 %{buildroot}%{_datadir}
rm -f %{buildroot}%{pyver_sitelib}/oslo_utils/locale/*/LC_*/oslo_utils*po
rm -f %{buildroot}%{pyver_sitelib}/oslo_utils/locale/*pot
mv %{buildroot}%{pyver_sitelib}/oslo_utils/locale %{buildroot}%{_datadir}/locale

# Find language files
%find_lang oslo_utils --all-name

%check
%{pyver_bin} setup.py test

%files -n python%{pyver}-%{pkg_name}
%doc README.rst
%license LICENSE
%{pyver_sitelib}/oslo_utils
%{pyver_sitelib}/*.egg-info
%exclude %{pyver_sitelib}/oslo_utils/tests

%if 0%{?with_doc}
%files -n python-%{pkg_name}-doc
%doc doc/build/html
%license LICENSE
%endif

%files -n python%{pyver}-%{pkg_name}-tests
%{pyver_sitelib}/oslo_utils/tests

%files -n python-%{pkg_name}-lang -f oslo_utils.lang
%license LICENSE

%changelog
* Mon Nov 18 2019 RDO <dev@lists.rdoproject.org> 3.41.3-1
- Update to 3.41.3

* Tue Nov 05 2019 RDO <dev@lists.rdoproject.org> 3.41.2-1
- Update to 3.41.2

* Thu Oct 03 2019 Joel Capitao <jcapitao@redhat.com> 3.41.1-2
- Removed python2 subpackages in no el7 distros

* Tue Sep 17 2019 RDO <dev@lists.rdoproject.org> 3.41.1-1
- Update to 3.41.1

