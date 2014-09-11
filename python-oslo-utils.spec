# Created by pyp2rpm-1.1.0b
%global pypi_name oslo.utils

Name:           python-oslo-utils
Version:        0.3.0
Release:        1%{?dist}
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
Requires:       python-six

%description
The OpenStack Oslo Utility library.
* Documentation: http://docs.openstack.org/developer/oslo.utils
* Source: http://git.openstack.org/cgit/openstack/oslo.utils
* Bugs: http://bugs.launchpad.net/oslo


%package doc
Summary:    Documentation for the Oslo database handling library
Group:      Documentation

BuildRequires:  python-sphinx
BuildRequires:  python-oslo-sphinx

%description doc
Documentation for the Oslo database handling library.


%prep
%setup -q -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info
# Let RPM handle the dependencies
rm -f requirements.txt
# make doc build compatible with python-oslo-sphinx RPM
sed -i 's/oslosphinx/oslo.sphinx/' doc/source/conf.py


%build
%{__python2} setup.py build

# generate html docs
sphinx-build doc/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}


%install
%{__python2} setup.py install --skip-build --root %{buildroot}


%files
%doc README.rst LICENSE
%{python2_sitelib}/oslo
%{python2_sitelib}/*.egg-info
%{python2_sitelib}/*-nspkg.pth

%files doc
%doc html LICENSE

%changelog
* Thu Sep 11 2014 Alan Pevec <apevec@redhat.com> - 0.3.0-1
- update to 0.3.0

* Wed Aug 20 2014 Alan Pevec <apevec@redhat.com> - 0.2.0-1
- update to 0.2.0

* Thu Jul 31 2014 Alan Pevec <apevec@redhat.com> - 0.1.1-1
- Initial package.
