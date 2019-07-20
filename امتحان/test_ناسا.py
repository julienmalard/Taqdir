import unittest
from json import JSONDecodeError

import pandas as pd
import pandas.testing as pdt
import requests
from pcse.db import NASAPowerWeatherDataProvider
from تقدیر.ذرائع import ناسا

جگہ = dict(عرض=11.02, طول=76.96, بلندی=1)
try:
    NASAPowerWeatherDataProvider(latitude=جگہ['عرض'], longitude=جگہ['طول'], force_update=False)
    جالبینی_رسائی = True
except (requests.exceptions.ConnectionError, KeyError, JSONDecodeError):
    جالبینی_رسائی = False
وجہ = 'ناسا کا جالبین صفھہ اب دستیاب نہیں۔'


class امتحان_ناسا(unittest.TestCase):
    @staticmethod
    def _پورا(سے, تک, اعداد):
        pdt.assert_index_equal(اعداد.روزانہ().index, pd.period_range(سے, تک, freq='D'))

    @unittest.skipUnless(جالبینی_رسائی, وجہ)
    def test_کوائف_پانا(خود):
        سے, تک = '۲۰۱۷۱۲۱۵', '۲۰۱۸۰۱۱۵'
        اعداد = ناسا().کوائف_پانا(سے, تک, **جگہ, خاکے='۴.۵')
        خود._پورا(سے, تک, اعداد)

    @unittest.skipUnless(جالبینی_رسائی, وجہ)
    def test_بنہ_خاکے(خود):
        سے, تک = '۲۰۱۷۱۲۱۵', '۲۰۱۸۰۱۱۵'
        اعداد = ناسا().کوائف_پانا(سے, تک, **جگہ, خاکے=None)
        خود._پورا(سے, تک, اعداد)
