import typing
import unittest

from hanguel_jamo_morph_tokenizer import HanguelJamoMorphTokenizer


class HanguelJamoMorphTokenizerTestCase(unittest.TestCase):
    tokenizer: HanguelJamoMorphTokenizer

    @classmethod
    def setUpClass(cls) -> None:
        cls.tokenizer = HanguelJamoMorphTokenizer()

    def test_jamo_serializer(self):
        with self.subTest("가나다 -> ㄱㅏㄴㅏㄷㅏ"):
            result = self.tokenizer.jamo_tokenizer("가나다")
            self.assertEqual(result, "ㄱㅏㄴㅏㄷㅏ")

        with self.subTest("김밥 -> ㄱㅣㅁㅂㅏㅂ"):
            result = self.tokenizer.jamo_tokenizer("김밥")
            self.assertEqual(result, "ㄱㅣㅁㅂㅏㅂ")

        with self.subTest("다노 소바면 -> ㄷㅏㄴㅗㅅㅗㅂㅏㅁㅕㄴ"):
            result = self.tokenizer.jamo_tokenizer("다노 소바면")
            self.assertEqual(result, "ㄷㅏㄴㅗㅅㅗㅂㅏㅁㅕㄴ")

        with self.subTest("꼬들 볶음면 -> ㄲㅗㄷㅡㄹㅂㅗㄲㅇㅡㅁㅁㅕㄴ"):
            result = self.tokenizer.jamo_tokenizer("꼬들 볶음면")
            self.assertEqual(result, "ㄲㅗㄷㅡㄹㅂㅗㄲㅇㅡㅁㅁㅕㄴ")

        with self.subTest("개미핥기 -> ㄱㅐㅁㅣㅎㅏㄾㄱㅣ"):
            result = self.tokenizer.jamo_tokenizer("개미핥기")
            self.assertEqual(result, "ㄱㅐㅁㅣㅎㅏㄾㄱㅣ")

        with self.subTest("ABC타입 -> ABCㅌㅏㅇㅣㅂ"):
            result = self.tokenizer.jamo_tokenizer("ABC타입")
            self.assertEqual(result, "ABCㅌㅏㅇㅣㅂ")

    def test_chosung_tokenizer(self):
        with self.subTest("가나다 -> ㄱㄴㄷ"):
            result = self.tokenizer.chosung_tokenizer("가나다")
            self.assertEqual(result, "ㄱㄴㄷ")

        with self.subTest("김밥 -> ㄱㅂ"):
            result = self.tokenizer.chosung_tokenizer("김밥")
            self.assertEqual(result, "ㄱㅂ")

        with self.subTest("다노 소바면 -> ㄷㄴㅅㅂㅁ"):
            result = self.tokenizer.chosung_tokenizer("다노 소바면")
            self.assertEqual(result, "ㄷㄴㅅㅂㅁ")

        with self.subTest("꼬들 볶음면 -> ㄲㄷㅂㅇㅁ"):
            result = self.tokenizer.chosung_tokenizer("꼬들 볶음면")
            self.assertEqual(result, "ㄲㄷㅂㅇㅁ")

        with self.subTest("개미핥기 -> ㄱㅁㅎㄱ"):
            result = self.tokenizer.chosung_tokenizer("개미핥기")
            self.assertEqual(result, "ㄱㅁㅎㄱ")

        with self.subTest("ABC타입 -> ABCㅌㅇ"):
            result = self.tokenizer.chosung_tokenizer("ABC타입")
            self.assertEqual(result, "ABCㅌㅇ")

    def test_jungsung_tokenizer(self):
        with self.subTest("가나다 -> ㅏㅏㅏ"):
            result = self.tokenizer.jungsung_tokenizer("가나다")
            self.assertEqual(result, "ㅏㅏㅏ")

        with self.subTest("김밥 -> ㅣㅏ"):
            result = self.tokenizer.jungsung_tokenizer("김밥")
            self.assertEqual(result, "ㅣㅏ")

        with self.subTest("다노 소바면 -> ㅏㅗㅗㅏㅕ"):
            result = self.tokenizer.jungsung_tokenizer("다노 소바면")
            self.assertEqual(result, "ㅏㅗㅗㅏㅕ")

        with self.subTest("꼬들 볶음면 -> ㅗㅡㅗㅡㅕ"):
            result = self.tokenizer.jungsung_tokenizer("꼬들 볶음면")
            self.assertEqual(result, "ㅗㅡㅗㅡㅕ")

        with self.subTest("개미핥기 -> ㅐㅣㅏㅣ"):
            result = self.tokenizer.jungsung_tokenizer("개미핥기")
            self.assertEqual(result, "ㅐㅣㅏㅣ")

        with self.subTest("왓더핵 -> ㅘㅓㅐ"):
            result = self.tokenizer.jungsung_tokenizer("왓더핵")
            self.assertEqual(result, "ㅘㅓㅐ")

        with self.subTest("ABC타입 -> ABCㅏㅣ"):
            result = self.tokenizer.jungsung_tokenizer("ABC타입")
            self.assertEqual(result, "ABCㅏㅣ")

    def test_jongsung_tokenizer(self):
        with self.subTest("가나다 -> X "):
            result = self.tokenizer.jongsung_tokenizer("가나다")
            self.assertEqual(result, "")

        with self.subTest("김밥 -> ㅁㅂ"):
            result = self.tokenizer.jongsung_tokenizer("김밥")
            self.assertEqual(result, "ㅁㅂ")

        with self.subTest("다노 소바면 -> ㄴ"):
            result = self.tokenizer.jongsung_tokenizer("다노 소바면")
            self.assertEqual(result, "ㄴ")

        with self.subTest("꼬들 볶음면 -> ㄹㄲㅁㄴ"):
            result = self.tokenizer.jongsung_tokenizer("꼬들 볶음면")
            self.assertEqual(result, "ㄹㄲㅁㄴ")

        with self.subTest("개미핥기 -> ㄾ"):
            result = self.tokenizer.jongsung_tokenizer("개미핥기")
            self.assertEqual(result, "ㄾ")

        with self.subTest("ABC타입 -> ABCㅂ"):
            result = self.tokenizer.jongsung_tokenizer("ABC타입")
            self.assertEqual(result, "ABCㅂ")

    def test_engtokor_tokenizer(self):
        with self.subTest("가나다 -> rkskek "):
            result = self.tokenizer.convert_korean_to_english("가나다")
            self.assertEqual(result, "rkskek")

        with self.subTest("김밥 -> rlaqkq"):
            result = self.tokenizer.convert_korean_to_english("김밥")
            self.assertEqual(result, "rlaqkq")

        with self.subTest("다노 소바면 -> ekshthqkaus"):
            result = self.tokenizer.convert_korean_to_english("다노 소바면")
            self.assertEqual(result, "ekshthqkaus")

        with self.subTest("꼬들 볶음면 -> RhemfqhRdmaaus"):
            result = self.tokenizer.convert_korean_to_english("꼬들 볶음면")
            self.assertEqual(result, "RhemfqhRdmaaus")

        with self.subTest("개미핥기 -> roalgkfxrl"):
            result = self.tokenizer.convert_korean_to_english("개미핥기")
            self.assertEqual(result, "roalgkfxrl")
