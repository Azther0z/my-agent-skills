---
name: learning-artifact-creation
description: "Use when a user asks to turn study sources into an exam-ready core pack, recall quiz bank, HTML slides, visual explanation, interactive practice, or a C4-style top-down concept map. Create grounded artifacts only on explicit create/update/publish intent, keep private source evidence separate from the approved web export, and prefer the bundled standalone HTML/SVG/JS map builder for zoomable learning views."
sources:
  - https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages
  - https://pymupdf.readthedocs.io/en/latest/recipes-text.html
compatibility: "Uses Python 3.10+ standard-library scripts for map generation and allowlisted publishing; generated pages require only a modern browser."
---

# Learning Artifact Creation

Turn grounded study material into small, inspectable learning surfaces. The
goal is not to produce a transcript or a pretty summary; it is to make the
material easier to retrieve, recall, practice, and navigate under exam time
pressure.

## Explicit Artifact Boundary

Write only when the user explicitly asks to create, update, or publish an
artifact. A question, explanation, search result, or preview is read-only.
Treat these as separate intents:

- `create` drafts or generates files in the private working/source area.
- `update` changes an existing artifact while preserving its provenance.
- `publish` copies an explicit allowlist into the approved web root.

Never infer publication from creation. Do not commit or push as part of this
skill. Do not copy raw PDFs, parser manifests, raw model responses, private
notes, credentials, or unrelated repository files into the web root.

## Artifact Set

For an approved study topic, propose or create only the outputs requested by
the user. The standard thin-slice set is:

- `core-pack.md` — concise concepts, relationships, worked examples, and
  source page references.
- `recall-quiz.md` — questions first, answers and explanations separated so
  the learner can self-test.
- `practice.html` — a self-contained interactive practice surface with no
  network or CDN dependency.
- `map.html` — a generated, zoomable learning map.
- `map.data.json` — private declarative source data for regenerating the map;
  publish it only if the user explicitly approves it.

Keep claims grounded in the parsed Markdown companions and source-page
references. Mark gaps, OCR uncertainty, conflicting sources, and unsupported
answers instead of smoothing them over. A derivative may reorganize or
explain source material, but it must not silently become a substitute for the
original evidence.

## Workflow

1. Read the project contract and route to the source Markdown and manifests.
   Do not assume the OpenKnowledge UI is the user's preferred editing surface;
   follow the repository's own tool contract when one exists.
2. Define the artifact set, private output directory, and approved publish
   directory before writing. If any is unclear, ask rather than selecting a
   broad repository path.
3. Build the core pack and recall questions from stable source text. Include
   page-level references in the form `[Source p. 4]` or the project's
   established equivalent.
4. Add an interactive practice surface only when its questions and answer
   key are grounded. Keep the HTML self-contained so it works offline after
   the file is opened.
5. Create the map data and generate the standalone map with the bundled
   template:

   ```sh
   python3 scripts/build_map.py \
     --data /private/study/map.data.json \
     --output /private/study/map.html \
     --force
   ```

   The default template is `assets/study-map.html`. It supports level tabs,
   node selection, drill-down links, pan, zoom, keyboard-friendly controls,
   and responsive layout without external assets.
6. Review all outputs for unsupported claims, broken local references,
   missing answer keys, inaccessible controls, and accidental private files.
7. Publish only the explicitly approved paths:

   ```sh
   python3 scripts/publish_artifacts.py \
     --source /private/study \
     --target /srv/workspace/my-llmbrain/artifact/midterm \
     --files core-pack.md recall-quiz.md practice.html map.html \
     --publish
   ```

   The publisher rejects PDFs, JSON manifests, response sidecars, hidden
   files, symlinks escaping the source root, and unlisted files. It never
   deletes older published files automatically.

## Map Data Contract

Use JSON as the portable declarative format. The minimum shape is:

```json
{
  "title": "Midterm systems map",
  "subtitle": "Context to detail",
  "levels": [
    {"id": "context", "label": "Context"},
    {"id": "module", "label": "Modules"},
    {"id": "detail", "label": "Details"}
  ],
  "nodes": [
    {
      "id": "topic-a",
      "label": "Topic A",
      "level": "context",
      "summary": "One-sentence grounded summary",
      "detail": "Longer explanation with source references",
      "x": 260,
      "y": 260,
      "children": ["topic-a-detail"],
      "sources": ["source.pdf.md#page-4"]
    }
  ],
  "edges": [{"from": "topic-a", "to": "topic-b", "label": "depends on"}]
}
```

Use stable IDs, keep edges directional only when the source supports a
direction, and use `children` for top-down drill-down. Coordinates are part of
the declarative data so layout changes remain reviewable. The generated HTML
inlines the data and does not need to expose the JSON file.

## Privacy And Publishing

The approved web root is an allowlisted derivative boundary. Store originals,
parser Markdown companions, manifests, and full model responses in private
source directories. A page that cites private source material may be
published only after the user explicitly approves its content and the
citations do not expose private paths or data. Use the self-hosted Access
route for the approved web root; hosting itself is infrastructure work, not a
reason to broaden the file allowlist.

## Quality Bar

- Core concepts are traceable to source pages.
- Quiz answers are hidden or separated until recall is attempted.
- Interactive controls work with keyboard and touch-sized targets.
- The map has a useful overview, readable labels, and a clear drill-down path.
- HTML, SVG, CSS, and JavaScript work without a CDN or backend.
- The publish command's file list is explicit and contains no private source.
- Remaining uncertainty is visible to the learner rather than disguised as
  confidence.
