image-factory
=============

image-factory is a command line tool for building golden Linux images. It uses
virt-install to do installations via the network. The installation and
configuration of the images is done using the netinstall support from the
distributions, i.e.

* preseed for Debian/Ubuntu
* Kickstart for CentOS/Fedora
* AutoYaST for openSUSE

image-factory is used by IONOS Cloud to build the golden public Linux images
for their Enterprise Cloud. The configuration files are shipped with this
project to allow anyone to rebuild their images.

image-factory runs following steps:

* Create a virtual RAW image using `qemu-img`.

* Cache `linux` kernel and `initrd`.

* Run installation using `virt-install`. `qemu:///session` is used as session
for normal users and `qemu:///system` when run as root.

* The installation partition is mounted and the installer logs are removed.

* `zerofree` is run on the partition.

* If `format` is set to `qcow2`, the virtual raw images will be converted
to `qcow2` using `qemu-img`.

* The SHA 256 sum is calculated for the image.

* The image will be uploaded to all locations configured in
`upload_destinations`.

* If `post-build-command` is configured, the specified command will be
executed.

Dependencies
============

These components are needed to run `image-factory`:

* Python 3
* Python modules:
  * httplib2
  * parted
* qemu-utils for `qemu-img`
* virtinst for `virt-install`
* zerofree

pandoc is needed to generate the man page.

The test cases have additional requirements:

* black
* flake8
* isort
* pylint

Permissions
===========

`image-factory` can be run as normal user, but it need root permission for a
few operations like chmod, mount, and umount. Since these operations cannot be
secured with sudo's wildcards, `image-factory-sudo-helper` was introduced to
check the commands using regular expression.

To allow running `image-factory` as normal user, only
`image-factory-sudo-helper` needs sudo permission for the user. Example sudo
configuration for user `jenkins`:

```
jenkins ALL = NOPASSWD:SETENV: /usr/bin/image-factory-sudo-helper
```

On Debian and Ubuntu, the user has to be in the group `disk` to get the
permission for mounting loop devices.

Alternatives
============

HashiCorp Packer
----------------

[HashiCorp Packer](https://www.packer.io/) automates the creation of any type
of machine image (including non *nix). The
[QEMU Builder](https://www.packer.io/docs/builders/qemu) can provide a similar
functionality to `image-factory`.

While HashiCorp Packer takes an URL pointing to an installer ISO,
`image-install` uses the smaller netinstall kernel and initrd files instead.

HashiCorp Packer provides post-processors that can enable the remaining
functionality of `image-factory`, namely
[checksum](https://www.packer.io/docs/post-processors/checksum) and
[local shell](https://www.packer.io/docs/post-processors/shell-local) to upload
the images via rsync, however there is currently no dedicated post-processor
for it. `image-factory` supports rsync uploads via configuration option.

Contributing
============

Contributions are welcome. The source code has test coverage, which should be
preserved or increased. So please provide a test case for each bugfix and one
or more test cases for each new feature. Please follow
[How to Write a Git Commit Message](https://chris.beams.io/posts/git-commit/)
for writing good commit messages.

Creating releases
=================

To create a release, increase the version in `Makefile`, document the
noteworthy changes in [NEWS.md](./NEWS.md), and commit and tag the release:

```sh
git commit -s -m "Release image-factory $(make version)" Makefile NEWS.md
git tag "$(make version)" -m "Release image-factory $(make version)"
```

The xz-compressed release tarball can be generated by running:
```sh
make dist
```
