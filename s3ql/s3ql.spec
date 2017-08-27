%global s3qlversion 2.23
Name:           s3ql
Version:        %{s3qlversion}b2
Release:        1%{?dist}
Summary:        Full-Featured File System for Online Data Storage
License:        GPLv3
URL:            https://bitbucket.org/nikratio/s3ql
Source0:        https://bitbucket.org/nikratio/s3ql/downloads/s3ql-%{s3qlversion}.tar.bz2
Patch0:         https://github.com/tardfree/s3ql-rpm/raw/master/s3ql/2.21-b2-support.diff
#patch is based on diff below with some cleanup
#https://github.com/s3ql/s3ql/compare/release-2.21...sylvainlehmann:master
BuildRequires:  python3-apsw
BuildRequires:  python3-crypto
BuildRequires:  python3-devel
BuildRequires:  python3-defusedxml
BuildRequires:  python3-dugong >= 3.4
BuildRequires:  python3-llfuse
BuildRequires:  python3-pytest
BuildRequires:  python3-setuptools
BuildRequires:  python3-sphinx
BuildRequires:  python3-Cython
BuildRequires:  rsync
BuildRequires:  sqlite-devel
Requires:       python3-apsw
Requires:       python3-crypto
Requires:       python3-defusedxml
Requires:       python3-dugong >= 3.4
Requires:       python3-llfuse
Requires:       python3-requests

%description
S3QL is a file system that stores all its data online using storage services
like Google Storage, Amazon S3 or OpenStack. S3QL effectively provides a hard
disk of dynamic, infinite capacity that can be accessed from any computer
with Internet access.

S3QL is a standard conforming, full featured UNIX file system that is
conceptually indistinguishable from any local file system. Furthermore, S3QL
has additional features like compression, encryption, data de-duplication,
immutable trees and snapshotting which make it especially suitable for on-line
backup and archival.

S3QL is designed to favor simplicity and elegance over performance and feature-
creep. Care has been taken to make the source code as readable and serviceable
as possible. Solid error detection and error handling have been included
from the very first line, and S3QL comes with extensive automated test cases
for all its components.

== Features ==
* Transparency. Conceptually, S3QL is indistinguishable from a local file 
system. For example, it supports hardlinks, symlinks, standard unix 
permissions, extended attributes and file sizes up to 2 TB.

* Dynamic Size. The size of an S3QL file system grows and shrinks dynamically 
as required.

* Compression. Before storage, all data may compressed with the LZMA, bzip2 
or deflate (gzip) algorithm.

* Encryption. After compression (but before upload), all data can AES 
encrypted with a 256 bit key. An additional SHA256 HMAC checksum is used to 
protect the data against manipulation.

* Data De-duplication. If several files have identical contents, the redundant
data will be stored only once. This works across all files stored in the file 
system, and also if only some parts of the files are identical while other 
parts differ.
* Immutable Trees. Directory trees can be made immutable, so that their 
contents can no longer be changed in any way whatsoever. This can be used to 
ensure that backups can not be modified after they have been made.

* Copy-on-Write/Snapshotting. S3QL can replicate entire directory trees 
without using any additional storage space. Only if one of the copies is 
modified, the part of the data that has been modified will take up additional 
storage space. This can be used to create intelligent snapshots that preserve 
the state of a directory at different points in time using a minimum amount 
of space.

* High Performance independent of network latency. All operations that do not 
write or read file contents (like creating directories or moving, renaming, 
and changing permissions of files and directories) are very fast because they 
are carried out without any network transactions.

S3QL achieves this by saving the entire file and directory structure in a 
database. This database is locally cached and the remote copy updated 
asynchronously.

* Support for low bandwidth connections. S3QL splits file contents into 
smaller blocks and caches blocks locally. This minimizes both the number of 
network transactions required for reading and writing data, and the amount of 
data that has to be transferred when only parts of a file are read or written.

%prep
%setup -qn s3ql-%{s3qlversion}
%patch0 -p1
rm -rf doc/html/man
rm doc/html/.buildinfo
rm -rf src/%{name}.egg-info
chmod 644 contrib/*

%build
%{__python3} setup.py build

%install
%{__python3} setup.py install --prefix="%{_prefix}" -O1 --root="%{buildroot}"

#for x in contrib/*.py; do
#    f="${x##*/}"
#    case $f in
#        *dummy*) continue ;;
#        %{name}*) t="$f" ;;
#        *) t="%{name}-$f" ;;
#    esac
#    t="${t%.py}"
#    install -D -m0755 "$x" "%{buildroot}%{_bindir}/$t"
#done

find "%{buildroot}%{python3_sitearch}" -type f -name '*.py' -exec chmod 0644 {} \;
# remove shebangs
find "%{buildroot}%{python3_sitearch}" -type f -name '*.py' -exec sed -i -e '/^#!\//, 1d' {} \;

%check
# we can't test those, they use fuse and require the fuse
# kernel module to be loaded, which we cannot do from a
# chrooted package build environment where we don't run
# as root:
#rm tests/t4* tests/t5*
# running test
# Missing:
# https://pypi.python.org/simple/requests/ (disallowed host; see http://bit.ly/1dg9ijs for details).
# https://pypi.python.org/simple/ (disallowed host; see http://bit.ly/1dg9ijs for details).
#python3-requests
#%{__python3} setup.py test

%files
%doc doc/html doc/manual.pdf contrib/
%doc Changes.txt LICENSE
%{_bindir}/fsck.s3ql
%{_bindir}/mkfs.s3ql
%{_bindir}/*mount.s3ql
%{_bindir}/s3ql*
%{_mandir}/man1/fsck*.1*
%{_mandir}/man1/mkfs.s3ql*
%{_mandir}/man1/*mount.s3ql*
%{_mandir}/man1/s3ql*.1*
%{python3_sitearch}/%{name}*

%changelog
* Sun Aug 27 2017 Robert Harrison <robert@splat.cx> - 2.23b2-1
- Update to 2.23

* Wed Jul 19 2017 Robert Harrison <robert@splat.cx> - 2.22b2-1
- Update to 2.22
- Included the backblaze b2 provider patch from https://github.com/sylvainlehmann/s3ql

* Fri May 20 2016 Athmane Madjoudj <athmane@fedoraproject.org> - 2.18-1
- Update to 2.18 (rhbz #1249301)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.13-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Mon Jul 13 2015 Marcel Wysocki <maci@satgnu.net> - 2.13-2
- Add missing dependencies python3-requests and python3-dugong>=3.4

* Mon Jun 29 2015 Marcel Wysocki <maci@satgnu.net> - 2.13-1
- Update to 2.13

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 01 2014 Christopher Meng <rpm@cicku.me> - 2.9-1
- Update to 2.9

* Thu Jun 12 2014 Christopher Meng <rpm@cicku.me> - 2.8.1-1
- Update to 2.8.1

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Sep 24 2013 Marcel Wysocki <maci@satgnu.net> - 2.4-1
- updated to version 2.4, all python3

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 04 2013 Marcel Wysocki <maci@satgnu.net> - 1.13.2-1
- updated to version 1.13.2
- add pytest BR
- fixes BZ#914501

* Fri Feb 15 2013 Marcel Wysocki <maci@satgnu.net> - 1.12-9
- rebuilt

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Nov 02 2012 Marcel Wysocki <maci@satgnu.net> 1.12-7
- python-argparse is provided by python-libs, remove it from requires

* Fri Nov 02 2012 Marcel Wysocki <maci@satgnu.net> 1.12-6
- fixed ownership /usr/lib*/python*/site-packages/s3ql*
- added LICENSE

* Fri Nov 02 2012 Marcel Wysocki <maci@satgnu.net> 1.12-5
- filter out private shared objects
- replace tabs by spaces
- clean up requires and buildrequires
- remove egg-info

* Thu Nov 01 2012 Marcel Wysocki <maci@satgnu.net> 1.12-4
- use python-setuptools instead of python-distribute
- add pyliblzma to BR

* Wed Oct 31 2012 Marcel Wysocki <maci@satgnu.net> 1.12-3
- remove python from deps, rpm knows it
- use python2-devel in BR

* Tue Oct 23 2012 Marcel Wysocki <maci@satgnu.net> 1.12-2
- don't use rm and install macros
- add missing dependencies

* Thu Oct 04 2012 Marcel Wysocki <maci@satgnu.net> 1.12-1
- update to 1.12
- fedora port
- fixed dependencies
