from pathlib import Path

import pytest

from vcfio import VcfReader
from vcfio import VcfWriter
from vcfio.utils.file_utils import open_file


class TestVcfWriter:
    @pytest.mark.parametrize("input_file, expected_output_file", (
            ('tests/samples/sample1.vcf', 'tests/samples/sample1.vcf'),
    ))
    def test_write_w_variants_headers(self, input_file, expected_output_file):
        output_path = Path('/tmp/output.vcf')
        with VcfReader(input_file) as reader, VcfWriter(output_path, variants=reader, headers=reader.headers) as writer:
            writer.write()
        assert output_path.read_bytes().strip() == Path(expected_output_file).read_bytes().strip()

    @pytest.mark.parametrize("input_file, expected_output_file", (
            ('tests/samples/sample1.vcf', 'tests/samples/sample1.no_headers.vcf'),
    ))
    def test_write_w_variants(self, input_file, expected_output_file):
        output_path = Path('/tmp/output.vcf')
        with VcfReader(input_file) as reader, VcfWriter(output_path, variants=reader) as writer:
            writer.write()
        assert output_path.read_bytes().strip() == Path(expected_output_file).read_bytes().strip()

    @pytest.mark.parametrize("input_file, expected_output_file", (
            ('tests/samples/sample1.vcf', 'tests/samples/sample1.no_variants.vcf'),
    ))
    def test_write_w_headers(self, input_file, expected_output_file):
        output_path = Path('/tmp/output.vcf')
        with VcfReader(input_file) as reader, VcfWriter(output_path, headers=reader.headers) as writer:
            writer.write()
        assert output_path.read_bytes().strip() == Path(expected_output_file).read_bytes().strip()

    @pytest.mark.none
    @pytest.mark.pysam
    @pytest.mark.biopython
    @pytest.mark.both
    @pytest.mark.parametrize("output_suffix, input_file, write_headers, expected_output_file", (
            ('.vcf', 'tests/samples/sample1.vcf', True, 'tests/samples/sample1.vcf'),
            ('.vcf.gz', 'tests/samples/sample1.vcf', True, 'tests/samples/sample1.vcf'),
            ('.vcf.bgz', 'tests/samples/sample1.vcf', True, 'tests/samples/sample1.vcf'),
            ('.vcf', 'tests/samples/sample1.vcf.gz', True, 'tests/samples/sample1.vcf'),
            ('.vcf.gz', 'tests/samples/sample1.vcf.gz', True, 'tests/samples/sample1.vcf'),
            ('.vcf.bgz', 'tests/samples/sample1.vcf.gz', True, 'tests/samples/sample1.vcf'),
            ('.vcf', 'tests/samples/sample1.vcf.bgz', True, 'tests/samples/sample1.vcf'),
            ('.vcf.gz', 'tests/samples/sample1.vcf.bgz', True, 'tests/samples/sample1.vcf'),
            ('.vcf.bgz', 'tests/samples/sample1.vcf.bgz', True, 'tests/samples/sample1.vcf'),
            ('.vcf', 'tests/samples/sample1.tabixed.vcf.bgz', True, 'tests/samples/sample1.vcf'),
            ('.vcf.gz', 'tests/samples/sample1.tabixed.vcf.bgz', True, 'tests/samples/sample1.vcf'),
            ('.vcf.bgz', 'tests/samples/sample1.tabixed.vcf.bgz', True, 'tests/samples/sample1.vcf'),
    ))
    def test_write_filetypes(self, tmp_path, output_suffix, input_file, write_headers, expected_output_file):
        output_path = tmp_path / ('output' + output_suffix)
        with VcfReader(input_file) as reader, VcfWriter(output_path, headers=reader.headers, variants=reader) as writer:
            writer.write()
        assert open_file(output_path).read(9999999).encode().strip() == Path(expected_output_file).read_bytes().strip()
