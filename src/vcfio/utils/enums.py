from enum import Enum
from enum import auto


class Zygosity(str, Enum):
    homozygote = 'HOM'
    heterozygote = 'HET'
    reference = 'REF'
    no_coverage = 'NO_COVERAGE'

    def __str__(self):
        return self.value

class Chromosomes(str, Enum):
    chr1 = auto()
    chr2 = auto()
    chr3 = auto()
    chr4 = auto()
    chr5 = auto()
    chr6 = auto()
    chr7 = auto()
    chr8 = auto()
    chr9 = auto()
    chr10 = auto()
    chr11 = auto()
    chr12 = auto()
    chr13 = auto()
    chr14 = auto()
    chr15 = auto()
    chr16 = auto()
    chr17 = auto()
    chr18 = auto()
    chr19 = auto()
    chr20 = auto()
    chr21 = auto()
    chr22 = auto()
    chrX = auto()
    chrY = auto()
    chrM = auto()