# Copyright (C) 2019, Benjamin Drung <benjamin.drung@cloud.ionos.com>
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

"""Test image-factory-sudo-helper script."""

import os
import subprocess
import unittest


class TestSudoHelper(unittest.TestCase):
    """
    This unittest class tests the image-factory-sudo-helper script.
    """

    SCRIPT = os.path.join(os.path.dirname(__file__), "..", "image-factory-sudo-helper")

    def call_helper(self, cmd, silence=False):
        """Call the image-factory-sudo-helper script in dryrun mode."""
        return subprocess.call(
            [self.SCRIPT] + cmd,
            stdout=subprocess.DEVNULL,
            env={"DRYRUN": "1"},
            stderr=subprocess.DEVNULL if silence else None,
        )

    def test_mount(self):
        """Test mounting."""
        cmd = ["mount", "/dev/loop0", "/tmp/image-factory._3gm0lem"]
        self.assertEqual(self.call_helper(cmd), 0)

    def test_chmod_root(self):
        """Test chmod mounted /root"""
        cmd = ["chmod", "o+rwx", "/tmp/image-factory._3gm0lem/root"]
        self.assertEqual(self.call_helper(cmd), 0)

    def test_chmod_var_log(self):
        """Test write access for mounted /var/log/..."""
        cmd = ["chmod", "o+w", "/tmp/image-factory.8a9573rd/var/log"]
        self.assertEqual(self.call_helper(cmd), 0)

    def test_chmod_dnf_log(self):
        """Test read access for dnf log file."""
        cmd = ["chmod", "o+r", "/tmp/image-factory.umh1oz39/var/log/anaconda/dnf.librepo.log"]
        self.assertEqual(self.call_helper(cmd), 0)

    def test_chmod_log_file(self):
        """Test read access for mounted /var/log/..."""
        cmd = ["chmod", "o+r", "/tmp/image-factory._3gm0lem/var/log/anaconda/journal.log"]
        self.assertEqual(self.call_helper(cmd), 0)

    def test_chmod_recursive(self):
        """Test chmod recursively"""
        cmd = ["chmod", "-R", "o+rwx", "/tmp/image-factory._3gm0lem/var/log/anaconda"]
        self.assertEqual(self.call_helper(cmd), 0)

    def test_chmod_remove_root(self):
        """Test chmod remove mounted /root permission"""
        cmd = ["chmod", "o-rwx", "/tmp/image-factory._3gm0lem/root"]
        self.assertEqual(self.call_helper(cmd), 0)

    def test_umount(self):
        """Test unmounting."""
        cmd = ["umount", "/tmp/image-factory._3gm0lem"]
        self.assertEqual(self.call_helper(cmd), 0)

    def test_reject_escaping(self):
        """Test rejecting ../../etc/shadow."""
        cmd = ["chmod", "o+rwx", "/tmp/image-factory._3gm0lem/../../etc/shadow"]
        self.assertEqual(self.call_helper(cmd, silence=True), 1)
