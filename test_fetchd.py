#!/usr/bin/env python3
"""Tests for fetchd CLI tool."""

import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import responses

import fetchd


HTML_SAMPLE = b'<h1>Test Title</h1><p>Test paragraph with <strong>bold</strong>.</p>'
HTML_TABLE = b'<table><tr><th>Name</th><th>Value</th></tr><tr><td>Item1</td><td>100</td></tr></table>'
HTML_SCRIPT = b'<html><head><script>alert("bad");</script></head><body><h1>Content</h1></body></html>'


@responses.activate
class TestFetchd(unittest.TestCase):
    """Test fetchd behavior."""

    def test_converts_html_to_markdown(self):
        """Should convert HTML from URL to markdown."""
        url = 'https://example.com/page'
        responses.add(responses.GET, url, body=HTML_SAMPLE, status=200)

        with patch.object(sys, 'argv', ['fetchd', url]):
            with patch('builtins.print') as mock_print:
                fetchd.main()
                output = mock_print.call_args.args[0]
                self.assertIn('Test Title', output)
                self.assertIn('Test paragraph', output)

    def test_handles_http_errors(self):
        """Should raise error on 404."""
        url = 'https://example.com/missing'
        responses.add(responses.GET, url, status=404)

        with patch.object(sys, 'argv', ['fetchd', url]):
            with self.assertRaises(Exception):
                fetchd.main()

    def test_converts_tables(self):
        """Should convert HTML tables to markdown tables."""
        url = 'https://example.com/table'
        responses.add(responses.GET, url, body=HTML_TABLE, status=200)

        with patch.object(sys, 'argv', ['fetchd', url]):
            with patch('builtins.print') as mock_print:
                fetchd.main()
                output = mock_print.call_args.args[0]
                self.assertIn('Name', output)
                self.assertIn('Item1', output)

    def test_strips_script_tags(self):
        """Should exclude script tags from output."""
        url = 'https://example.com/scripted'
        responses.add(responses.GET, url, body=HTML_SCRIPT, status=200)

        with patch.object(sys, 'argv', ['fetchd', url]):
            with patch('builtins.print') as mock_print:
                fetchd.main()
                output = mock_print.call_args.args[0]
                self.assertIn('Content', output)
                self.assertNotIn('alert', output)

    def test_converts_local_file(self):
        """Should convert local HTML file to markdown."""
        with tempfile.NamedTemporaryFile(mode='wb', suffix='.html', delete=False) as f:
            f.write(HTML_SAMPLE)
            filepath = f.name

        try:
            with patch.object(sys, 'argv', ['fetchd', filepath]):
                with patch('builtins.print') as mock_print:
                    fetchd.main()
                    output = mock_print.call_args.args[0]
                    self.assertIn('Test Title', output)
        finally:
            Path(filepath).unlink()

    @responses.activate
    def test_enable_plugins_flag(self):
        """Should pass --enable-plugins to MarkItDown."""
        mock_result = Mock()
        mock_result.text_content = 'output'

        with patch('fetchd.MarkItDown') as mock_md:
            mock_md.return_value.convert_stream.return_value = mock_result
            url = 'https://example.com'
            responses.add(responses.GET, url, body=b'content', status=200)

            with patch.object(sys, 'argv', ['fetchd', url, '--enable-plugins']):
                fetchd.main()
                self.assertTrue(mock_md.call_args.kwargs.get('enable_plugins'))


if __name__ == '__main__':
    unittest.main()
