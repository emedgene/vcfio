from __future__ import annotations

from cmath import nan
from collections import OrderedDict

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import AnyStr
    from typing import List
    from typing import Tuple

from vcfio.utils.easy_dict import EasyDict
from vcfio.utils.str_utils import standardize_chromosome
from vcfio.utils.str_utils import to_number


class VariantProperties:
    # Variant is split into 2 classes to avoid a "War and Peace" situation
    # This class is for Variant's properties and basic parsing methods

    def __init__(self, chromosome=None, position=None, vcf_id=None, ref=None, alt=None, quality=None,
                 vcf_filter=None, info=None, sample_format=None, sample_names=None, samples=None):
        """
        All parameters are raw strings, the class' properties will parse them (if needed).
        All the raw attributes are stored as _<attribute-name> and the properties are without _ .
        """
        self._chromosome = chromosome
        self._position = position
        self._vcf_id = vcf_id
        self._ref = ref
        self._alt = alt
        self._quality = quality
        if vcf_filter is None:
            vcf_filter = []
        self._vcf_filter = vcf_filter
        self._raw_info = info
        self._parsed_info = None
        self._sample_format = sample_format
        if samples is None:
            samples = []
        if sample_names is None:
            sample_names = []
        self._sample_names = sample_names
        self._raw_samples = tuple(samples)
        self._parsed_samples = None

    @property
    def chromosome(self) -> AnyStr:
        return standardize_chromosome(self._chromosome)

    @chromosome.setter
    def chromosome(self, value):
        self._chromosome = value

    @property
    def position(self):
        return int(self._position)

    @position.setter
    def position(self, value):
        self._position = value

    @property
    def vcf_id(self):
        return self._vcf_id

    @vcf_id.setter
    def vcf_id(self, value):
        self._vcf_id = value

    @property
    def ref(self):
        return self._ref

    @ref.setter
    def ref(self, value):
        self._ref = value

    @property
    def alt(self):
        if isinstance(self._alt, str):
            return self._alt.split(',')
        return self._alt

    @alt.setter
    def alt(self, value):
        self._alt = value

    @property
    def quality(self):
        return to_number(self._quality, default=0)

    @quality.setter
    def quality(self, value):
        self._quality = value

    @property
    def vcf_filter(self) -> List[AnyStr]:
        if isinstance(self._vcf_filter, str):
            return self._vcf_filter.split(';')
        if isinstance(self._vcf_filter, list):
            return self._vcf_filter
        return []

    @property
    def info(self):
        # Already parsed
        if self._parsed_info:
            return self._parsed_info

        # User set the value (example: variant.info = {'SVTYPE': 'DEL', 'DN': 'DeNovo'}
        if isinstance(self._raw_info, dict):
            self._parsed_info = EasyDict(self._raw_info)
            return self._parsed_info

        self._parsed_info = EasyDict()

        # Empty values
        if self._raw_info is None or self._raw_info == '.':
            return self._parsed_info

        # Parse
        if isinstance(self._raw_info, str):
            for pair in self._raw_info.split(';'):
                """
                key=val; --> key: val
                key=;    --> key: ''
                key;     --> key: nan
                """
                key, *val = pair.split('=', 1)
                self._parsed_info[key] = val[0] if val else nan

        return self._parsed_info

    @info.setter
    def info(self, value):
        self._raw_info = value

    @property
    def sample_format(self) -> Tuple[AnyStr]:
        if isinstance(self._sample_format, (list, tuple)):
            return tuple(self._sample_format)

        return tuple(self._sample_format.split(':'))

    @sample_format.setter
    def sample_format(self, value):
        self._sample_format = value

    @property
    def sample_names(self) -> Tuple:
        if isinstance(self._sample_names, str):
            return tuple(self._sample_names.split(','))

        return tuple(self._sample_names)

    @property
    def samples(self):
        # Already parsed
        if self._parsed_samples:
            self._parsed_samples = OrderedDict(((key, EasyDict(val)) for key, val in self._parsed_samples.items()))
            return self._parsed_samples

        # User set the values (example: variant.samples = {'DP': 10, 'GT': '1/0'})
        if isinstance(self._raw_samples, dict) and not isinstance(self._raw_samples, OrderedDict):
            self._parsed_samples = OrderedDict(((key, EasyDict(val)) for key, val in self._raw_samples.items()))
            return self._parsed_samples

        # parse the samples
        self._parsed_samples = OrderedDict()
        for name, raw_sample in zip(self.sample_names, self._raw_samples):
            self._parsed_samples[name] = EasyDict(zip(self.sample_format, raw_sample.split(':')))
        return self._parsed_samples

    @samples.setter
    def samples(self, value):
        self._raw_samples = value

    def __repr__(self):
        return f'Variant(chromosome={self.chromosome},position={self.position},ref={self.ref},alt={self.alt})'
