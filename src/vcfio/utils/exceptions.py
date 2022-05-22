from __future__ import annotations

from typing import AnyStr


class InvalidZygosity(Exception):
    def __init__(self, chromosome, position, zygosity):
        self.chromosome = chromosome
        self.position = position
        self.zygosity = zygosity

    def __str__(self):
        return f'Got invalid zygosity in {self.chromosome} at position {self.position}: {self.zygosity}'


class InvalidVariantLine(Exception):
    def __init__(self, line):
        self.line = line

    def __str__(self):
        return f'Variant line from vcf is invalid: {self.line}'


class GTException(Exception):
    def __init__(self, gt: AnyStr):
        self.gt = gt
    def __str__(self):
        return f'Invalid GT: {self.gt}'
