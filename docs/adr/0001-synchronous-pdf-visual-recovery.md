---
status: accepted
---

# Use synchronous agent-mediated visual recovery for PDF derivatives

## Context

The previous `my-parse-pdf` workflow stopped with a special exit code and
required a later `responses.json` plus `apply_session_ocr.py` invocation for
in-session vision work. That made a single agent run look like an asynchronous
OCR service, created raw-response lifecycle state, and still missed diagrams on
pages that contained enough embedded text. PDF best practices distinguish
deterministic text/layout extraction from multimodal inspection and preserve
source image evidence when a representation is uncertain.

## Decision

The skill will use a synchronous two-stage workflow: PyMuPDF deterministically
renders and inventories every page, then the active agent directly inspects the
renders and reconciles the Markdown and manifest in the same run. Important
visual regions must retain a source crop as ground truth; Mermaid or other
structured representations are optional, explicitly labeled reconstructions
only when the visible relationships are clear. The workflow has no OCR queue,
special pending exit code, response sidecar, or apply handoff script.

## Considered Options

- **Persisted in-session OCR handoff:** rejected because it adds state and a
  second command without representing the actual agent capability.
- **Implicit local OCR engine:** rejected for this skill because language packs,
  compute cost, and OCR quality would become hidden dependencies; it can be a
  separate explicit decision later.
- **External OCR/model endpoint:** rejected because it introduces data-transfer,
  privacy, credentials, billing, retries, and provenance requirements beyond
  this local derivative workflow.
- **Deterministic extraction only:** rejected because text extraction cannot
  preserve the meaning of diagrams, charts, screenshots, or image-only pages.

## Consequences

The parser has a simpler normal-completion contract and can preserve visual
evidence even on text-rich pages. The active agent must inspect every rendered
page and may need to edit the manifest directly. Visual completeness depends on
the available vision capability, so unreadable regions remain explicit gaps
instead of becoming confident-looking guesses. Existing callers using
`--session-dir` or `apply_session_ocr.py` must rerun from the original PDF.
