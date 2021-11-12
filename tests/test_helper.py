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

"""Test helper functions from image-factory."""

import unittest

from image_factory import parse_bytes


class TestParseBytes(unittest.TestCase):
    """
    This unittest class tests parse_bytes().
    """

    def test_parse_1_g(self):
        """Test parse_bytes("1G")"""
        self.assertEqual(parse_bytes("1G"), 1073741824)

    def test_parse_2_tb(self):
        """Test parse_bytes("2 TB")"""
        self.assertEqual(parse_bytes("2 TB"), 2000000000000)

    def test_parse_512_mib(self):
        """Test parse_bytes("512 MiB")"""
        self.assertEqual(parse_bytes("512 MiB"), 536870912)

    def test_invalid(self):
        """Test parse_bytes("invalid")"""
        with self.assertRaises(ValueError):
            parse_bytes("invalid")
