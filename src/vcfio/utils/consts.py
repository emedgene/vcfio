from vcfio.utils.enums import Zygosity

GT_ZYGOSITY_MAP = {
    ('0', '0'): Zygosity.reference,
    ('0', '1'): Zygosity.heterozygote,
    ('1', '0'): Zygosity.heterozygote,
    ('1', '1'): Zygosity.homozygote,
    ('1', '2'): Zygosity.heterozygote,
    ('2', '1'): Zygosity.heterozygote,
}