from pathlib import Path
from typing import AnyStr
from typing import Iterable
from typing import List

from vcfio.utils.file_utils import open_file
from vcfio.variant.variant import Variant

REQUIRED_HEADERS = (
    '##fileformat=VCFv4.2',
    '#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT {sample_names}'
)


class VcfWriter:
    def __init__(self, output_file: AnyStr, headers: List[AnyStr] = REQUIRED_HEADERS,
                 variants: Iterable[Variant] = []):
        self.output_file = Path(output_file)
        self.headers = headers
        self.variants = variants
        self._headers_written = False

        self.file = open_file(self.output_file, mode='w')
        self._raw_variant_iterator = self.file

    def write(self):
        """
        Write the headers and variants to self.output_path
        ** This method will close the output file **
        """
        self._write_headers()
        for variant in self.variants:
            self.write_variant(variant)

    def _write_headers(self, sample_names=()):
        if not self._headers_written:
            for header in self.headers:
                if header == REQUIRED_HEADERS[-1]:
                    header = header.format(sample_names='\t'.join(sample_names))
                self.file.write(header)
                self.file.write('\n')
            self._headers_written = True

    def write_variant(self, variant):
        self._write_headers(variant.samples.keys())
        self.file.write(variant.to_vcf_line())
        self.file.write('\n')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
        return False

    def close(self):
        self.file.close()