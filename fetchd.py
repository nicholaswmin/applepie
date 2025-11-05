#!/usr/bin/env python3
"""Fetch URLs or files and convert to markdown."""

import argparse
import warnings
from io import BytesIO
from pathlib import Path

# Suppress pydub ffmpeg warning before imports
warnings.filterwarnings("ignore", message="Couldn't find ffmpeg or avconv")

import requests
from markitdown import MarkItDown


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Fetch URL or file and convert to markdown"
    )
    parser.add_argument("source", help="URL or filepath")
    parser.add_argument("--llm-model", help="LLM model for image descriptions")
    parser.add_argument("--llm-prompt", help="Custom prompt for image descriptions")
    parser.add_argument("--exiftool-path", help="Path to exiftool binary")
    parser.add_argument("--enable-plugins", action="store_true",
                       help="Enable 3rd-party plugins")
    return parser.parse_args()


def fetch_url(url):
    """Fetch content from URL."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15",
        "Accept": "*/*"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.content


def read_file(filepath):
    """Read content from local file."""
    return Path(filepath).read_bytes()


def to_markdown(content, **options):
    """Convert binary content to markdown."""
    converter = MarkItDown(**options)
    result = converter.convert_stream(BytesIO(content))
    return result.text_content


def main():
    """Main entry point."""
    args = parse_args()

    # Extract converter options
    options = {k: v for k, v in vars(args).items()
              if k != "source" and v is not None}

    # Fetch or read content
    if args.source.startswith(("http://", "https://")):
        content = fetch_url(args.source)
    else:
        content = read_file(args.source)

    # Convert and output
    markdown = to_markdown(content, **options)
    print(markdown)


if __name__ == "__main__":
    main()
