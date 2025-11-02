#!/usr/bin/env python3
"""Behavior tests for fetchd CLI tool."""

import unittest
from unittest.mock import Mock, patch
import sys

import responses

import fetchd


# Test data constants
TEST_URL = 'https://example.com'
HTML_WITH_HEADING = b'<h1>Test Title</h1><p>Test paragraph with <strong>bold</strong>.</p>'
HTML_TABLE = b'<table><tr><th>Name</th><th>Value</th></tr><tr><td>Item1</td><td>100</td></tr></table>'
HTML_WITH_SCRIPT = b'<html><head><script>alert("bad");</script></head><body><h1>Content</h1></body></html>'


@responses.activate
class TestFetchdBehavior(unittest.TestCase):
    """Test fetchd end-to-end behavior."""

    def test_converts_html_to_markdown(self) -> None:
        """Given HTML at URL, should output markdown."""
        responses.add(
            responses.GET,
            f'{TEST_URL}/page',
            body=HTML_WITH_HEADING,
            status=200,
            content_type='text/html'
        )

        with patch.object(sys, 'argv', ['fetchd', f'{TEST_URL}/page']):
            with patch('builtins.print') as mock_print:
                fetchd.main()

                printed_output = mock_print.call_args.args[0]
                self.assertIn('Test Title', printed_output)
                self.assertIn('Test paragraph', printed_output)

    def test_handles_http_errors_gracefully(self) -> None:
        """Given 404, should raise appropriate error."""
        responses.add(responses.GET, f'{TEST_URL}/missing', status=404)

        with patch.object(sys, 'argv', ['fetchd', f'{TEST_URL}/missing']):
            with self.assertRaises(Exception):
                fetchd.main()

    def test_converts_tables_to_markdown(self) -> None:
        """Given HTML table, should output markdown table."""
        responses.add(
            responses.GET,
            f'{TEST_URL}/table',
            body=HTML_TABLE,
            status=200
        )

        with patch.object(sys, 'argv', ['fetchd', f'{TEST_URL}/table']):
            with patch('builtins.print') as mock_print:
                fetchd.main()

                printed_output = mock_print.call_args.args[0]
                self.assertIn('Name', printed_output)
                self.assertIn('Value', printed_output)
                self.assertIn('Item1', printed_output)

    def test_strips_script_tags(self) -> None:
        """Given HTML with script tags, should exclude them from output."""
        responses.add(
            responses.GET,
            f'{TEST_URL}/scripted',
            body=HTML_WITH_SCRIPT,
            status=200
        )

        with patch.object(sys, 'argv', ['fetchd', f'{TEST_URL}/scripted']):
            with patch('builtins.print') as mock_print:
                fetchd.main()

                printed_output = mock_print.call_args.args[0]
                self.assertIn('Content', printed_output)
                self.assertNotIn('alert', printed_output)


class TestFetchdOptions(unittest.TestCase):
    """Test that CLI options affect behavior."""

    @responses.activate
    def test_enable_plugins_flag_is_passed(self) -> None:
        """When --enable-plugins is passed, should enable plugins."""
        mock_result = Mock()
        mock_result.text_content = 'output'

        with patch('fetchd.MarkItDown') as mock_md_class:
            mock_md_class.return_value.convert_stream.return_value = mock_result

            responses.add(responses.GET, TEST_URL, body=b'content', status=200)

            with patch.object(sys, 'argv', ['fetchd', TEST_URL, '--enable-plugins']):
                fetchd.main()

                call_kwargs = mock_md_class.call_args.kwargs
                self.assertTrue(call_kwargs.get('enable_plugins'))


if __name__ == '__main__':
    unittest.main()
