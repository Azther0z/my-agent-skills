---
name: my-parse-pdf
description: "Use whenever a user asks to ingest, extract, OCR, transcribe, make searchable, or create a Markdown companion from a PDF, including scanned handouts, study slides, assignments, diagrams, charts, screenshots, or bilingual English/Thai material. Preserve the original, create a grounded page-oriented Markdown derivative and manifest, render and inspect every page, and recover missing visual meaning with source crops and clearly labeled Mermaid reconstructions when safe. Do not use a waiting OCR handoff, upload source pages, or invent unreadable content."
sources:
  - https://skills.sh/anthropics/skills/pdf
  - https://ai.google.dev/gemini-api/docs/document-processing
  - https://cloud.google.com/document-ai/docs/enterprise-document-ocr
  - https://pymupdf.readthedocs.io/en/latest/recipes-images.html
  - https://pymupdf.readthedocs.io/en/latest/recipes-text.html
  - https://pymupdf.readthedocs.io/en/latest/pymupdf4llm/index.html
  - https://docling-project.github.io/docling/_generated/examples/export_figures/
  - https://ocrmypdf.readthedocs.io/en/latest/introduction.html
compatibility: "Requires Python 3.10+ and either uv or python3-venv; scripts/run_tool.py installs pinned PyMuPDF in a user-owned cache. No system OCR binary or external model endpoint is required."
---

# PDF Parser

Create an inspectable, source-faithful PDF derivative with a visual evidence layer. The parser is the deterministic preparation step. The active agent owns the visual review and writes its applied transcription or visual recovery into the Markdown in the same run. Do not turn that work into a queue, a polling protocol, or a fake asynchronous OCR job.

## Write boundary

Use this skill for an explicit artifact-producing request such as:

- "parse this PDF"
- "create a Markdown companion"
- "make this scanned PDF searchable"
- "transcribe these slides"
- "preserve the diagrams in a text derivative"

For a question about a PDF, answer from available evidence without creating a derivative. Never overwrite or rewrite the original PDF. Choose a private source/derivative directory; do not put source PDFs, manifests, page renders, crops, or agent reconstructions in a published web export.

## Output contract

For an input named `lecture.pdf`, create these files in the private derivative directory:

- `lecture.pdf.md` — page-oriented Markdown containing native text, direct visual transcriptions, source-image links where visual evidence matters, and explicitly labeled reconstructions or gaps.
- `lecture.pdf.manifest.json` — schema version 2, source hash and size, page count, languages, renderer settings, page geometry, text/image/drawing inventory, generated asset paths, and agent-review status.
- `assets/pages/page-0001.png` — a private render for every source page.
- `assets/embedded/page-0001-image-01.png` (when safely extractable) — private copies of embedded image blocks with their page bounding boxes.
- `assets/crops/...png` — targeted source crops created for important visual regions; keep them when they support a transcription or reconstruction.

The source PDF remains authoritative. The Markdown is a grounded derivative, not a summary. Keep page numbers and visible line/order information. Preserve English and Thai (or the user-requested languages). Use `[unreadable]` or an explicit gap such as `[diagram relationship unclear]` instead of guessing.

Distinguish these in the Markdown and manifest:

- **Source text** — text extracted from the PDF or directly transcribed from a visible page.
- **Source image/crop** — an unchanged render or crop of source evidence.
- **Reconstruction** — Mermaid, a table, or factual prose derived from visible source content; never present it as if it were the original artwork.
- **Gap** — content that could not be read or safely represented.

Do not retain a full model response or create an OCR response sidecar. Retain only the applied content, its source page/asset reference, and the concise method/status metadata needed to audit the derivative.

## Workflow

1. Read the repository's agent contract and choose private source and output directories. Do not assume a particular wiki or editor.
2. Run the deterministic preparation step. It renders **every** page, records text block/image/drawing geometry, safely extracts embedded image blocks, and creates the Markdown draft and manifest:

   ```sh
   python3 scripts/run_tool.py parse_pdf.py \
     --input /private/course/lecture.pdf \
     --output-dir /private/course/derived \
     --languages en,th \
     --dpi 200 \
     --force
   ```

   The command exits `0` after preparation. A visual review requirement is manifest metadata, not a special exit code and not a request to run another script later.
3. Open and inspect every `assets/pages/page-*.png` with the current agent's vision-capable image tool. Do not inspect only pages with little extracted text: diagrams and screenshots often share a page with perfectly usable text. If no vision tool is available, keep the render and record an explicit gap; do not fabricate a transcription.
4. For pages with embedded text, use the deterministic text as the baseline. Correct only obvious reading-order/interleaving errors using block geometry; do not editorially rewrite wording. For scanned or image-only pages, transcribe visible text directly in page order. Mark uncertain characters rather than silently repairing them.
5. For every visual region that carries meaning not present in the text:

   - identify the region in PDF points from the page/manifest geometry;
   - create a reproducible source crop with `python3 scripts/run_tool.py crop_pdf.py`;
   - link the crop with a caption such as `Source crop — page 3, diagram`; and
   - choose the safest representation below.

   ```sh
   python3 scripts/run_tool.py crop_pdf.py \
     --input /private/course/lecture.pdf \
     --page 3 \
     --rect 72,180,540,610 \
     --dpi 300 \
     --output /private/course/derived/assets/crops/page-0003-diagram-01.png
   ```

   Keep the crop as ground truth even when a reconstruction is added.
6. Recover visual meaning conservatively:

   - **Flowcharts, pipelines, sequences, trees, and graphs:** add Mermaid only when the nodes, labels, direction, and relationships are visibly clear. Label it `Reconstruction (not source)` and keep the source crop beside it.
   - **Tables:** use a Markdown table only when cell boundaries and values are clear; otherwise keep the crop and describe the legible structure.
   - **Equations or code in an image:** transcribe only what is legible; use a crop for anything whose notation cannot be represented reliably.
   - **Photos, screenshots, or decorative art:** retain a crop and a short, factual caption only when it helps identify the source content. Do not infer hidden context.
   - **Unreadable or ambiguous regions:** keep the source evidence and write a precise gap marker. A complete-looking guess is a failed parse.

7. Reconcile the Markdown and manifest directly. Each page should have an `agent_review` object like this; do not create a response file or invoke an apply/handoff script:

   ```json
   {
     "status": "complete_with_gaps",
     "method": "direct-agent-vision",
     "artifacts": ["assets/crops/page-0003-diagram-01.png"],
     "gaps": ["rightmost arrow label is unreadable"]
   }
   ```

   Use `complete` when no meaningful content is missing and `complete_with_gaps` when the remaining limitation is explicitly recorded.
8. Verify before reporting completion:

   - the original PDF hash and byte size are unchanged;
   - every page has a deterministic status and an agent-review status;
   - every page render referenced by the manifest exists;
   - every linked crop/reconstruction asset exists;
   - source text, direct transcription, reconstruction, and gaps are visibly distinguishable;
   - no unexplained blank page, `OCR_PENDING` marker, response sidecar, or unreported visual region remains.

## Manifest and status rules

The parser emits schema version 2. Its page status describes deterministic preparation (`embedded_text` or `visual_only`); `agent_review.status` describes the active agent's visual pass (`required`, `complete`, or `complete_with_gaps`). The parser may return normal completion while reviews are required because it never waits for the agent or owns the agent's edits.

Record asset paths relative to the manifest/Markdown directory. Record page coordinates in PDF points and preserve the original page number (1-based). Treat image and drawing bounding boxes as evidence hints, not as proof that a complete figure has been segmented: a diagram may be made from many vector drawings or mixed text and images.

## What this release does not do

- It does not run Tesseract, OCRmyPDF, a local neural OCR model, or an external OCR/model endpoint implicitly.
- It does not upload PDFs or page images.
- It does not create a persistent in-session OCR response queue or raw model response sidecars.
- It does not rewrite the source PDF, publish private assets, or turn parsing into a Git commit or push.
- It does not claim that a crop or Mermaid diagram is source-native content.

If a future release adds local or external OCR, it needs a separate explicit decision covering dependencies, language packs, data transfer, privacy, quality/uncertainty, retries, and manifest provenance.

## Failure handling

- Missing PyMuPDF: use `python3 scripts/run_tool.py` to install it in the user cache; never install into the repository or system Python without an explicit environment decision.
- Encrypted, malformed, or unreadable PDF: preserve the original, write the error in the manifest, and stop rather than emitting an empty success.
- Missing vision capability: preserve the generated page render and record a gap; do not guess.
- Existing derivatives: require `--force` for a deterministic rerun. The old `--session-dir` and `apply_session_ocr.py` handoff are intentionally removed; rerun the source through this workflow instead of trying to migrate its response sidecars.

## Bundled scripts

- `scripts/run_tool.py` — user-space dependency bootstrap and entrypoint for both PDF tools.
- `scripts/parse_pdf.py` — text extraction, all-page rendering, and visual inventory/manifest generation.
- `scripts/crop_pdf.py` — reproducible page-region rendering from PDF points.
