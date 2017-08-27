# s3ql-rpm
Packaged version of s3ql for use in fedora copr.

This version includes the experimental b2 backend patch.

* Original sources: https://github.com/s3ql/s3ql
* B2 backend patch from: https://github.com/sylvainlehmann/s3ql

To build:

1 - Build dugong which is a prerequisite

```shell
cd python3-dugong
spectool -g python3-dugong.spec
rpmbuild -bs python3-dugong.spec
mock -r fedora-25-x86_64 --no-clean --rebuild ~/rpmbuild/SRPMS/python3-dugong-3.7.1-1.fc25.src.rpm
or
copr-cli build tardfree/s3ql-rpm ~/rpmbuild/SRPMS/python3-dugong-3.7.1-1.fc25.src.rpm
```

1a - If using Mock, install the pre-req packages in the mock chroot.

```shell
mock -r fedora-25-x86_64 --no-clean --install /var/lib/mock/fedora-25-x86_64/result/python3-dugong*.noarch.rpm
```

2 - Build s3ql package now

```shell
cd s3ql
spectool -g s3ql.spec
rpmbuild -bs s3ql.spec
mock -r fedora-25-x86_64 --no-clean --rebuild ~/rpmbuild/SRPMS/s3ql-2.23b2-1.fc25.src.rpm
or
copr-cli build tardfree/s3ql-rpm ~/rpmbuild/SRPMS/s3ql-2.23b2-1.fc25.src.rpm
```

Please raise any package specific issues with these packages in [this repo](https://github.com/tardfree/s3ql-rpm).

-Rob

