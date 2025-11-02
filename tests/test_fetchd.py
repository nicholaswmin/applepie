#!/usr/bin/env python3
"""Unit tests for fetchd module."""

import unittest
import argparse

from fetchd import extract_converter_options


class TestExtractConverterOptions(unittest.TestCase):
    """Test MarkItDown option extraction from args."""

    def test_excludes_url(self):
        """Should exclude URL from converter options."""
        args = argparse.Namespace(url='http://example.com', llm_model='gpt-4o')
        options = extract_converter_options(args)
        self.assertNotIn('url', options)

    def test_excludes_none_values(self):
        """Should exclude None values from options."""
        args = argparse.Namespace(url='http://example.com', llm_model=None)
        options = extract_converter_options(args)
        self.assertNotIn('llm_model', options)

    def test_includes_valid_options(self):
        """Should include non-None options."""
        args = argparse.Namespace(
            url='http://example.com',
            llm_model='gpt-4o',
            enable_plugins=True
        )
        options = extract_converter_options(args)
        self.assertEqual(options['llm_model'], 'gpt-4o')
        self.assertTrue(options['enable_plugins'])


if __name__ == '__main__':
    unittest.main()
