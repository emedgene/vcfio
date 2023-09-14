import functools
from typing import AnyStr

from vcfio.utils.consts import GT_ZYGOSITY_MAP
from vcfio.utils.enums import Zygosity
from vcfio.utils.regex_patterns import GT_PATTERN


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


def calculate_zygosity(gt: AnyStr) -> Zygosity:
    """
    calculate zygosity of a sample
    examples:
        '0/1' -> HET
        './.' -> NO_COVERAGE
    """
    gt_pair = GT_PATTERN.findall(gt)[0]
    return GT_ZYGOSITY_MAP.get(gt_pair, Zygosity.no_coverage)