# from zkill_share import 
import requests
import requests_mock
import unittest

session = requests.Session()
adapter = requests_mock.Adapter()
session.mount('mock', adapter)
huf_rate_jpy = 2.9980562833  # jpy base
jpy_rate_huf = 0.3335494419  # huf base
usd_rate_jpy = 0.009183639  # jpy base
eur_rate_jpy = 0.0084509423  # jpy base


class TestSzamok(unittest.TestCase):

    def test_power(self):
        self.assertEqual(get_power(1), 0)
        self.assertEqual(get_power(10), 1)
        self.assertEqual(get_power(100), 2)
        self.assertEqual(get_power(1000), 3)
        self.assertEqual(get_power(10000), 4)
        self.assertEqual(get_power(100000), 5)
        self.assertEqual(get_power(1000000), 6)
        self.assertEqual(get_power(10000000), 7)
        self.assertEqual(get_power(100000000), 8)
        self.assertEqual(get_power(1000000000), 9)
        self.assertEqual(get_power(10000000000), 10)
        self.assertEqual(get_power(100000000000), 11)
        self.assertEqual(get_power(1000000000000), 12)
        self.assertEqual(get_power(10000000000000), 13)
        self.assertEqual(get_power(100000000000000), 14)
        self.assertEqual(get_power(1000000000000000), 15)
        self.assertEqual(get_power(10000000000000000), 16)
        self.assertEqual(get_power(100000000000000000), 17)
        self.assertEqual(get_power(10000000000000000000000), 22)

    def test_get_number(self):
        self.assertEqual(get_number(1), "egy")
        self.assertEqual(get_number(9), "kilenc")

    def test_get_tizes(self):
        self.assertEqual(get_tizes(10), "tíz")
        self.assertEqual(get_tizes(20), "húsz")
        self.assertEqual(get_tizes(11), "tizen")
        self.assertEqual(get_tizes(21), "huszon")
        self.assertEqual(get_tizes(95), "kilencven")

    def test_get_szazas(self):
        self.assertEqual(get_szazas(100), "egyszáz")
        self.assertEqual(get_szazas(200), "kettőszáz")
        self.assertEqual(get_szazas(300), "háromszáz")
        self.assertEqual(get_szazas(900), "kilencszáz")

    def test_get_human_readable_format_hu(self):
        self.assertEqual(get_human_readable_format(1000000, "hu"), "1 millió")
        self.assertEqual(get_human_readable_format(10000000, "hu"), "10 millió")
        self.assertEqual(get_human_readable_format(100000000, "hu"), "100 millió")
        self.assertEqual(get_human_readable_format(1000000000, "hu"), "1 milliárd")
        self.assertEqual(get_human_readable_format(10000000000, "hu"), "10 milliárd")
        self.assertEqual(get_human_readable_format(100000000000, "hu"), "100 milliárd")
        self.assertEqual(get_human_readable_format(1000000000000, "hu"), "1 billió")
        self.assertEqual(get_human_readable_format(10000000000000, "hu"), "10 billió")
        self.assertEqual(get_human_readable_format(100000000000000, "hu"), "100 billió")
        self.assertEqual(get_human_readable_format(123400000000000, "hu"), "123 billió 400 milliárd")
        self.assertEqual(get_human_readable_format(123456000000000, "hu"), "123 billió 456 milliárd")
        self.assertEqual(get_human_readable_format(123456789000000, "hu"), "123 billió 456 milliárd 789 millió")
        self.assertEqual(get_human_readable_format(1000, "hu"), "1000")
        self.assertEqual(get_human_readable_format(1, "hu"), "1")
        self.assertEqual(get_human_readable_format(100000, "hu"), "100000")

    def test_get_human_readable_format_en(self):
        self.assertEqual(get_human_readable_format(1000000, "en"), "1 million")
        self.assertEqual(get_human_readable_format(10000000, "en"), "10 million")
        self.assertEqual(get_human_readable_format(100000000, "en"), "100 million")
        self.assertEqual(get_human_readable_format(1000000000, "en"), "1 billion")
        self.assertEqual(get_human_readable_format(10000000000, "en"), "10 billion")
        self.assertEqual(get_human_readable_format(100000000000, "en"), "100 billion")
        self.assertEqual(get_human_readable_format(1000000000000, "en"), "1 trillion")
        self.assertEqual(get_human_readable_format(10000000000000, "en"), "10 trillion")
        self.assertEqual(get_human_readable_format(100000000000000, "en"), "100 trillion")
        self.assertEqual(get_human_readable_format(123400000000000, "en"), "123 trillion 400 billion")
        self.assertEqual(get_human_readable_format(123456000000000, "en"), "123 trillion 456 billion")
        self.assertEqual(get_human_readable_format(123456789000000, "en"), "123 trillion 456 billion 789 million")


class TestConvert(unittest.TestCase):

    def test_convert_kanji(self):
        self.assertEqual(convert_kanji("1兆1"), 1000000000001)
        self.assertEqual(convert_kanji("9199兆9999億1000万2千5百67"), 9199999910002567)

    def test_reconvert(self):
        self.assertEqual(reconvert(99), "99")
        self.assertEqual(reconvert(100), "百")
        self.assertEqual(reconvert(200), "2百")
        self.assertEqual(reconvert(234), "2百34")
        self.assertEqual(reconvert(1000), "千")
        self.assertEqual(reconvert(1234), "千2百34")
        self.assertEqual(reconvert(2000), "2千")
        self.assertEqual(reconvert(2567), "2千5百67")
        self.assertEqual(reconvert(10000), "1万")
        self.assertEqual(reconvert(12567), "1万2千5百67")
        self.assertEqual(reconvert(102567), "10万2千5百67")
        self.assertEqual(reconvert(1002567), "100万2千5百67")
        self.assertEqual(reconvert(1002567), "100万2千5百67")
        self.assertEqual(reconvert(10002567), "1000万2千5百67")
        self.assertEqual(reconvert(100000000), "1億")
        self.assertEqual(reconvert(110002567), "1億1000万2千5百67")
        self.assertEqual(reconvert(1000000000000), "1兆")
        self.assertEqual(reconvert(1000110002567), "1兆1億1000万2千5百67")
        self.assertEqual(reconvert(1001010002567), "1兆10億1000万2千5百67")
        self.assertEqual(reconvert(1011010002567), "1兆110億1000万2千5百67")
        self.assertEqual(reconvert(1111010002567), "1兆1110億1000万2千5百67")
        self.assertEqual(reconvert(9999910002567), "9兆9999億1000万2千5百67")
        self.assertEqual(reconvert(99999910002567), "99兆9999億1000万2千5百67")
        self.assertEqual(reconvert(199999910002567), "199兆9999億1000万2千5百67")
        self.assertEqual(reconvert(9199999910002567), "9199兆9999億1000万2千5百67")
        self.assertEqual(reconvert(9001200000000), "9兆12億")


class TestExchange(unittest.TestCase):

    def test_get_exchange_url(self):
        self.assertEqual(get_exchange_url('JPY', 'HUF'), "https://api.exchangeratesapi.io/latest?base=JPY&symbols=HUF")
        self.assertEqual(get_exchange_url('HUF', 'JPY'), "https://api.exchangeratesapi.io/latest?base=HUF&symbols=JPY")
        self.assertEqual(get_exchange_url('JPY', 'USD'), "https://api.exchangeratesapi.io/latest?base=JPY&symbols=USD")

    @requests_mock.Mocker()
    def test_exchange(self, m):
        rate = {'rates': {'HUF': huf_rate_jpy}, 'base': 'JPY', 'date': '2020-04-09'}
        m.get('/latest?base=JPY&symbols=HUF', json=rate)
        self.assertEqual(exchange_rate('JPY', 'HUF'), rate)

    @requests_mock.Mocker()
    def test_xe_all(self, m):
        rate = {"rates": {"HUF": huf_rate_jpy, "EUR": eur_rate_jpy, "USD": usd_rate_jpy}, "base": "JPY", "date": "2020-04-09"}
        m.get('/latest', json=rate)
        got = xe_all(1000, 'JPY')
        self.assertEqual(got['HUF']['converted'], huf_rate_jpy*1000)
        self.assertEqual(got['USD']['converted'], usd_rate_jpy*1000)
        self.assertEqual(got['EUR']['converted'], eur_rate_jpy*1000)


if __name__ == '__main__':
    unittest.main()
