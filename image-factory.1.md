---
date: 2020-08-05
footer: image-factory
header: "image-factory's Manual"
layout: page
license: 'Licensed under the ISC license'
section: 1
title: IMAGE-FACTORY
---

# NAME

image-factory - build golden Linux images

# SYNOPSIS

**image-factory** [**-h**|**\--help**] [**-c**|**\--cache-dir** *CACHE_DIR*]
[**-f**|**\--format** {*qcow2*,*raw*}] [**\--image-size** *IMAGE_SIZE*]
[**\--mac** *MAC*] [**\--installer-logs**] [**\--no-installer-logs**]
[**\--log-file**] [**\--no-log-file**] [**\--log-filename** *LOG_FILENAME*]
*image*

# DESCRIPTION

**image-factory** is a command line tool for building golden Linux images. It
uses **virt-install** to do installations via the network. The installation and
configuration of the images is done using the netinstall support from the
distributions, i.e.

* preseed for Debian/Ubuntu
* Kickstart for CentOS/Fedora
* AutoYaST for openSUSE

**image-factory** is used by IONOS Cloud to build the golden public Linux
images for their Enterprise Cloud. The configuration files are shipped with
this project to allow anyone to rebuild their images.

**image-factory** runs following steps:

* Create a virtual RAW image using qemu-img.

* Cache **linux** kernel and **initrd**.

* Run installation using **virt-install**. *qemu:///session* is used as session
for normal users and *qemu:///system* when run as root.

* The installation partition is mounted and the installer logs are removed.

* **zerofree** is run on the partition.

* If **format** is set to *qcow2*, the virtual raw images will be converted
to qcow2 using **qemu-img**.

* The SHA 256 sum is calculated for the image.

* The image will be uploaded to all locations configured in
**upload_destinations**.

* If **post-build-command** is configured, the specified command will be
executed.

# OPTIONS

**-h**, **\--help**
:    Show a help message and exit

**-c** *CACHE_DIR*, **\--cache-dir** *CACHE_DIR*
:    Cache directory (default: *~/.cache/image-factory* or
*var/cache/image-factory* for root)

**-f** {*qcow2*,*raw*}, **\--format** {*qcow2*,*raw*}
:    Image format to use (default: *raw*)

**\--image-size** *IMAGE_SIZE*
:    Size of the raw image (default: *2G*)

**\--mac** *MAC*
:    MAC address used in the installation machine

**\--installer-logs**
:    Print installer logs into logging output

**\--no-installer-logs**
:    Do not print installer logs into logging output

**\--log-file**
:    Store logs into a file (in addition to stdout/stderr)

**\--no-log-file**
:    Do not store logs into a file (in addition to stdout/stderr)

**\--log-filename** *LOG_FILENAME*
:    log into specified file

*image*
:    Image to build. The date in form of *YYYY-MM-DD* and the file format
suffix will be added to the generated image filename.

# CONFIGURATION

Each image needs to be also configured in */etc/image-factory.conf* or
*~/.config/image-factory.conf*. These configuration files use the INI
file format. The image name will be used as section and following keys are
used:

**append**
:    Extra kernel parameter for the netboot image to use

**cache_dir**
:    Cache directory (default: *~/.cache/image-factory* or
*var/cache/image-factory* for root). Can be overridden by **\--cache-dir**.

**cores**
:    Number of CPU cores to use during installation. Default: *1*

**format**
:    Image format to use. Can be *qcow2* or *raw* (default). Can be overridden
by **\--format**.

**image-size**
:    Size of the raw image (default: *2G*). Can be overridden by
**\--image-size**.

**initrd**
:    URI of the netboot installer initrd. Supported schemes are *file:*,
*http:*, *https:*, and *rsync:*. Unless using *file:*, the specified initrd
will be cached locally.

**installer-logs**
:    Boolean whether to print installer logs into logging output. Can be
overridden by **\--installer-logs** or **\--no-installer-logs**.

**keep-raw**
:    Boolean whether to keep raw image (in case format is not raw). Default is
*False*.

**kickstart**
:    Filename of the Kickstart file. Needed when using Kickstart on
CentOS/Fedora.

**linux**
:    URI of the netboot installer Linux kernel. Supported schemes are *file:*,
*http:*, *https:*, and *rsync:*. Unless using *file:*, the specified kernel
will be cached locally.

**log-file**
:    Boolean whether to store logs into a file (in addition to stdout/stderr).
Can be overridden by **\--log-file** or **\--no-log-file**.

**log-filename**
:    Filename to log into (if enabled). Can be overridden by
**\--log-filename**.

**mac**
:    MAC address used in the installation machine. Can be overridden by
**\--mac**.

**post-build-command**
:    Optional command to run after the image was successfully built. The name
of the image will be passed as first argument.

**preseed**
:    Filename of the preseed file. Needed when using preseed on Debian/Ubuntu.

**ram**
:    Memory for virtual machine to use during installation.

**upload_destinations**
:    Comma-separated list of upload destinations. Each upload destination
needs a section in the configuration file (see UPLOAD DESTINATION CONFIGURATION
below). To disable the upload, let **upload_destinations** undefined or set to
an empty string.

**vnc**
:    VNC port for the installation virtual machine. It is recommended to bind
the VNC port to localhost only.

**yast**
:    Filename of the AutoYaST file. Needed when using AutoYaST on openSUSE.

# UPLOAD DESTINATION CONFIGURATION

Each upload destination configured in **upload_destinations** needs a section
in the INI configuration, where at least **upload_type** and **upload_target**
are set. Following keys are accepted:

**post-upload-command**
:    Additional command to run after a successful upload. *${image}* can be
used as parameter in post-upload-command. If multiple commands are needed,
suffix the key with a number (counting up from 1), e.g.
**post-upload-command1**.

**upload_args**
:    Additional arguments for the upload command to use, e.g. *\--progress*
for uploads with rsync.

**upload_target**
:    Upload target in the format the upload type supports it.

**upload_type**
:    Type of upload. Currently only *rsync* is supported.

# SEE ALSO

qemu-img(1), virt-install(1), zerofree(8)

# AUTHOR

Benjamin Drung <benjamin.drung@cloud.ionos.com>
