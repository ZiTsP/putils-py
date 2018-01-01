
import os.path as path
import re

class _CodingLanguage():
    AROUND_REG_FROM_COMPILED = None
    AROUND_REG_TO = r' \1 '

    PREF_REG_FROM_COMPILED = None
    PREF_REG_TO = r' \1'

    SUFF_REG_FROM_COMPILED = None
    SUFF_REG_TO = r'\1 '

    REG_SKIP_COMPILED = None

    def _sub(from_regex, to_regex, text):
        return from_regex.sub(to_regex, text) if from_regex and to_regex else text

    def _match(match_regex, text):
        return match_regex.match(text) if match_regex else False

    @classmethod
    def parse(cls, text):
        new_text = []
        for e in text:
            if cls._match(cls.REG_SKIP_COMPILED, e):
                new_text.append(e)
            else:
                e = cls._sub(cls.AROUND_REG_FROM_COMPILED, cls.AROUND_REG_TO, e)
                e = cls._sub(cls.PREF_REG_FROM_COMPILED, cls.PREF_REG_TO, e)
                e = cls._sub(cls.SUFF_REG_FROM_COMPILED, cls.SUFF_REG_TO, e)
                new_text.append(e)
        return new_text


class Java(_CodingLanguage):
    AROUND_REG_FROM_COMPILED = re.compile(r'([,;:\){}])')
    PREF_REG_FROM_COMPILED = re.compile(r'([\.])')
    SUFF_REG_FROM_COMPILED = re.compile(r'([\(])')
    REG_SKIP_COMPILED = re.compile(r'^package|^import')
