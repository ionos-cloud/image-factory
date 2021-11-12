# Copyright (C) 2019, Benjamin Drung <benjamin.drung@ionos.com>
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

"""Test command-line related functions from image-factory."""

import configparser
import os
import unittest

from image_factory import get_config, override_configs_by_args, parse_args


class TestCLI(unittest.TestCase):
    """
    This unittest class tests command-line related functions from image-factory.
    """

    def test_empty_config(self):
        """Test empty configuration file."""
        args = parse_args(["Debian-10-server"])
        config = configparser.ConfigParser()
        override_configs_by_args(config, args)
        self.assertTrue(config.has_section("Debian-10-server"))
        self.assertEqual(
            config.items("Debian-10-server"), [("cache_dir", "~/.cache/image-factory")]
        )

    def test_example_config(self):
        """Test exapmle image-factory.conf file."""
        config_file = os.path.join(os.path.dirname(__file__), "..", "image-factory.conf")
        os.environ["IMAGE_FACTORY_CONFIG"] = config_file
        args = parse_args(["--format", "raw", "Debian-10-server"])
        config = get_config()
        override_configs_by_args(config, args)
        self.assertTrue(config.has_section("Debian-10-server"))
        self.assertEqual(
            config.items("Debian-10-server"),
            [
                ("data_dir", "/usr/share/image-factory"),
                ("cores", "1"),
                ("format", "raw"),
                ("keep-raw", "False"),
                ("installer-logs", "True"),
                ("log-file", "True"),
                ("ram", "1G"),
                ("centos_mirror", "rsync://mirror2.hs-esslingen.de/centos"),
                ("debian_mirror", "rsync://ftp.de.debian.org/debian"),
                ("ubuntu_mirror", "http://de.archive.ubuntu.com/ubuntu"),
                ("fedora_mirror", "rsync://ftp.fau.de/fedora"),
                ("opensuse_mirror", "rsync://ftp.halifax.rwth-aachen.de/opensuse"),
                ("dist", "buster"),
                (
                    "initrd",
                    "rsync://ftp.de.debian.org/debian/dists/buster/main/installer-amd64/"
                    "current/images/netboot/debian-installer/amd64/initrd.gz",
                ),
                (
                    "linux",
                    "rsync://ftp.de.debian.org/debian/dists/buster/main/installer-amd64/"
                    "current/images/netboot/debian-installer/amd64/linux",
                ),
                ("preseed", "/usr/share/image-factory/Debian-10-server-de.cfg"),
                (
                    "append",
                    "auto-install/enable=true keymap=us hostname=debian "
                    "domain=unassigned-domain vga=771 d-i -- quiet",
                ),
                ("vnc", "localhost:13"),
                ("cache_dir", "~/.cache/image-factory"),
            ],
        )

    def test_override_cache_dir(self):
        """Test overriding the cache directory."""
        args = parse_args(["--cache-dir", "/var/cache/example", "Debian-10-server"])
        config = configparser.ConfigParser()
        config[config.default_section] = {}
        config[config.default_section]["cache_dir"] = "~/.cache/image-factory"
        override_configs_by_args(config, args)
        self.assertTrue(config.has_section("Debian-10-server"))
        self.assertEqual(config.items("Debian-10-server"), [("cache_dir", "/var/cache/example")])
