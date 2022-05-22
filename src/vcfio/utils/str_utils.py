from __future__ import annotations
import functools
from typing import TYPE_CHECKING

from vcfio.utils.exceptions import GTException

if TYPE_CHECKING:
    from typing import AnyStr

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
    if chromosome == 'chrMT':
        chromosome = 'chrM'

    return chromosome


def calculate_zygosity(gt: AnyStr) -> Zygosity:
    """
    calculate zygosity of a sample
    examples:
        '0/1' -> HET
        './.' -> NO_COVERAGE
        '1/1' -> HOM
        '0/0' -> REF
        '1/3' -> HET
    """
    try:
        gt_set = set(GT_PATTERN.findall(gt)[0])
    except IndexError:
        raise GTException(gt)

    if gt_set == {'.'}:
        return Zygosity.no_coverage
    if gt_set == {'0'}:
        return Zygosity.reference
    if len(gt_set) == 1:
        return Zygosity.homozygote
    return Zygosity.heterozygote
