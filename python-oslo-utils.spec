# Created by pyp2rpm-1.1.0b
%global pypi_name oslo.utils

Name:           python-oslo-utils
Version:        2.2.0
Release:        2%{?dist}
Summary:        OpenStack Oslo Utility library

License:        ASL 2.0
URL:            http://launchpad.net/oslo
Source0:        https://pypi.python.org/packages/source/o/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

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

%description
The OpenStack Oslo Utility library.
* Documentation: http://docs.openstack.org/developer/oslo.utils
* Source: http://git.openstack.org/cgit/openstack/oslo.utils
* Bugs: http://bugs.launchpad.net/oslo


%package doc
Summary:    Documentation for the Oslo Utility library
Group:      Documentation

BuildRequires:  python-sphinx
BuildRequires:  python-oslo-sphinx
# for API autodoc
BuildRequires:  python-netifaces
BuildRequires:  python-debtcollector

%description doc
Documentation for the Oslo Utility library.


%prep
%setup -q -n %{pypi_name}-%{version}

# Let RPM handle the dependencies
rm -f requirements.txt


%build
%{__python2} setup.py build

# generate html docs
sphinx-build doc/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}


%install
%{__python2} setup.py install --skip-build --root %{buildroot}


%files
%doc README.rst
%license LICENSE
%{python2_sitelib}/oslo_utils
%{python2_sitelib}/*.egg-info

%files doc
%doc html
%license LICENSE

%changelog
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
