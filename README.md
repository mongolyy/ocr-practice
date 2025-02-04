# ocr-practice

## Requirements

- uv
- poppler-windows
  - https://github.com/oschwartz10612/poppler-windows

## How to run

```sh
uv run bedrock/ocr_plain.py
uv run bedrock/ocr_pdf2img.py

uv run --env-file=openai/.env openai/ocr.py
```
