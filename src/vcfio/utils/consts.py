from vcfio.utils.enums import Zygosity

VALID_CHROMOSOMES = [
    'chr1',
    'chr2',
    'chr3',
    'chr4',
    'chr5',
    'chr6',
    'chr7',
    'chr8',
    'chr9',
    'chr10',
    'chr11',
    'chr12',
    'chr13',
    'chr14',
    'chr15',
    'chr16',
    'chr17',
    'chr18',
    'chr19',
    'chr20',
    'chr21',
    'chr22',
    'chrX',
    'chrY',
    'chrM'
]

GT_ZYGOSITY_MAP = {
    ('0', '0'): Zygosity.reference,
    ('0', '1'): Zygosity.heterozygote,
    ('1', '0'): Zygosity.heterozygote,
    ('1', '1'): Zygosity.homozygote,
    ('1', '2'): Zygosity.heterozygote,
    ('2', '1'): Zygosity.heterozygote,
}