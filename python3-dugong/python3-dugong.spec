Name:           python3-dugong
Version:        3.7.1
Release:        1%{?dist}
Summary:        Python 3.x HTTP 1.1 client module
License:        Python
URL:            https://bitbucket.org/nikratio/python-dugong

%global gitowner nikratio
%global gitreponame python-dugong
%global gittag0 release-%{version}
%global shortcommit0 c04533401178

Source0:        https://bitbucket.org/nikratio/python-dugong/get/%{gittag0}.tar.bz2
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-pytest
BuildRequires:  python3-setuptools

%description
The Python Dugong module provides an API for communicating with HTTP 1.1 
servers. It is an alternative to the standard library's http.client 
(formerly httplib) module. In contrast to http.client, Dugong:

- Allows you to send multiple requests right after each other without 
having to read the responses first.

- Supports waiting for 100-continue before sending the request body.

- Raises an exception instead of silently delivering partial data if the 
connection is closed before all data has been received.

- Raises one specific exception (ConnectionClosed) if the connection has been
closed (while http.client connection may raise any of BrokenPipeError, 
~http.client.BadStatusLine, ConnectionAbortedError, ConnectionResetError,
~http.client.IncompleteRead or simply return '' on read)

- Supports non-blocking, asynchronous operation and is compatible with the 
asyncio module.

- Not compatible with old HTTP 0.9 or 1.0 servers.

All request and response headers are represented as str, but must be encodable
in latin1. Request and response body must be bytes-like objects or binary 
streams.

%prep
%autosetup -n %{gitowner}-%{gitreponame}-%{shortcommit0}
rm -frv dugong.egg-info

%build
%{__python3} setup.py build

%install
%{__python3} setup.py install -O1 --skip-build --root=%{buildroot}

%check
#py.test-%{python3_version} test

%files
%doc Changes.rst LICENSE README.rst
%{python3_sitelib}/dugong/
%{python3_sitelib}/dugong-%{version}-py%{python3_version}.egg-info/

%changelog
* Wed Jul 19 2017 Robert Harrison <robert@splat.cx> - 3.7.1-1
- Update to 3.7.1

* Wed Jul 22 2015 Marcel Wysocki <maci@satgnu.net> - 3.5-1
- Update to 3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Aug 07 2014 Christopher Meng <rpm@cicku.me> - 3.3-1
- Update to 3.3

* Fri Aug 01 2014 Christopher Meng <rpm@cicku.me> - 3.2-1
- Update to 3.2

* Tue Jul 01 2014 Christopher Meng <rpm@cicku.me> - 3.1-1
- Update to 3.1

* Thu Jun 19 2014 Christopher Meng <rpm@cicku.me> - 3.0-1
- Initial Package.
