import hashlib
import re
from cmath import nan
from typing import AnyStr
from typing import Iterable
from typing import TextIO

from vcfio.utils.consts import VALID_CHROMOSOMES
from vcfio.utils.enums import Zygosity
from vcfio.utils.exceptions import InvalidVariantLine
from vcfio.utils.exceptions import InvalidZygosity
from vcfio.utils.str_utils import calculate_zygosity
from vcfio.variant.variant_properties import VariantProperties


class Variant(VariantProperties):
    # A class with implementation of methods

    def is_sv(self) -> bool:
        """ Return whether the variant is a structural variant """
        return self.info.get('SVTYPE') is not None

    def stringify_info(self):
        fields = []
        for key, val in self.info.items():
            if val is nan:
                res_string = key
            else:
                if isinstance(val, list):
                    val = ",".join(map(str, val))
                res_string = f"{key}={val}"
            fields.append(res_string)
        return ';'.join(fields).replace(" ", "_")

    def stringify_samples(self):
        def stringify_sample(value):
            """This method converts the value to string depending on the key"""
            if isinstance(value, list):
                converted_list = [str(element) if element is not None else '.' for element in value]
                result = ",".join(converted_list)
            else:
                result = str(value) if value is not None else '.'
            return result

        return [':'.join([stringify_sample(sample.get(format_field)) for format_field in self.sample_format])
                for sample in self.samples.values()]

    def to_vcf_line(self, with_samples: bool = True):
        return '\t'.join(map(str, [
            self.chromosome,
            self.position,
            self.vcf_id or '.',
            self.ref,
            ','.join(self.alt),
            self.quality or '.',
            ';'.join(self.vcf_filter) or '.',
            self.stringify_info() or '.',
        ] + ([':'.join(self.sample_format), *self.stringify_samples()] if with_samples else [])
                             )).strip()

    def get_zygosity(self, sample_name) -> Zygosity:
        gt = self.samples[sample_name].get('GT', './.')
        try:
            return calculate_zygosity(gt)
        except IndexError:
            raise InvalidZygosity(self.chromosome, self.position, gt)

    def is_sample_called(self, sample_name):
        return '.' not in self.samples[sample_name].get('GT', '.')

    def is_chromosome_valid(self):
        return self.chromosome in VALID_CHROMOSOMES

    @classmethod
    def from_variant_line(cls, variant_line: TextIO, sample_names: Iterable[AnyStr] = (),
                          default_sample_format: Iterable[AnyStr] = ()) -> 'Variant':
        """
        Create a Variant instance from a raw line
        Example:
            Input - "chr3    2956    .       G       GACACACAC       100     .       AC=1;AN=2;DP4=1,0,6,0;DP=7;IDV=6;IMF=0.857143;INDEL;MQ0F=0;MQ=51;SGB=-0.616816;VDB=0.041536;multiallele.gid=1   GT:PL:AD        0/1:111,0,113:0,4"
            Output - Variant(chromosome=chr3,position=2956,ref=G,alt=['GACACACAC'])
        """
        variant_line_values = re.split('\t| +', variant_line.strip('\n'))

        if len(variant_line_values) < 8:
            raise InvalidVariantLine(variant_line)

        chromosome, position, vcf_id, ref, alt, quality, vcf_filter, info = variant_line_values[:8]
        sample_format, *samples = variant_line_values[8:] or ('',)

        new_variant = cls(
            chromosome=chromosome,
            position=position,
            vcf_id=vcf_id,
            ref=ref,
            alt=alt,
            quality=quality,
            vcf_filter=vcf_filter,
            info=info,
            sample_format=sample_format or default_sample_format,
            sample_names=sample_names,
            samples=samples
        )

        return new_variant