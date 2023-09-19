from cmath import nan

import pytest

from vcfio import Variant
from vcfio.utils.enums import Zygosity


class TestVariant:

    @pytest.mark.parametrize("line, sample_names, expected_output", [
        ('chr1	726	.	G	C,T	500	.	DP=200;MQ=250.00	GT:AD:AF:DP:GQ	0/1:10,160,30:0.8,0.15:200:420', [], 'chr1	726	.	G	C,T	500	.	DP=200;MQ=250.00'),
        ('chr1	726	.	G	C,T	500	.	DP=200;MQ=250.00	GT:AD:AF:DP:GQ	0/1:10,160,30:0.8,0.15:200:420', ['proband'], 'chr1	726	.	G	C,T	500	.	DP=200;MQ=250.00	GT:AD:AF:DP:GQ	0/1:10,160,30:0.8,0.15:200:420'),
        ('chr1	3348	.	T	C	50.3687	badReads	AN=1	GT:MQM:DP:AB:BQ:GQ:VCF:QUAL:AD:PL:SB	0/0:.:26:.:.:.:.:.:.:.:.	0/0:.:27:.:.:.:.:.:.:.:.	0/1:60:30.0:0.28:50.3687:99.0:FB,GTK,PLTP,SAM,GTK4:50.3687:.:.:.', ['father', 'mother', 'proband'], 'chr1	3348	.	T	C	50.3687	badReads	AN=1	GT:MQM:DP:AB:BQ:GQ:VCF:QUAL:AD:PL:SB	0/0:.:26:.:.:.:.:.:.:.:.	0/0:.:27:.:.:.:.:.:.:.:.	0/1:60:30.0:0.28:50.3687:99.0:FB,GTK,PLTP,SAM,GTK4:50.3687:.:.:.'),
    ])
    def test_from_variant_line(self, line, sample_names, expected_output):
        variant = Variant.from_variant_line(line, sample_names=sample_names)
        assert expected_output == variant.to_vcf_line(with_samples=bool(sample_names))

    @pytest.mark.parametrize("line, sample_names, expected_output", [
        ('chr1	726	.	G	C,T	500	.	DP=200;MQ=250.00	GT:AD:AF:DP:GQ	0/1:10,160,30:0.8,0.15:200:420', ['proband'], 'DP=200;MQ=250.00'),
    ])
    def test_stringify_info(self, line, sample_names, expected_output):
        variant = Variant.from_variant_line(line, sample_names=sample_names)
        output = variant.stringify_info()
        assert expected_output == output

    @pytest.mark.parametrize("line, sample_names, expected_output", [
        ('chr1	726	.	G	C,T	500	.	DP=200;MQ=250.00	GT:AD:AF:DP:GQ	0/1:10,160,30:0.8,0.15:200:420', ['proband'], ['0/1:10,160,30:0.8,0.15:200:420']),
        ('chr1	726	.	G	C,T	500	.	DP=200;MQ=250.00	GT:AD:AF:DP:GQ	0/1:10,160,30:0.8,0.15:200:420  0/1:10,160,30:0.8,0.15:200:420', ['proband', 'father'], ['0/1:10,160,30:0.8,0.15:200:420', '0/1:10,160,30:0.8,0.15:200:420']),
    ])
    def test_stringify_samples(self, line, sample_names, expected_output):
        variant = Variant.from_variant_line(line, sample_names=sample_names)
        output = variant.stringify_samples()
        assert expected_output == output

    @pytest.mark.parametrize("line, sample_names, expected_output", [
        ('chr1	726	.	G	C,T	500	.	DP=200;MQ=250.00	GT:AD:AF:DP:GQ	0/1:10,160,30:0.8,0.15:200:420', ['proband'], {'proband': {'GT': '0/1', 'AD': '10,160,30', 'AF': '0.8,0.15', 'DP': '200', 'GQ': '420'}}),
    ])
    def test_samples(self, line, sample_names, expected_output):
        variant = Variant.from_variant_line(line, sample_names=sample_names)
        assert expected_output == variant.samples

    @pytest.mark.parametrize("line, sample_names, new_value, expected_output", [
        ('chr1	726	.	G	C,T	500	.	DP=200;MQ=250.00	GT:AD:AF:DP:GQ	0/1:10,160,30:0.8,0.15:200:420', ['proband'], {'GT': '1/1'}, {'proband': {'GT': '1/1', 'AD': '10,160,30', 'AF': '0.8,0.15', 'DP': '200', 'GQ': '420'}}),
        ('chr1	726	.	G	C,T	500	.	DP=200;MQ=250.00	GT:AD:AF:DP:GQ	.', ['proband'], {'GT': '1/1'}, {'proband': {'GT': '1/1'}}),
    ])
    def test_samples_mutate(self, line, sample_names, new_value, expected_output):
        variant = Variant.from_variant_line(line, sample_names=sample_names)
        for sample in sample_names:
            variant.samples[sample].update(new_value)

        assert expected_output == variant.samples

    @pytest.mark.parametrize("line, sample_names, new_value, expected_output", [
        ('chr1	726	.	G	C,T	500	.	DP=200;MQ=250.00	GT:AD:AF:DP:GQ	0/1:10,160,30:0.8,0.15:200:420', ['proband'], {'proband': {'GT': '1/1'}}, {'proband': {'GT': '1/1'}}),
        ('chr1	726	.	G	C,T	500	.	DP=200;MQ=250.00	GT:AD:AF:DP:GQ	0/1:10,160,30:0.8,0.15:200:420', ['proband'], {'father': {'GT': '1/1'}}, {'father': {'GT': '1/1'}}),
        ('chr1	726	.	G	C,T	500	.	DP=200;MQ=250.00	GT:AD:AF:DP:GQ	.', ['proband'], {'proband': {'GT': '1/1'}}, {'proband': {'GT': '1/1'}}),
    ])
    def test_samples_setter(self, line, sample_names, new_value, expected_output):
        variant = Variant.from_variant_line(line, sample_names=sample_names)
        variant.samples = new_value
        assert expected_output == variant.samples

    @pytest.mark.parametrize("line, sample_names, expected_output", [
        ('chr1	726	.	G	C,T	500	.	DP=200;MQ=250.00	GT:AD:AF:DP:GQ	0/1:10,160,30:0.8,0.15:200:420', ['proband'], Zygosity.heterozygote),
        ('chr1	726	.	G	C,T	500	.	DP=200;MQ=250.00	GT:AD:AF:DP:GQ	1/1:10,160,30:0.8,0.15:200:420', ['proband'], Zygosity.homozygote),
        ('chr1	726	.	G	C,T	500	.	DP=200;MQ=250.00	GT:AD:AF:DP:GQ	0/0:10,160,30:0.8,0.15:200:420', ['proband'], Zygosity.reference),
    ])
    def test_get_zygosity(self, line, sample_names, expected_output):
        variant = Variant.from_variant_line(line, sample_names=sample_names)
        output = variant.get_zygosity('proband')
        assert expected_output == output

    @pytest.mark.parametrize("line, sample_names, new_chromosome, expected_output", [
        ('chr1	726	.	G	C,T	500	.	DP=200;MQ=250.00	GT:AD:AF:DP:GQ	0/1:10,160,30:0.8,0.15:200:420', ['proband'], 'chrM', 'chrM')
    ])
    def test_chromosome_setter(self, line, sample_names, new_chromosome, expected_output):
        variant = Variant.from_variant_line(line, sample_names=sample_names)
        variant.chromosome = new_chromosome
        assert expected_output == variant.chromosome

    @pytest.mark.parametrize("line, sample_names, expected_output", [
        ('chr1	726	.	G	C,T	500	.	DP=200;MQ=250.00	GT:AD:AF:DP:GQ	0/1:10,160,30:0.8,0.15:200:420', ['proband'], ['.']),
        ('chr1	726	.	G	C,T	500	PASS	DP=200;MQ=250.00	GT:AD:AF:DP:GQ	0/1:10,160,30:0.8,0.15:200:420', ['proband'], ['PASS']),
        ('chr1	726	.	G	C,T	500	filter	DP=200;MQ=250.00	GT:AD:AF:DP:GQ	0/1:10,160,30:0.8,0.15:200:420', ['proband'], ['filter']),
        ('chr1	726	.	G	C,T	500	filter1;filter2	DP=200;MQ=250.00	GT:AD:AF:DP:GQ	0/1:10,160,30:0.8,0.15:200:420', ['proband'], ['filter1', 'filter2']),
    ])
    def test_vcf_filter(self, line, sample_names, expected_output):
        variant = Variant.from_variant_line(line, sample_names=sample_names)
        assert expected_output == variant.vcf_filter

    @pytest.mark.parametrize("line, sample_names, expected_output", [
        ('chr1	726	.	G	C,T	500	.	DP=200;MQ=250.00	GT:AD:AF:DP:GQ	0/1:10,160,30:0.8,0.15:200:420', ['proband'], {'DP': '200', 'MQ': '250.00'}),
    ])
    def test_info(self, line, sample_names, expected_output):
        variant = Variant.from_variant_line(line, sample_names=sample_names)
        assert expected_output == variant.info

    @pytest.mark.parametrize("line, sample_names, key, expected_output", [
        ('chr1	726	.	G	C,T	500	.	DP=200;MQ=250.00	GT:AD:AF:DP:GQ	0/1:10,160,30:0.8,0.15:200:420', ['proband'], 'DP', 200),
        ('chr1	726	.	G	C,T	500	.	DP=200;MQ=250.00	GT:AD:AF:DP:GQ	0/1:10,160,30:0.8,0.15:200:420', ['proband'], 'MQ', 250),
        ('chr1	726	.	G	C,T	500	.	DP=200;MQ=250.00;K=1,2	GT:AD:AF:DP:GQ	0/1:10,160,30:0.8,0.15:200:420', ['proband'], 'K', [1, 2]),
        ('chr1	726	.	G	C,T	500	.	DP=200;MQ=250.00;K=a,b	GT:AD:AF:DP:GQ	0/1:10,160,30:0.8,0.15:200:420', ['proband'], 'K', ['a', 'b']),
    ])
    def test_info_get(self, line, sample_names, key, expected_output):
        variant = Variant.from_variant_line(line, sample_names=sample_names)
        output = variant.info.get(key, infer_type=True)
        assert expected_output == output

    @pytest.mark.parametrize("line, sample_names, key, new_val, expected_output", [
        ('chr1	726	.	G	C,T	500	.	DP=200;MQ=250.00	GT:AD:AF:DP:GQ	0/1:10,160,30:0.8,0.15:200:420', ['proband'], 'DP', 300, {'DP': 300, 'MQ': '250.00'}),
        ('chr1	726	.	G	C,T	500	.	.	GT:AD:AF:DP:GQ	0/1:10,160,30:0.8,0.15:200:420', ['proband'], 'DP', 300, {'DP': 300}),
    ])
    def test_info_mutate(self, line, sample_names, key, new_val, expected_output):
        variant = Variant.from_variant_line(line, sample_names=sample_names)
        variant.info[key] = new_val
        assert expected_output == variant.info

    @pytest.mark.parametrize("line, new_value, expected_output", [
        ('chr1	726	.	G	C,T	500	.	DP=200;MQ=250.00	GT:AD:AF:DP:GQ	0/1:10,160,30:0.8,0.15:200:420', {'key0': 'val0', 'key1': 'val1'}, {'key0': 'val0', 'key1': 'val1'}),
        ('chr1	726	.	G	C,T	500	.	DP=200;MQ=250.00	GT:AD:AF:DP:GQ	0/1:10,160,30:0.8,0.15:200:420', {'DP': 90}, {'DP': 90}),
        ('chr1	726	.	G	C,T	500	.	DP=200;MQ=250.00	GT:AD:AF:DP:GQ	0/1:10,160,30:0.8,0.15:200:420', 'DP=90;KEY0=VAL0;key1=;key2', {'DP': '90', 'KEY0': 'VAL0', 'key1': '', 'key2': nan}),
        ('chr1	726	.	G	C,T	500	.	.	GT:AD:AF:DP:GQ	0/1:10,160,30:0.8,0.15:200:420', 'DP=90;KEY0=VAL0;key1=;key2', {'DP': '90', 'KEY0': 'VAL0', 'key1': '', 'key2': nan}),
    ])
    def test_info_setter(self, line, new_value, expected_output):
        variant = Variant.from_variant_line(line)
        variant.info = new_value
        assert expected_output == variant.info
