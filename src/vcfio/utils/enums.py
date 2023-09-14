from enum import Enum


class Zygosity(str, Enum):
    homozygote = 'HOM'
    heterozygote = 'HET'
    reference = 'REF'
    no_coverage = 'NO_COVERAGE'

    def __str__(self):
        return self.value
