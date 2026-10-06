# Lossless UTF-8 text transfer

Use an immutable source snapshot. Decode UTF-8 strictly; retain a BOM if present as U+FEFF. Do not translate or HTML-unescape content. Count Unicode code points, not UTF-16 code units, grapheme clusters, or Chinese characters. Encode the decoded text back to UTF-8 for byte count and SHA-256. Preserve CRLF versus LF. For binary files, use a supported binary attachment route rather than this text format.

Choose chunk size from the actual serialized message length and byte budget of the transport. JSON escaping and the envelope add overhead; the default 8000 source characters is not guaranteed to fit every tool.

Each JSON part contains `handoff`, `file`, `part`, `parts`, `character_start`, `character_end`, `total_characters`, `total_utf8_bytes`, `whole_file_sha256`, and `text`. Part numbers are one-based; character ranges are zero-based half-open. Transport JSON escaping is decoded exactly once. Literal text such as `&lt;` remains literal.

Before writing the output, require identical identity metadata across parts; no duplicate or missing part; continuous ranges starting at zero; per-part text lengths matching ranges; final length, bytes, and hash matching the manifest. Reject a changed snapshot even if each individual piece looks plausible. Do not overwrite an existing destination by default. Read the saved output back and verify again.

The companion-material manifest is separate from the body-file chunk count. A four-part body plus three appendices is not complete until both declared groups are received. A tool's truncated text output is not recovered by assuming its hidden remainder is present. A previously verified identical snapshot may support continued review, but label the provenance; do not claim that new transmission was reassembled when it was not.

CLI:

```
python scripts/handoff_text.py split SOURCE.md PARTS_DIR --handoff sample-r1 --chunk-size 8000
python scripts/handoff_text.py join OUTPUT.md PARTS_DIR/*.json
```

Only pass part JSON files to `join`. The tool is transport validation, not a content reviewer or delivery service.
