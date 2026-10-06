import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'skills/local-dot-handoff/scripts/handoff_text.py'
spec = importlib.util.spec_from_file_location('handoff', SCRIPT)
h = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)

class TransferTest(unittest.TestCase):
    def parts(self, raw):
        self.root = Path(self.tmp.name)
        src = self.root / 'source.md'
        src.write_bytes(raw)
        h.split(src, self.root/'parts', 'synthetic-r1', 3)
        return [json.loads(p.read_text()) for p in sorted((self.root/'parts').glob('*.json'))]
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
    def tearDown(self):
        self.tmp.cleanup()
    def test_roundtrip(self):
        raw = '\ufeff甲\r\n😀e\u0301&lt;tag&gt;\n尾\t '.encode()
        p = self.parts(raw)
        self.assertEqual(h.assemble(list(reversed(p))), raw)
    def test_empty(self):
        self.assertEqual(h.assemble(self.parts(b'')), b'')
    def test_missing(self):
        p = self.parts('abcdefg'.encode())
        with self.assertRaises(ValueError): h.assemble(p[:-1])
    def test_duplicate(self):
        p = self.parts(b'abcdefg')
        with self.assertRaises(ValueError): h.assemble(p+[p[-1]])
    def test_changed_content(self):
        p = self.parts(b'abcdefg'); p[0]['text'] = 'xyz'
        with self.assertRaises(ValueError): h.assemble(p)
    def test_mixed_snapshot(self):
        p = self.parts(b'abcdefg'); p[-1]['handoff'] = 'other'
        with self.assertRaises(ValueError): h.assemble(p)
    def test_overlap(self):
        p = self.parts(b'abcdefg'); p[1]['character_start'] -= 1
        with self.assertRaises(ValueError): h.assemble(p)
    def test_unsafe_filename_not_used(self):
        p = self.parts(b'abcdefg')
        for x in p: x['file'] = '../../unsafe'
        paths = []
        for i, x in enumerate(p):
            q = self.root/f'{i}.json'; q.write_text(json.dumps(x)); paths.append(q)
        h.join(self.root/'safe', paths)
        self.assertEqual((self.root/'safe').read_bytes(), b'abcdefg')
        with self.assertRaises(FileExistsError): h.join(self.root/'safe', paths)
    def test_invalid_utf8(self):
        src = Path(self.tmp.name)/'invalid'; src.write_bytes(b'\xff')
        with self.assertRaises(UnicodeDecodeError): h.split(src, src.parent/'parts', 'x', 3)

if __name__ == '__main__': unittest.main()
