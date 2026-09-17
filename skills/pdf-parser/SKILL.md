---
name: pdf-parser
description: "Use when a user asks to ingest, extract, OCR, transcribe, or make a PDF searchable, especially for study slides, assignments, scanned handouts, or bilingual English/Thai material. Preserve the original PDF, create a grounded Markdown companion and machine-readable manifest, and use an explicit in-session vision handoff for pages without usable embedded text. Do not upload source pages or invent OCR results."
sources:
  - https://pymupdf.readthedocs.io/en/latest/tutorial.html
  - https://pymupdf.readthedocs.io/en/latest/recipes-images.html
  - https://pymupdf.readthedocs.io/en/latest/recipes-text.html
compatibility: "Requires Python 3.10+ and either uv or python3-venv; the first-use wrapper installs PyMuPDF in a user-owned cache. No system OCR binary is required."
---

# PDF Parser

Create inspectable PDF derivatives without changing the source file. This skill
is intentionally text-first: PyMuPDF extracts embedded text and renders page
images for review, but this release does not run a local OCR engine or call an
external model endpoint.

## Write Boundary

Use this skill only for an explicit artifact-producing request such as:

- "parse this PDF"
- "create the Markdown companion"
- "update the OCR derivative"
- "finish the pending page transcriptions"

Do not create files for a question about a PDF, a one-off explanation, or a
routine preview. Never overwrite the original PDF. Keep source PDFs,
manifests, pending images, and OCR response sidecars in a private source or
working directory, not in a web export directory.

## Output Contract

For an input named `lecture.pdf`, produce these companions beside the chosen
private output directory:

- `lecture.pdf.md` — faithful page-oriented Markdown with embedded text and
  explicit markers for pages awaiting session vision.
- `lecture.pdf.manifest.json` — schema version, source hash, page count,
  languages, renderer details, page status, image paths, and errors.
- `ocr-responses/page-0002.json` — private sidecar containing the full raw
  in-session model response and the applied transcription for each OCR page.

The original `lecture.pdf` remains authoritative. The Markdown companion is a
derivative for search and grounding, not a replacement or a summary. Use
English and Thai as the default requested languages; retain page numbers and
line breaks where the model can see them. Mark unreadable text as
`[unreadable]` rather than guessing.

## Workflow

1. Read the repository's agent contract and identify the private source and
   derivative directories. Do not assume a particular wiki or editor tool.
2. Run the bundled wrapper. It creates a user-space virtual environment on
   first use and caches the pinned `PyMuPDF` dependency outside Git:

   ```sh
   scripts/run_parser.sh \
     --input /private/course/lecture.pdf \
     --output-dir /private/course/derived \
     --session-dir /private/course/ocr-session \
     --languages en,th \
     --force
   ```

3. If the command exits with status `2`, read the manifest and open each
   `session_vision_pending` image with the current agent's vision-capable
   image tool. Work one page at a time. Return a faithful transcription only;
   do not summarize, translate, repair uncertain characters, or infer text
   hidden by graphics.
4. Write a private responses file with this shape, preserving the complete
   model response in `raw_response`:

   ```json
   {
     "pages": [
       {
         "page": 2,
         "text": "Visible transcription here.",
         "raw_response": "The exact response returned by the model."
       }
     ]
   }
   ```

5. Apply the handoff. The script writes private per-page response sidecars,
   updates the Markdown page block, and reconciles the manifest:

   ```sh
   scripts/apply_session_ocr.py \
     --markdown /private/course/derived/lecture.pdf.md \
     --manifest /private/course/derived/lecture.pdf.manifest.json \
     --responses /private/course/ocr-session/responses.json \
     --response-dir /private/course/ocr-responses
   ```

   It exits `2` when pages remain pending and `0` when all pages are complete.
6. Verify the manifest has no pending pages, every page has a status, the
   original hash is unchanged, and the Markdown contains no unexplained blank
   page. Report any remaining `session_vision_pending` page explicitly.

## What This Release Does Not Do

- It does not upload PDFs or page images to an external endpoint.
- It does not run Tesseract, OCRmyPDF, a local neural OCR model, or a hidden
  fallback that consumes substantial host resources.
- It does not publish source PDFs, manifests, or raw response sidecars.
- It does not turn a parser request into a Git commit or push.

If external OCR is later added, it needs a separate explicit opt-in, provider
and model configuration, data-transfer notice, retry policy, and manifest
backend field. Do not add that behavior implicitly to this skill.

## Failure Handling

- Missing PyMuPDF: use `scripts/run_parser.sh`; never install into the
  repository or system Python without an explicit environment decision.
- Encrypted, malformed, or unreadable PDF: preserve the original, write an
  error in the manifest, and stop rather than emitting an empty successful
  derivative.
- Missing vision capability: keep the rendered page and pending status; do
  not replace it with guessed text.
- Existing derivatives: require `--force` for a full parser rerun. The apply
  script only updates pages supplied in the response file.

## Bundled Scripts

- `scripts/run_parser.sh` — user-space dependency bootstrap and parser entry.
- `scripts/parse_pdf.py` — embedded text extraction, page rendering, and
  manifest generation.
- `scripts/apply_session_ocr.py` — explicit application of session vision
  responses and private provenance sidecars.
