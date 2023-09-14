from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from vcfio.utils.file_utils import open_file
from vcfio.variant.variant import Variant

if TYPE_CHECKING:
    from typing import Union
    from typing import AnyStr
    from typing import Iterable

REQUIRED_HEADERS = (
    '##fileformat=VCFv4.2',
    '#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	{sample_names}'
)


class VcfWriter:
    def __init__(self, output_file: Union[AnyStr, Path]):
        """
        output_file -- /path/to/output
        headers -- array of vcf headers - should comply with VCF specifications
        variants -- array of Variants
        """
        self.output_file = Path(output_file)

        self._file_descriptor = open_file(self.output_file, mode='w')
        self._write_last_header = False

    def write(self, headers: Iterable[AnyStr] = (), variants: Iterable[Variant] = ()):
        """
        Write the headers and variants to self.output_path
        If headers is empty - will write REQUIRED HEADERS (using sample names from `variants` parameter
        """
        self.write_headers(headers)
        self.write_variants(variants)

    def write_headers(self, headers: Iterable[AnyStr] = ()):
        if not headers:
            headers = [REQUIRED_HEADERS[0]]
            self._write_last_header = True
        for header in headers:
            self._file_descriptor.write(header)
            self._file_descriptor.write('\n')

    def write_variants(self, variants: Iterable[Variant]):
        for variant in variants:
            self.write_variant(variant)

    def write_variant(self, variant: Variant):
        if self._write_last_header:
            self._file_descriptor.write(REQUIRED_HEADERS[-1].format(sample_names='\t'.join(variant.sample_names)))
            self._file_descriptor.write('\n')
            self._write_last_header = False

        self._file_descriptor.write(variant.to_vcf_line())
        self._file_descriptor.write('\n')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
        return False

    def close(self):
        self._file_descriptor.close()
