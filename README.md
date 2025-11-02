## applepie

Build standalone macOS binaries from Python CLI tools.
Uses GitHub Actions and PyInstaller.

[![Build macOS Binary][badge-build-macos]][workflow-build-macos]
[![Build fetchd Binary][badge-build-fetchd]][workflow-build-fetchd]
[![Test][badge-test]][workflow-test]

## Tools

**markitdown**

Converts files to Markdown:
PDFs, DOCX, XLSX, PPTX, images, web pages.

**fetchd**

Fetches URLs and converts to Markdown.
Supports LLM-powered image descriptions.

## Quick Start

Download binaries from GitHub Actions artifacts:

```bash
gh run download <run-id> --repo nicholaswmin/applepie
```

Run without Python installed:

```bash
# Convert PDF
./markitdown-macos-arm64/markitdown document.pdf

# Fetch URL
./fetchd-macos-arm64/fetchd https://example.com
```

## fetchd Usage

Basic:

```bash
fetchd https://example.com/article
```

With LLM image descriptions:

```bash
fetchd https://example.com --llm-model gpt-4o
```

**Options:**

- `--llm-model` - Model for image descriptions
- `--llm-prompt` - Custom image prompt
- `--exiftool-path` - Path to exiftool
- `--enable-plugins` - Enable 3rd-party plugins

## Build Process

Workflow runs on macOS 15 ARM64.
Installs Python 3.12 and dependencies.
Bundles with PyInstaller into single executable.
Uploads artifact (~93MB).

## Local Build

**Requirements:**

- Python 3.10+
- macOS

**Setup:**

```bash
git clone https://github.com/nicholaswmin/applepie.git
cd applepie
pip install -r requirements.txt
```

**Build markitdown:**

```bash
pyinstaller --onefile --name markitdown \
  --collect-all markitdown --collect-all magika \
  run_markitdown.py
```

**Build fetchd:**

```bash
pyinstaller --onefile --name fetchd \
  --collect-all markitdown --collect-all magika \
  fetchd.py
```

**Test:**

```bash
python -m unittest discover -v
```

## Development

Run tests:

```bash
python -m unittest test_fetchd -v
```

**Structure:**

```
.
├── .github/workflows/
│   ├── build-macos.yml
│   ├── build-fetchd.yml
│   └── test.yml
├── fetchd.py
├── run_markitdown.py
├── test_fetchd.py
└── requirements.txt
```

## Credits

Built on [microsoft/markitdown][markitdown-repo].

## License

MIT

[badge-build-macos]: https://github.com/nicholaswmin/applepie/actions/workflows/build-macos.yml/badge.svg
[badge-build-fetchd]: https://github.com/nicholaswmin/applepie/actions/workflows/build-fetchd.yml/badge.svg
[badge-test]: https://github.com/nicholaswmin/applepie/actions/workflows/test.yml/badge.svg
[workflow-build-macos]: https://github.com/nicholaswmin/applepie/actions/workflows/build-macos.yml
[workflow-build-fetchd]: https://github.com/nicholaswmin/applepie/actions/workflows/build-fetchd.yml
[workflow-test]: https://github.com/nicholaswmin/applepie/actions/workflows/test.yml
[markitdown-repo]: https://github.com/microsoft/markitdown
