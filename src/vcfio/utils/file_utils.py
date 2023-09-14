from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import TextIO

def get_open_method(path: Path, mode, encoding='utf-8'):
    from gzip import open as gzip_open
    try:
        from Bio.bgzf import open as bgzip_open
    except ModuleNotFoundError:
        logging.warning("Biopython module not found - using gzip. It is recommended to pip install biopython.")
        bgzip_open = gzip_open

    if 'b' in mode:
        encoding = None

    if 'r' in mode:
        with path.open(mode='rb') as fin:
            header = fin.read(4)
        if header == b'\x1f\x8b\x08\x08':
            return gzip_open(path, mode, encoding=encoding)
        if header == b'\x1f\x8b\x08\x04':
            try:
                return bgzip_open(path, mode, encoding=encoding)
            except TypeError:
                return bgzip_open(path, mode)
    elif '.gz' in path.suffixes or '.bgz' in path.suffixes:
        try:
            return bgzip_open(path, mode, encoding=encoding)
        except TypeError:
            return bgzip_open(path, mode)

    return open(path, mode, encoding=encoding)



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
        if 't' not in mode:
            mode += 't'
        if 'w' in mode:
            path.parent.mkdir(exist_ok=True, parents=True)
        return get_open_method(path, mode, encoding='utf-8')
