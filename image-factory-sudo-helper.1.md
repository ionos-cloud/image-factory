---
date: 2020-08-05
footer: image-factory-sudo-helper
header: "image-factory-sudo-helper's Manual"
layout: page
license: 'Licensed under the ISC license'
section: 1
title: IMAGE-FACTORY-SUDO-HELPER
---

# NAME

image-factory-sudo-helper - Run certain commands as root

# SYNOPSIS

**image-factory-sudo-helper** **COMMAND**

# DESCRIPTION

**image-factory** can be run as normal user, but it need root permission for a
few operations like chmod, mount, and umount. Since these operations cannot be
secured with sudo's wildcards, **image-factory-sudo-helper** was introduced to
check the commands using regular expression.

**image-factory-sudo-helper** will take a command (including parameters) and
checks if it one of the three allowed commands:

* chmod on files or (sub-)directories in /tmp/image-factory

* mount of loop device in /tmp/image-factory

* umount in /tmp/image-factory

If the given command passes is one of the allowed commands, it will be
executed. Otherwise an error message will be printed.

# USAGE

To allow running **image-factory** as normal user, only
**image-factory-sudo-helper** needs sudo permission for the user. Example sudo
configuration for user *jenkins*:

```
jenkins ALL = NOPASSWD:SETENV: /usr/bin/image-factory-sudo-helper
```

# ENVIRONMENT

If the environment variable **DRYRUN** is set, the given command will not be
executed but printed instead.

# AUTHOR

Benjamin Drung <benjamin.drung@ionos.com>
