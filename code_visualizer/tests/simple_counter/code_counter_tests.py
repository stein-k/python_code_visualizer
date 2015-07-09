"""
Tests the simple counter on simple input
"""

import unittest

from simple_counter.code_counter import get_counters_for_file


class TestUncommentedCode(unittest.TestCase):

    def test_empty_string(self):
        expected_count = {'lines': 1, 'empty_lines': 1, 'comment_lines': 0}
        counters_for_input = get_counters_for_file('')
        self.assertEqual(counters_for_input, expected_count)
