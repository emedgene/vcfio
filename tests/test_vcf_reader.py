from itertools import zip_longest

import pytest

from vcfio import VcfReader


class TestVcfReader:

    @pytest.mark.none
    @pytest.mark.parametrize("input_file, expected_variants", [('tests/samples/sample1.vcf', [
        "chr1	180235571	2E_2	C	<DEL>	.	PASS	SVTYPE=DEL;END=180243501;SVLEN=7930;DN=DeNovo;HET	GT:MQM:DP:AB:BQ:GQ:VCF:QUAL:AD:AZ:BC:CN	0/1:.:0:0.0:0:0:DRGN3.6:.:0,0:0:99999:.",
        "chr5	69728749	2E_2	G	<DEL>	.	PASS	SVTYPE=DEL;END=70242661;SVLEN=513912;DN=DeNovo;HET	GT:MQM:DP:AB:BQ:GQ:VCF:QUAL:AD:AZ:BC:CN	0/1:.:0:0.0:0:0:DRGN3.6:.:0,0:0:99999:.",
        "chr7	117199648	rs74571530	T	G	.	PASS	DN=;EFF=missense_variant(MODERATE|MISSENSE|tTt/tGt|p.Phe508Cys/c.1523T>G|1480|CFTR|protein_coding|CODING|NM_000492.3|11|1);HET	GT:MQM:DP:AB:BQ:GQ:VCF:QUAL:AD:AZ:BC:CN	0/1:250.0:53:0.45:0:48:DRGN3.6:.:29,24:0:99999:.", ])])
    def test_iteration(self, input_file, expected_variants):
        with VcfReader(input_file) as vcf_reader:
            for variant, expected_variant_line in zip_longest(vcf_reader, expected_variants):
                assert expected_variant_line == variant.to_vcf_line()

    @pytest.mark.parametrize("input_file, expected_values", [
        ('tests/samples/sample1.vcf', {'SVTYPE': {'id': 'SVTYPE', 'number': '1', 'type': 'String', 'desc': 'None', 'source': None, 'version': None}, 'END': {'id': 'END', 'number': '2', 'type': 'Integer', 'desc': 'None', 'source': None, 'version': None}, 'SVLEN': {'id': 'SVLEN', 'number': '3', 'type': 'Integer', 'desc': 'None', 'source': None, 'version': None}, 'DN': {'id': 'DN', 'number': '4', 'type': 'String', 'desc': 'None', 'source': None, 'version': None}, 'customized_column': {'id': 'customized_column', 'number': '5', 'type': 'String', 'desc': 'None', 'source': None, 'version': None}, 'NMD': {'id': 'NMD', 'number': '.', 'type': 'String', 'desc': "Predicted nonsense mediated decay effects for this variant. Format: 'Gene_Name | Gene_ID | Number_of_transcripts_in_gene | Percent_of_transcripts_affected' ", 'source': None, 'version': None}, 'LOF': {'id': 'LOF', 'number': '.', 'type': 'String', 'desc': "Predicted loss of function effects for this variant. Format: 'Gene_Name | Gene_ID | Number_of_transcripts_in_gene | Percent_of_transcripts_affected' ", 'source': None, 'version': None}, 'EFF': {'id': 'EFF', 'number': '.', 'type': 'String', 'desc': "Predicted effects for this variant.Format: 'Effect ( Effect_Impact | Functional_Class | Codon_Change | Amino_Acid_Change| Amino_Acid_length | Gene_Name | Transcript_BioType | Gene_Coding | Transcript_ID | Exon_Rank  | Genotype_Number [ | ERRORS | WARNINGS ] )' ", 'source': None, 'version': None}, 'VARTYPE': {'id': 'VARTYPE', 'number': 'A', 'type': 'Flag', 'desc': 'Variant types {SNP,MNP,INS,DEL,Mixed}', 'source': None, 'version': None}, 'HET': {'id': 'HET', 'number': '0', 'type': 'Flag', 'desc': 'Variant is heterozygous', 'source': None, 'version': None}, 'HOM': {'id': 'HOM', 'number': '0', 'type': 'Flag', 'desc': 'Variant is homozygous', 'source': None, 'version': None}, 'MIXED': {'id': 'MIXED', 'number': '0', 'type': 'Flag', 'desc': 'Variant is mixture of INS/DEL/SNP/MNP', 'source': None, 'version': None}, 'DEL': {'id': 'DEL', 'number': '0', 'type': 'Flag', 'desc': 'Variant is an deletion', 'source': None, 'version': None}, 'INS': {'id': 'INS', 'number': '0', 'type': 'Flag', 'desc': 'Variant is an insertion', 'source': None, 'version': None}, 'MNP': {'id': 'MNP', 'number': '0', 'type': 'Flag', 'desc': 'Variant is an MNP', 'source': None, 'version': None}, 'SNP': {'id': 'SNP', 'number': '0', 'type': 'Flag', 'desc': 'Variant is a SNP', 'source': None, 'version': None}, 'CSQ': {'id': 'CSQ', 'number': '.', 'type': 'String', 'desc': 'Consequence annotations from Ensembl VEP. Format: Allele|Consequence|IMPACT|SYMBOL|Gene|Feature_type|Feature|BIOTYPE|EXON|INTRON|HGVSc|HGVSp|cDNA_position|CDS_position|Protein_position|Amino_acids|Codons|Existing_variation|DISTANCE|STRAND|FLAGS|SYMBOL_SOURCE|HGNC_ID|REFSEQ_MATCH|REFSEQ_OFFSET|GIVEN_REF|USED_REF|BAM_EDIT|HGVS_OFFSET', 'source': None, 'version': None}})
    ])
    def test_infos(self, input_file, expected_values):
        with VcfReader(input_file) as vcf_reader:
            assert vcf_reader.infos == expected_values

    @pytest.mark.parametrize("input_file, expected_values", [('tests/samples/sample1.vcf', {'ALT': {'id': 'ALT', 'val': '<ID=DUP,Description="Region of elevated copy number relative ' 'to the reference">'}, 'DRAGENVersion': {'id': 'DRAGENVersion', 'val': '<ID=dragen,Version="SW: 05.021.572.3.6.3, HW: ' '05.021.572">'}, 'FILTER': {'id': 'FILTER', 'val': '<ID=MNP,Description="Multi nucleotide variant">'}, 'FORMAT': {'id': 'FORMAT', 'val': '<ID=CN,Number=12,Type=String,Description="CN">'}, 'INFO': {'id': 'INFO', 'val': '<ID=CSQ,Number=.,Type=String,Description="Consequence ' 'annotations from Ensembl VEP. Format: ' 'Allele|Consequence|IMPACT|SYMBOL|Gene|Feature_type|Feature|BIOTYPE|EXON|INTRON|HGVSc|HGVSp|cDNA_position|CDS_position|Protein_position|Amino_acids|Codons|Existing_variation|DISTANCE|STRAND|FLAGS|SYMBOL_SOURCE|HGNC_ID|REFSEQ_MATCH|REFSEQ_OFFSET|GIVEN_REF|USED_REF|BAM_EDIT|HGVS_OFFSET">'}, 'SnpEffVersion': {'id': 'SnpEffVersion', 'val': '"4.0e (build 2014-09-13), by Pablo Cingolani"'}, 'SnpSiftVersion': {'id': 'SnpSiftVersion', 'val': '"SnpSift 4.0e (build 2014-09-13), by Pablo ' 'Cingolani"'}, 'VEP': {'id': 'VEP', 'val': '"v100" time="2021-10-13 10:10:15" ' 'cache="/root/.vep/homo_sapiens_refseq/100_GRCh37" ' 'ensembl-io=100 ensembl=100 ensembl-funcgen=100 ' 'ensembl-variation=100 1000genomes="phase3" COSMIC="90" ' 'ClinVar="201912" ESP="20141103" HGMD-PUBLIC="20194" ' 'assembly="GRCh37.p13" dbSNP="153" gencode="GENCODE 19" ' 'genebuild="2011-04" gnomAD="r2.1" polyphen="2.2.2" ' 'refseq="01_2015" regbuild="1.0" sift="sift5.2.2"'}, 'bcftools_mergeVersion': {'id': 'bcftools_mergeVersion', 'val': '1.9+htslib-1.9'}, 'bcftools_normVersion': {'id': 'bcftools_normVersion', 'val': '1.9+htslib-1.9'}, 'contig': {'id': 'contig', 'val': '<ID=chrY,length=59373566>'}, 'fileformat': {'id': 'fileformat', 'val': 'VCFv4.2'}, 'reference': {'id': 'reference', 'val': 'file:///home/centos/GRCh37/reference.bin'}})])
    def test_metadata(self, input_file, expected_values):
        with VcfReader(input_file) as vcf_reader:
            assert vcf_reader.metadata == expected_values

    @pytest.mark.parametrize("input_file, expected_values", [('tests/samples/sample1.vcf', {'chrM': {'id': 'chrM', 'length': '16569'}, 'chr1': {'id': 'chr1', 'length': '249250621'}, 'chr2': {'id': 'chr2', 'length': '243199373'}, 'chr3': {'id': 'chr3', 'length': '198022430'}, 'chr4': {'id': 'chr4', 'length': '191154276'}, 'chr5': {'id': 'chr5', 'length': '180915260'}, 'chr6': {'id': 'chr6', 'length': '171115067'}, 'chr7': {'id': 'chr7', 'length': '159138663'}, 'chr8': {'id': 'chr8', 'length': '146364022'}, 'chr9': {'id': 'chr9', 'length': '141213431'}, 'chr10': {'id': 'chr10', 'length': '135534747'}, 'chr11': {'id': 'chr11', 'length': '135006516'}, 'chr12': {'id': 'chr12', 'length': '133851895'}, 'chr13': {'id': 'chr13', 'length': '115169878'}, 'chr14': {'id': 'chr14', 'length': '107349540'}, 'chr15': {'id': 'chr15', 'length': '102531392'}, 'chr16': {'id': 'chr16', 'length': '90354753'}, 'chr17': {'id': 'chr17', 'length': '81195210'}, 'chr18': {'id': 'chr18', 'length': '78077248'}, 'chr19': {'id': 'chr19', 'length': '59128983'}, 'chr20': {'id': 'chr20', 'length': '63025520'}, 'chr21': {'id': 'chr21', 'length': '48129895'}, 'chr22': {'id': 'chr22', 'length': '51304566'}, 'chrX': {'id': 'chrX', 'length': '155270560'}, 'chrY': {'id': 'chrY', 'length': '59373566'}})])
    def test_contigs(self, input_file, expected_values):
        with VcfReader(input_file) as vcf_reader:
            assert vcf_reader.contigs == expected_values

    @pytest.mark.parametrize("input_file, expected_values", [('tests/samples/sample1.vcf', {'GT': {'id': 'GT', 'number': '0', 'type': 'String', 'desc': 'GT'}, 'MQM': {'id': 'MQM', 'number': '1', 'type': 'String', 'desc': 'MQM'}, 'DP': {'id': 'DP', 'number': '2', 'type': 'String', 'desc': 'DP'}, 'AB': {'id': 'AB', 'number': '3', 'type': 'String', 'desc': 'AB'}, 'BQ': {'id': 'BQ', 'number': '4', 'type': 'String', 'desc': 'BQ'}, 'GQ': {'id': 'GQ', 'number': '5', 'type': 'String', 'desc': 'GQ'}, 'VCF': {'id': 'VCF', 'number': '7', 'type': 'String', 'desc': 'VCF'}, 'QUAL': {'id': 'QUAL', 'number': '8', 'type': 'String', 'desc': 'QUAL'}, 'AD': {'id': 'AD', 'number': '9', 'type': 'String', 'desc': 'AD'}, 'AZ': {'id': 'AZ', 'number': '10', 'type': 'String', 'desc': 'AZ'}, 'BC': {'id': 'BC', 'number': '11', 'type': 'String', 'desc': 'BC'}, 'CN': {'id': 'CN', 'number': '12', 'type': 'String', 'desc': 'CN'}})])
    def test_formats(self, input_file, expected_values):
        with VcfReader(input_file) as vcf_reader:
            assert vcf_reader.formats == expected_values

    @pytest.mark.parametrize("input_file, expected_values", [('tests/samples/sample1.vcf', {'PASS': {'id': 'PASS', 'desc': 'All filters passed'}, 'SampleFT': {'id': 'SampleFT', 'desc': 'No sample passes all the sample-level filters (at the field FORMAT/FT)'}, 'cnvQual': {'id': 'cnvQual', 'desc': 'CNV with quality below 10'}, 'cnvBinSupportRatio': {'id': 'cnvBinSupportRatio', 'desc': 'CNV with low supporting number of bins with respect to event length'}, 'cnvCopyRatio': {'id': 'cnvCopyRatio', 'desc': 'CNV with copy ratio within +/- 0.2 of 1.0'}, 'DRAGENSnpHardQUAL': {'id': 'DRAGENSnpHardQUAL', 'desc': 'Set if true:QUAL < 10.41'}, 'DRAGENIndelHardQUAL': {'id': 'DRAGENIndelHardQUAL', 'desc': 'Set if true:QUAL < 7.83'}, 'LowDepth': {'id': 'LowDepth', 'desc': 'Set if true:DP <= 1'}, 'LowGQ': {'id': 'LowGQ', 'desc': 'Set if true:GQ = 0'}, 'PloidyConflict': {'id': 'PloidyConflict', 'desc': 'Genotype call from variant caller not consistent with chromosome ploidy'}, 'RMxNRepeatRegion': {'id': 'RMxNRepeatRegion', 'desc': 'Site filtered because all or part of the variant allele is a repeat of the reference'}, 'INDEL': {'id': 'INDEL', 'desc': 'Set if true:Qual < 10 || DP < 10.0'}, 'SNP': {'id': 'SNP', 'desc': 'Set if true:Qual < 10 || DP < 10.0'}, 'MNP': {'id': 'MNP', 'desc': 'Multi nucleotide variant'}})])
    def test_filters(self, input_file, expected_values):
        with VcfReader(input_file) as vcf_reader:
            assert vcf_reader.filters == expected_values

    @pytest.mark.parametrize("input_file, expected_values", [('tests/samples/sample1.vcf', {'CNV': {'id': 'CNV', 'desc': 'Copy number variant region'}, 'DEL': {'id': 'DEL', 'desc': 'Deletion relative to the reference'}, 'DUP': {'id': 'DUP', 'desc': 'Region of elevated copy number relative to the reference'}})])
    def test_alts(self, input_file, expected_values):
        with VcfReader(input_file) as vcf_reader:
            assert vcf_reader.alts == expected_values

    @pytest.mark.pysam
    @pytest.mark.none
    @pytest.mark.parametrize("input_file, chromosome, start, end, expected_output_path", [
        ('tests/samples/sample2.vcf.gz', 'chr1', 2200, 2202, 'tests/samples/sample2.fetched.vcf'),
        ('tests/samples/sample2.vcf', 'chr1', 2200, 2202, 'tests/samples/sample2.fetched.vcf'),
    ])
    def test_fetch(self, input_file, chromosome, start, end, expected_output_path):
        with VcfReader(input_file) as vcf_reader, open(expected_output_path) as expected_output_file:
            fetched = [variant.to_vcf_line() for variant in vcf_reader.fetch(chromosome, start, end)]
            expected_variant_lines = expected_output_file.read().splitlines()
            assert fetched == expected_variant_lines
