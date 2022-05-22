import re

# The following regular expressions were taken from PyVCF
# https://github.com/jamescasbon/PyVCF/blob/476169cd457ba0caa6b998b301a4d91e975251d9/vcf/parser.py#L84-L111

INFO_PATTERN = re.compile(r'''\#\#INFO=<
            ID=(?P<id>[^,]+),\s*
            Number=(?P<number>-?\d+|\.|[AGR]),\s*
            Type=(?P<type>Integer|Float|Flag|Character|String),\s*
            Description="(?P<desc>[^"]*)"
            (?:,\s*Source="(?P<source>[^"]*)")?
            (?:,\s*Version="?(?P<version>[^"]*)"?)?
            >''', re.VERBOSE)

FILTER_PATTERN = re.compile(r'''\#\#FILTER=<
            ID=(?P<id>[^,]+),\s*
            Description="(?P<desc>[^"]*)"
            >''', re.VERBOSE)

ALT_PATTERN = re.compile(r'''\#\#ALT=<
            ID=(?P<id>[^,]+),\s*
            Description="(?P<desc>[^"]*)"
            >''', re.VERBOSE)

FORMAT_PATTERN = re.compile(r'''\#\#FORMAT=<
            ID=(?P<id>.+),\s*
            Number=(?P<number>-?\d+|\.|[AGR]),\s*
            Type=(?P<type>.+),\s*
            Description="(?P<desc>.*)"
            >''', re.VERBOSE)

CONTIG_PATTERN = re.compile(r'''\#\#contig=<
            ID=(?P<id>[^>,]+)
            (,.*length=(?P<length>-?\d+))?
            .*
            >''', re.VERBOSE)

META_PATTERN = re.compile(r'''##(?P<id>.+?)=(?P<val>.+)''')

GT_PATTERN = re.compile('([0-9]+|\.)[/|]([0-9]+|\.)')
