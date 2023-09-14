import gzip
import sys
from pathlib import Path
from typing import TextIO

from Bio import bgzf


def is_gzip(filepath: Path) -> bool:
    with filepath.open(mode='rb') as fin:
        header = fin.read(2)
    return header[:2] == b"\x1f\x8b"


def bgzf_open(path, mode, encoding='utf-8'):
    return bgzf.open(path, mode)


def open_file(path: Path, mode='r') -> TextIO:
    """
    Get file descriptor from path
    Considers whether the file is/should be gzipped
    """
    if path == '-':
        f = sys.stdin if 'r' in mode else sys.stdout
        if 'b' in mode:
            f = f.buffer
        return f
    else:
        if 'w' in mode:
            path.parent.mkdir(exist_ok=True, parents=True)
            _open = bgzf_open if '.gz' in path.suffixes else open
            return _open(path, mode, encoding='utf-8')
        else:
            if 't' not in mode:
                mode += 't'
            _open = gzip.open if is_gzip(path) else open
            return _open(path, mode, encoding='utf-8')
