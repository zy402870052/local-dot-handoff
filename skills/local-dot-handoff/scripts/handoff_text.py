#!/usr/bin/env python3
"""Split and losslessly reassemble UTF-8 text. No network access."""
import argparse
import hashlib
import json
from pathlib import Path

FIELDS = ('handoff', 'file', 'parts', 'total_characters', 'total_utf8_bytes', 'whole_file_sha256')

def sha(data):
    return hashlib.sha256(data).hexdigest()

def split(source, destination, handoff, chunk_size):
    if chunk_size < 1:
        raise ValueError('chunk-size must be positive')
    raw = Path(source).read_bytes()
    text = raw.decode('utf-8', errors='strict')
    count = max(1, (len(text) + chunk_size - 1) // chunk_size)
    out = Path(destination)
    out.mkdir(parents=True, exist_ok=True)
    paths = [out / f'part-{i:05d}.json' for i in range(1, count + 1)]
    if any(p.exists() for p in paths):
        raise ValueError('refusing to overwrite existing part files')
    for i, path in enumerate(paths):
        start = i * chunk_size
        end = min(len(text), start + chunk_size)
        value = dict(handoff=handoff, file=Path(source).name, part=i+1, parts=count,
                     character_start=start, character_end=end, total_characters=len(text),
                     total_utf8_bytes=len(raw), whole_file_sha256=sha(raw), text=text[start:end])
        with path.open('x', encoding='utf-8', newline='\n') as stream:
            json.dump(value, stream, ensure_ascii=False)
    return dict(parts=count, total_characters=len(text), total_utf8_bytes=len(raw), whole_file_sha256=sha(raw))

def assemble(parts):
    if not parts:
        raise ValueError('no parts supplied')
    for p in parts:
        for key in (*FIELDS, 'part', 'character_start', 'character_end', 'text'):
            if key not in p:
                raise ValueError(f'missing field: {key}')
        for key in ('part', 'parts', 'character_start', 'character_end', 'total_characters', 'total_utf8_bytes'):
            if type(p[key]) is not int:
                raise ValueError(f'{key} must be an integer')
        if not isinstance(p['text'], str):
            raise ValueError('text must be a string')
        if any(p[k] != parts[0][k] for k in FIELDS):
            raise ValueError('mixed file identities or snapshots')
    ordered = sorted(parts, key=lambda p: p['part'])
    meta = ordered[0]
    if meta['parts'] < 1 or len(ordered) != meta['parts'] or any(p['part'] != i for i, p in enumerate(ordered, 1)):
        raise ValueError('missing or duplicate part numbers')
    offset = 0
    for p in ordered:
        if p['character_start'] != offset or p['character_end'] != offset + len(p['text']):
            raise ValueError('gap, overlap, or incorrect character range')
        offset = p['character_end']
    content = ''.join(p['text'] for p in ordered)
    raw = content.encode('utf-8', errors='strict')
    if offset != meta['total_characters'] or len(raw) != meta['total_utf8_bytes'] or sha(raw) != meta['whole_file_sha256']:
        raise ValueError('whole-file length, bytes, or SHA-256 mismatch')
    return raw

def join(destination, paths):
    parts = [json.loads(Path(p).read_text(encoding='utf-8')) for p in paths]
    raw = assemble(parts)
    out = Path(destination)
    # Explicit destination; do not trust file names in untrusted transport metadata.
    with out.open('xb') as stream:
        stream.write(raw)
    if out.read_bytes() != raw:
        raise ValueError('saved output readback mismatch')
    return dict(total_characters=len(raw.decode('utf-8')), total_utf8_bytes=len(raw), whole_file_sha256=sha(raw))

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    s = sub.add_parser('split')
    s.add_argument('source'); s.add_argument('destination')
    s.add_argument('--handoff', required=True)
    s.add_argument('--chunk-size', type=int, default=8000)
    j = sub.add_parser('join')
    j.add_argument('destination'); j.add_argument('parts', nargs='+')
    args = parser.parse_args()
    try:
        result = split(args.source, args.destination, args.handoff, args.chunk_size) if args.command == 'split' else join(args.destination, args.parts)
    except (ValueError, OSError, UnicodeError) as exc:
        parser.exit(2, f'error: {exc}\n')
    print(json.dumps(result, ensure_ascii=False))

if __name__ == '__main__':
    main()
