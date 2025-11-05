[![Test][badge-test]][workflow-test]

## fetchd

Basically [microsoft/markitdown][markitdown-repo] with `curl` 

> suitable for LLM use in technical domains,  
> because it fetches *everything*, not just summaries.




## Usage

```bash
fetchd https://example.com
fetchd document.pdf
fetchd https://example.com --llm-model gpt-4o
```

## Credits

Built on [microsoft/markitdown][markitdown-repo].

## License

MIT

[badge-test]: https://github.com/nicholaswmin/applepie/actions/workflows/test.yml/badge.svg
[workflow-test]: https://github.com/nicholaswmin/applepie/actions/workflows/test.yml
[markitdown-repo]: https://github.com/microsoft/markitdown
