import typing

# ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
CHOSUNG = [0x3131, 0x3132, 0x3134, 0x3137, 0x3138, 0x3139, 0x3141, 0x3142, 0x3143, 0x3145, 0x3146,
           0x3147, 0x3148, 0x3149, 0x314a, 0x314b, 0x314c, 0x314d, 0x314e]

# ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']
JUNGSUNG = [0x314f, 0x3150, 0x3151, 0x3152, 0x3153, 0x3154, 0x3155, 0x3156, 0x3157, 0x3158, 0x3159,
            0x315a, 0x315b, 0x315c, 0x315d, 0x315e, 0x315f, 0x3160, 0x3161, 0x3162, 0x3163]

# [' ', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ',
# 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
JONGSUNG = [0x0000, 0x3131, 0x3132, 0x3133, 0x3134, 0x3135, 0x3136, 0x3137, 0x3139, 0x313a, 0x313b,
            0x313c, 0x313d, 0x313e, 0x313f, 0x3140, 0x3141, 0x3142, 0x3144, 0x3145, 0x3146, 0x3147,
            0x3148, 0x314a, 0x314b, 0x314c, 0x314d, 0x314e]

CHOSUNG_EN = ["r", "R", "s", "e", "E", "f", "a", "q", "Q", "t", "T", "d", "w", "W", "c", "z", "x", "v", "g"]

JUNGSUNG_EN = ["k", "o", "i", "O", "j", "p", "u", "P", "h", "hk", "ho", "hl", "y", "n", "nj", "np", "nl", "b", "m",
               "ml", "l"]

CHOSUNG_BEGIN_UNICODE = 12593
CHOSUNG_END_UNICODE = 12622
HANGUEL_BEGIN_UNICODE = 44032
HANGUEL_END_UNICODE = 55203
NUMBER_BEGIN_UNICODE = 48
NUMBER_END_UNICODE = 57
ENGLISH_LOWER_BEGIN_UNICODE = 65
ENGLISH_LOWER_END_UNICODE = 90
ENGLISH_UPPER_BEGIN_UNICODE = 97
ENGLISH_UPPER_END_UNICODE = 122

JONGSUNG_EN = ["", "r", "R", "rt", "s", "sw", "sg", "e", "f", "fr", "fa",
               "fq", "ft", "fx", "fv", "fg", "a", "q", "qt", "t", "T", "d", "w", "c", "z", "x", "v", "g"]

LETTER_EN = ["r", "R", "rt", "s", "sw", "sg", "e", "E", "f", "fr", "fa",
             "fq", "ft", "fx", "fv", "fg", "a", "q", "Q", "qt", "t", "T", "d", "w", "W", "c", "z", "x",
             "v", "g"]


class HanguelJamoMorphTokenizer:
    """
    [분리 기본 공식]
    초성 = ( ( (글자 - 0xAC00) - (글자 - 0xAC00) % 28 ) ) / 28 ) / 21
    중성 = ( ( (글자 - 0xAC00) - (글자 - 0xAC00) % 28 ) ) / 28 ) % 21
    종성 = (글자 - 0xAC00) % 28

    [합치기 기본 공식]
    원문 = 0xAC00 + 28 * 21 * (초성의 index) + 28 * (중성의 index) + (종성의 index)
    각 index 정보는 CHOSUNG, JUNGSUNG, JONGSUNG char[]에 정의한 index 입니다.
    하지만 아래 코드에서는 원문이 필요 없기 때문에 합치기 위한 로직은 포함 되어 있지 않습니다.
    """

    @staticmethod
    def is_possible_character(c: str) -> bool:
        c = ord(c)
        return (
                (NUMBER_BEGIN_UNICODE <= c <= NUMBER_END_UNICODE)
                or (ENGLISH_UPPER_BEGIN_UNICODE <= c <= ENGLISH_UPPER_END_UNICODE)
                or (ENGLISH_LOWER_BEGIN_UNICODE <= c <= ENGLISH_LOWER_END_UNICODE)
                or (HANGUEL_BEGIN_UNICODE <= c <= HANGUEL_END_UNICODE)
                or (CHOSUNG_BEGIN_UNICODE <= c <= CHOSUNG_END_UNICODE)
        )

    def tokenizer(self, source: str, jamo_type: str) -> str:
        _jamo_type_tokenizers: typing.Dict[str, typing.Callable] = dict(
            CHOSUNG=self.chosung_tokenizer,
            JUNGSUNG=self.jungsung_tokenizer,
            JONGSUNG=self.jongsung_tokenizer,
            KORTOENG=self.convert_korean_to_english,
        )

        jamo = _jamo_type_tokenizers.get(jamo_type, self.jamo_tokenizer)(source)
        return jamo

    def jamo_tokenizer(self, source: str) -> str:
        jamo = ""
        for _c in source:
            c = ord(_c)
            if c >= 0xAC00:
                criteria = c - 0xAC00
                jamo_idx = (((criteria - (criteria % 28)) // 28) // 21)
                jamo_idx = int(jamo_idx)

                jamo += chr(CHOSUNG[jamo_idx])

                jamo_idx = (((criteria - (criteria % 28)) / 28) % 21)
                jamo_idx = int(jamo_idx)

                jamo += chr(JUNGSUNG[jamo_idx])

                jamo_idx = ((c - 0xAC00) % 28)

                if jamo_idx != 0:
                    jamo += chr(JONGSUNG[jamo_idx])

            elif self.is_possible_character(_c):
                jamo += _c

        return jamo

    def chosung_tokenizer(self, source: str) -> str:
        chosung = ""
        for _c in source:
            c = ord(_c)
            if c >= 0xAC00:
                criteria = c - 0xAC00
                jamo_idx = (((criteria - (criteria % 28)) // 28) // 21)
                jamo_idx = int(jamo_idx)

                chosung += chr(CHOSUNG[jamo_idx])

            elif self.is_possible_character(_c):
                chosung += _c

        return chosung

    def jungsung_tokenizer(self, source: str) -> str:
        jungsung = ""
        for _c in source:
            c = ord(_c)
            if c >= 0xAC00:
                criteria = c - 0xAC00
                jamo_idx = (((criteria - (criteria % 28)) / 28) % 21)
                jamo_idx = int(jamo_idx)

                jungsung += chr(JUNGSUNG[jamo_idx])

            elif self.is_possible_character(_c):
                jungsung += _c

        return jungsung

    def jongsung_tokenizer(self, source: str) -> str:
        jongsung = ""
        for _c in source:
            c = ord(_c)
            if c >= 0xAC00:
                jamo_idx = ((c - 0xAC00) % 28)

                if jamo_idx != 0:
                    jongsung += chr(JONGSUNG[jamo_idx])

            elif self.is_possible_character(_c):
                jongsung += _c

        return jongsung

    def convert_korean_to_english(self, source: str) -> str:
        english = ""

        for _c in source:
            c = ord(_c)
            criteria = c - 0xAC00
            cho_idx = criteria // (21 * 28)
            jung_idx = criteria % (21 * 28) // 28
            jong_idx = criteria % (21 * 28) % 28

            if c >= 0xAC00:
                english += CHOSUNG_EN[cho_idx] + JUNGSUNG_EN[jung_idx]

                if jong_idx != 0:
                    english += JONGSUNG_EN[jong_idx]

            elif self.is_possible_character(_c):
                english += _c

        return english
