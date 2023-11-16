import functools
from typing import Optional

from vcfio.utils.enums import Zygosity


def to_number(value, default=''):
    """
    Try to convert value to int or float
    """
    try:
        x = max(int(value), float(value))
    except ValueError:
        try:
            x = float(value)
        except ValueError:
            x = default
    except TypeError:
        x = default
    return x


@functools.lru_cache(maxsize=2**16)
def standardize_chromosome(raw_chr):
    chromosome = raw_chr
    if not chromosome.startswith('chr'):
        chromosome = 'chr' + raw_chr
    if chromosome in ('chrM', 'chrMT'):
        chromosome = 'chrM'

    return chromosome


def calculate_zygosity(genotype: str) -> Optional[Zygosity]:
    """
    calculate zygosity of a sample
    examples:
        '0/1' -> HET
        './.' -> NO_COVERAGE
    """
    zygosity = None
    if len(genotype) == 1:
        zygosity = _parse_haploid(genotype)
    elif len(genotype) == 3:
        zygosity = _parse_diploid(genotype)

    return zygosity


def _parse_haploid(genotype: str) -> Optional[Zygosity]:
    if genotype == '0':
        return Zygosity.reference
    elif genotype.isdigit():
        return Zygosity.homozygote
    else:
        return None


def _parse_diploid(genotype: str) -> Optional[Zygosity]:
    x, sep, y = genotype[0], genotype[1], genotype[2]
    if sep not in '/|':
        return None
    elif x == '.' or y == '.':
        return Zygosity.no_coverage
    elif x == y:
        if x == '0':
            return Zygosity.reference
        elif x.isdigit():
            return Zygosity.homozygote
        else:
            return None
    else:
        if x.isdigit() and y.isdigit():
            return Zygosity.heterozygote
        else:
            return None
