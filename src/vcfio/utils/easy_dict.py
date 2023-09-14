from vcfio.utils.str_utils import to_number


class EasyDict(dict):
    def get(self, key, default=None, empty_value='.', infer_type=False):
        """
        If single value
            If number
                return int / float
            Else
                return value
        If list
            If length = 1
                return first value
            Else
                return list
        """
        raw_val = super().get(key, default)

        if raw_val is None or raw_val == empty_value:
            return default

        if not infer_type:
            return raw_val

        if isinstance(raw_val, str) and ',' in raw_val:
            raw_val = raw_val.split(',')

        if isinstance(raw_val, list):
            if len(raw_val) == 1:
                return to_number(raw_val[0], default=raw_val)

            return [to_number(sub_val, default=sub_val) for sub_val in raw_val]

        return to_number(raw_val, default=raw_val)
