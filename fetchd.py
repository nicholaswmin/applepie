#!/usr/bin/env python3
"""Fetch URLs and convert to markdown with configurable LLM support.

A command-line tool that fetches web content and converts it to markdown
format using the markitdown library, with optional LLM-powered image
descriptions.
"""

# pyright: reportMissingImports=false, reportUnknownMemberType=false
# pyright: reportUnknownArgumentType=false, reportMissingModuleSource=false
# pyright: reportUnknownVariableType=false

from __future__ import annotations

import argparse
from io import BytesIO
from typing import Any

import requests
from fake_useragent import UserAgent
from markitdown import MarkItDown


# HTTP header constants
DEFAULT_ACCEPT = "*/*"
DEFAULT_ACCEPT_LANGUAGE = "*"
DEFAULT_ACCEPT_ENCODING = "gzip, deflate"
DEFAULT_CONNECTION = "keep-alive"


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments.

    Returns:
        Parsed arguments namespace containing URL and optional
        MarkItDown configuration parameters.
    """
    parser = argparse.ArgumentParser(
        description="Fetch URL and convert to markdown",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("url", help="URL to fetch")
    parser.add_argument(
        "--llm-model",
        dest="llm_model",
        help="LLM model for image descriptions (e.g., gpt-4o)"
    )
    parser.add_argument(
        "--llm-prompt",
        dest="llm_prompt",
        help="Custom prompt for image descriptions"
    )
    parser.add_argument(
        "--exiftool-path",
        dest="exiftool_path",
        help="Path to exiftool binary"
    )
    parser.add_argument(
        "--enable-plugins",
        dest="enable_plugins",
        action="store_true",
        help="Enable 3rd-party plugins"
    )
    return parser.parse_args()


def build_headers() -> dict[str, str]:
    """Build HTTP headers with rotating Safari user-agent.

    Returns:
        Dictionary of HTTP headers with user-agent and accept headers.
    """
    user_agent = UserAgent()
    return {
        "User-Agent": str(user_agent.safari),
        "Accept": DEFAULT_ACCEPT,
        "Accept-Language": DEFAULT_ACCEPT_LANGUAGE,
        "Accept-Encoding": DEFAULT_ACCEPT_ENCODING,
        "Connection": DEFAULT_CONNECTION
    }


def fetch_url(url: str, headers: dict[str, str]) -> bytes:
    """Fetch content from URL with specified headers.

    Args:
        url: Target URL to fetch.
        headers: HTTP headers to include in request.

    Returns:
        Raw response content as bytes.

    Raises:
        requests.HTTPError: If HTTP request fails.
    """
    response: requests.Response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.content


def markdownify(content: bytes, **options: Any) -> str:
    """Convert binary content to markdown format.

    Args:
        content: Raw binary content to convert.
        **options: Additional options to pass to MarkItDown constructor.

    Returns:
        Converted markdown text.
    """
    converter = MarkItDown(**options)
    result = converter.convert_stream(BytesIO(content))
    return str(result.text_content)


def extract_converter_options(args: argparse.Namespace) -> dict[str, Any]:
    """Extract MarkItDown options from parsed arguments.

    Args:
        args: Parsed command-line arguments.

    Returns:
        Dictionary of non-None options for MarkItDown, excluding URL.
    """
    return {
        key: value
        for key, value in vars(args).items()
        if key != "url" and value is not None
    }


def main() -> None:
    """Main entry point for fetchd CLI tool."""
    args = parse_args()

    headers = build_headers()
    content = fetch_url(args.url, headers)
    converter_options = extract_converter_options(args)

    markdown_output = markdownify(content, **converter_options)
    print(markdown_output)


if __name__ == "__main__":
    main()
