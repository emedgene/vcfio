from itertools import zip_longest
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
        with VcfReader(input_file) as reader, VcfWriter(output_path) as writer:
            writer.write(variants=reader, headers=reader.headers)
        assert output_path.read_bytes().strip() == Path(expected_output_file).read_bytes().strip()

    @pytest.mark.parametrize("input_file, expected_output_file", (
            ('tests/samples/sample1.vcf', 'tests/samples/sample1.no_headers.vcf'),
    ))
    def test_write_w_variants(self, input_file, expected_output_file):
        output_path = Path('/tmp/output.vcf')
        with VcfReader(input_file) as reader, VcfWriter(output_path) as writer:
            writer.write(variants=reader)

        for actual_line, expected_line in zip_longest(output_path.read_bytes().splitlines(),
                                              Path(expected_output_file).read_bytes().splitlines()):
            if actual_line.startswith(b'#'):
                continue
            assert actual_line == expected_line

    @pytest.mark.parametrize("input_file, expected_output_file", (
            ('tests/samples/sample1.vcf', 'tests/samples/sample1.no_variants.vcf'),
    ))
    def test_write_w_headers(self, input_file, expected_output_file):
        output_path = Path('/tmp/output.vcf')
        with VcfReader(input_file) as reader, VcfWriter(output_path) as writer:
            writer.write(headers=reader.headers)
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
        with VcfReader(input_file) as reader, VcfWriter(output_path) as writer:
            writer.write(headers=reader.headers, variants=reader)
        assert open_file(output_path).read(9999999).encode().strip() == Path(expected_output_file).read_bytes().strip()

    @pytest.mark.parametrize("input_file, expected_output_file", (
            ('tests/samples/sample1.vcf', 'tests/samples/expected_info_headers_before_last_line.vcf'),
    ))
    def test_write_non_sorted_headers_at_the_end(self, input_file, expected_output_file):
        output_path = Path('/tmp/output.vcf')
        with VcfReader(input_file) as reader, VcfWriter(output_path) as writer:
            new_headers = [
                '##INFO=<ID=tier1_rank,Number=1,Type=Integer,Description="AI rank for tier 1">',
                '##INFO=<ID=tier2_rank,Number=1,Type=Integer,Description="AI rank for tier 2">'
            ]
            # add headers at the end of the headers list and write to file
            headers = reader.headers + new_headers
            writer.write(variants=reader, headers=headers)
        assert output_path.read_bytes().strip() == Path(expected_output_file).read_bytes().strip()

    @pytest.mark.parametrize("input_file, expected_output_file", (
            ('tests/samples/sample1.vcf', 'tests/samples/expected_info_headers_after_first_line.vcf'),
    ))
    def test_write_non_sorted_headers_at_the_beginning(self, input_file, expected_output_file):
        output_path = Path('/tmp/output.vcf')
        with VcfReader(input_file) as reader, VcfWriter(output_path) as writer:
            new_headers = [
                '##INFO=<ID=tier1_rank,Number=1,Type=Integer,Description="AI rank for tier 1">',
                '##INFO=<ID=tier2_rank,Number=1,Type=Integer,Description="AI rank for tier 2">'
            ]
            # add headers at the beginning of the headers list and write to file
            headers = new_headers + reader.headers
            writer.write(variants=reader, headers=headers)
        assert output_path.read_bytes().strip() == Path(expected_output_file).read_bytes().strip()

    @pytest.mark.parametrize("input_file, expected_output_file", (
            ('tests/samples/sample1.vcf', 'tests/samples/expected_info_headers_before_last_line.vcf'),
    ))
    def test_write_non_sorted_headers_at_the_end(self, input_file, expected_output_file):
        output_path = Path('/tmp/output.vcf')
        with VcfReader(input_file) as reader, VcfWriter(output_path) as writer:
            new_headers = [
                '##INFO=<ID=tier1_rank,Number=1,Type=Integer,Description="AI rank for tier 1">',
                '##INFO=<ID=tier2_rank,Number=1,Type=Integer,Description="AI rank for tier 2">'
            ]
            # add headers at the end of the headers list and write to file
            headers = reader.headers + new_headers
            writer.write(variants=reader, headers=headers)
        assert output_path.read_bytes().strip() == Path(expected_output_file).read_bytes().strip()
