---
name: local-dot-handoff
description: Coordinate complete, verifiable handoffs between local project executors and a designated dot reviewer. Use for project recovery, long-file transfers, review receipts, version adoption, or unreliable cross-thread communication.
---

# Local project ↔ dot handoff

## Establish the current contract

Identify the authorized project, local executor, designated reviewer, source version, allowed edits, frozen scope, and storage destination. Reuse verified existing project entrances; do not create replacement projects or rename navigation merely because messaging fails. Keep project-specific reading targets, work hours, genres, and approval gates in the project contract, not universal defaults.

## Keep four statuses separate

1. **Sent:** the transport accepted the message or file.
2. **Received and verified:** the receiver has the actual complete bytes, has read them back, and has checked the declared identity and completeness.
3. **Reviewed:** the reviewer actually performed the stated content review on that version and reports its scope, findings, and remaining issues.
4. **Adopted:** the authorized owner approved using that version and any authorized writeback was verified.

A checksum proves byte equality, not reading or quality. A prior review does not approve a changed version. A local report of reading is evidence about that local reader, not a substitute for the reviewer's reading.

## Transfer once, then reference precisely

Prefer an accessible complete artifact plus a concise manifest. Verify that the receiving environment can open it; a path on another machine is not a delivered file. Use a shared Page for stable operating rules and reusable instructions when requested. Subsequent messages should carry project, version, changed scope, artifact reference, and requested decision rather than repeat the full rules.

When the supported route only accepts message text, use lossless JSON slices of the original decoded text. Read [the transfer contract](references/transfer-contract.md) before chunking or reassembly. Use `scripts/handoff_text.py` to split and verify UTF-8 text. Wait for all declared pieces and accompanying materials before whole-package receipt. Request only missing or corrupted pieces. Never normalize punctuation, line endings, HTML entities, or whitespace to make a hash match.

## Recover communication without inventing capabilities

Test supported read and send routes separately, record the exact observed result, and distinguish a missing reply from a failed tool call. Do not present a temporary routing failure as a permanent product restriction. If local→reviewer delivery and local reading of reviewer output are verified while reverse sending fails, use this pullback workflow:

- Local executor sends the complete submission to the fixed reviewer entrance.
- Reviewer leaves the version-specific receipt and review at that entrance.
- Local executor reads it directly and confirms which complete result it received.

Do not fabricate receipt, bypass denied access, repeatedly retry an uncertain send, or introduce an unapproved alternative recipient. If neither route works, report the exact blocked operation and retain the package in its authorized destination.

## Review and close the loop

Use the project’s domain-review skill for quality assessment. Record actual read scope separately from mechanical comparisons. Return per-file receipt, per-issue decisions, exact change scope, unresolved choices, and remaining freezes. Use [receipt templates](references/receipt-templates.md) as needed. The executor applies only authorized decisions, reads affected continuity, and returns a versioned change list for re-review.

Do not overwrite a canonical manuscript, publish, unfreeze future work, or discard historical evidence merely because a candidate passed a narrow review. Follow the owner’s current storage and adoption rule. Keep superseded reports intact when their byte identity matters; correct current status with a dated addendum.

## Public sharing

Publish only explicitly authorized, redacted workflow material. Exclude manuscript content, real conversation IDs, email addresses, private Pages, private document links, credentials, and private operating notes. Use synthetic examples. A user's request to share the method does not authorize exposing the underlying project archive.
