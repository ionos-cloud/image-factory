image-factory 1.0.2 (2021-11-12)
================================

* Fix issues found by pylint 2.11.1
  (fixes [Debian bug #998571](https://bugs.debian.org/998571)):
  * tests: Use `with` for `subprocess.Popen` and `open` calls
  * Open log files explicitly as UTF-8
  * Replace `.format()` with f-strings
* Drop Python 2 support
* Update my email address to @ionos.com
* tests: Add black code formatting check
* tests: Check import definitions order with isort
* tests: Fix running tests as root
* tests: Disable bad-continuation for pylint (for Ubuntu 20.04)
* Use ftp.rz.uni-frankfurt.de as example CentOS mirror (old mirror is gone)

image-factory 1.0.1 (2021-01-29)
================================

* Update example CentOS 7 mirror URL (old URL does not work any more)
* Increase CentOS 7 image size from 2 GiB to 3 GiB

image-factory 1.0.0 (2020-08-11)
================================

* Initial release
