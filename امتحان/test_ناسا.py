import unittest

import pandas as pd
import pandas.testing as pdt
import requests
from pcse.db import NASAPowerWeatherDataProvider
from تقدیر۲.ذرائع import ناسا

try:
    جالبینی_رسائی = requests.head("https://power.larc.nasa.gov/cgi-bin/v1/DataAccess.py").status_code == 200
    NASAPowerWeatherDataProvider(latitude=11.02, longitude=76.96, force_update=False)
except (requests.exceptions.ConnectionError, KeyError):
    جالبینی_رسائی = False
وجہ = 'ناسا کا جالبین پنہ اب دستیاب نہیں۔'


class امتحان_ناسا(unittest.TestCase):
    @staticmethod
    def _پورا(سے, تک, اعداد):
        pdt.assert_index_equal(اعداد.dropna(how='all').index, pd.period_range(سے, تک, freq='D'))

    @unittest.skipUnless(جالبینی_رسائی, وجہ)
    def test_کوائف_پانا(خود):
        سے, تک = '۲۰۱۷۱۲۱۵', '۲۰۱۸۰۱۱۵'
        اعداد = ناسا().کوائف_پانا(سے, تک, چوڑائی=11.02, طول=76.96, بلندی=1, خاکے='۴۔۵')
        خود._پورا(سے, تک, اعداد)

    @unittest.skipUnless(جالبینی_رسائی, وجہ)
    def test_بنہ_خاکے(خود):
        سے, تک = '۲۰۱۷۱۲۱۵', '۲۰۱۸۰۱۱۵'
        اعداد = ناسا().کوائف_پانا(سے, تک, چوڑائی=11.02, طول=76.96, بلندی=1, خاکے=None)
        خود._پورا(سے, تک, اعداد)
