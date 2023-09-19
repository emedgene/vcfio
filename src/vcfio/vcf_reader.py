from __future__ import annotations

import functools
import logging
from pathlib import Path

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import AnyStr
    from typing import Iterator
    from typing import List
    from typing import Union


from vcfio.utils.file_utils import open_file
from vcfio.utils.regex_patterns import ALT_PATTERN
from vcfio.utils.regex_patterns import CONTIG_PATTERN
from vcfio.utils.regex_patterns import FILTER_PATTERN
from vcfio.utils.regex_patterns import FORMAT_PATTERN
from vcfio.utils.regex_patterns import INFO_PATTERN
from vcfio.utils.regex_patterns import META_PATTERN
from vcfio.utils.str_utils import standardize_chromosome
from vcfio.utils.str_utils import to_number
from vcfio.variant.variant import Variant


class VcfReader:
    def __init__(self, input_file: Union[Path, AnyStr]):
        self.input_file = Path(input_file)
        self.contigs = {}
        self.infos = {}
        self.filters = {}
        self.alts = {}
        self.formats = {}
        self.metadata = {}
        self._default_sample_format = ''
        self._file_descriptor = open_file(self.input_file)
        self._raw_variant_iterator = self._file_descriptor
        _ = self.headers

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
        return False

    def close(self):
        self._file_descriptor.close()

    def __iter__(self) -> Iterator[Variant]:
        return self

    def __next__(self) -> Variant:
        """
        Iterate variants and yield Variant instances
        If sample format is not given in the raw line then use the FIRST format in the file
        """
        line = next(self._raw_variant_iterator)
        if not line or line.isspace():
            raise StopIteration

        variant = Variant.from_variant_line(line, self.sample_names, self._default_sample_format)
        self._default_sample_format = self._default_sample_format or variant.sample_format
        return variant

    @property
    @functools.lru_cache(maxsize=None)
    def headers(self) -> List[AnyStr]:
        """
        Read first lines of self._reader until last header (#CHROM  POS ID  REF...)
        Match regex patterns of header types and initialize them to instance attributes
        Return raw header lines
        """
        raw_header_lines = []
        for raw_line in self._file_descriptor:
            line = raw_line.strip()
            self._match_header_pattern(line)
            raw_header_lines.append(line)
            if line[1:].lower().startswith("chrom"):
                return raw_header_lines
        return []

    def _match_header_pattern(self, raw_header_line: AnyStr):
        attribute_patterns = (
            (self.infos, INFO_PATTERN),
            (self.contigs, CONTIG_PATTERN),
            (self.filters, FILTER_PATTERN),
            (self.alts, ALT_PATTERN),
            (self.formats, FORMAT_PATTERN),
            (self.metadata, META_PATTERN)
        )
        for attribute, pattern in attribute_patterns:
            match = pattern.match(raw_header_line)
            if match:
                attribute[match.group('id')] = to_number(match.groupdict(), default=match.groupdict())

    @property
    def variant_fields(self) -> List[AnyStr]:
        # CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	proband
        return self.headers[-1].strip('#').strip('\n').split()

    @property
    def sample_names(self) -> List[AnyStr]:
        # CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	---> [proband, mother, father] <---
        return self.variant_fields[9:]

    def fetch(self, chromosome: AnyStr, start: int = 1, end: int = None) -> Iterator[Variant]:
        """
        ** This function fetches using a 1-based system **
        If there is a tabix file - fetch using pysam
        Else - open another reader of the same path and iterate the selected variant
        """
        try:
            yield from self._fetch_by_index(chromosome, end, start)
        except OSError:  # .tbi file not found
            logging.warning(
                f"Tab-index file not found ({self.input_file.as_posix() + '.tbi'}) - using regular iteration.")
            yield from self._fetch_by_iteration(chromosome, end, start)
        except ModuleNotFoundError:  # if pysam is not installed
            logging.warning("Pysam module not found - using regular iteration.")
            yield from self._fetch_by_iteration(chromosome, end, start)

    def _fetch_by_index(self, chromosome, end, start):
        from pysam import TabixFile
        with TabixFile(filename=self.input_file.as_posix(), encoding='utf-8') as tabix_file:
            for line in tabix_file.fetch(standardize_chromosome(chromosome), start - 1, end - 1 if end else None):
                yield Variant.from_variant_line(
                    line,
                    sample_names=self.sample_names,
                    default_sample_format=self._default_sample_format
                )

    def _fetch_by_iteration(self, chromosome, end, start):
        with VcfReader(self.input_file) as sub_reader:
            for variant in sub_reader:
                if variant.chromosome == chromosome and variant.position in range(start, end):
                    yield variant
                if variant.position == end:
                    break

    def __repr__(self):
        return f"VcfReader('{self.input_file.absolute()}')"
