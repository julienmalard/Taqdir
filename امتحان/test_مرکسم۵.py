import os
import sys
import unittest
from warnings import warn as انتباہ

import pandas as pd
import pandas.testing as pdt
import requests
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from تقدیر.ذرائع import مرکسم۵, مرکسم۵_جال
from تقدیر.ذرائع.مرکسم۵ import راستہ_مرکسم_پانا

راستہ_مرکسم۵ = راستہ_مرکسم_پانا()

try:
    جال_بینی_رسائی = requests.head("http://gisweb.ciat.cgiar.org/MarkSimGCM/#tabs-3").status_code == 200
    webdriver.Firefox()
except (requests.exceptions.ConnectionError, WebDriverException):
    جال_بینی_رسائی = False


def مرکسم_۵_بنانا(نمونہ='۱۱۱۱۱۱۱۱۱۱۱۱۱۱۱۱۱'):
    if راستہ_مرکسم۵:
        return مرکسم۵(نمونہ=نمونہ)
    انتباہ('مرکسم ۵ کا راستہ نھیں ملا۔')
    پایتھان = sys.executable
    return مرکسم۵(پایتھان + ' ' + os.path.join(os.path.split(__file__)[0], 'وسائل/مرکسم۵_جیسے.py'), نمونہ=نمونہ)
    # مجھے لگتا ہے کہ اوپر راستہ ٹھيک نہيں


class امتحان_مرکسم۵(unittest.TestCase):
    @classmethod
    def setUpClass(قسم):
        قسم.ذرائع = [مرکسم_۵_بنانا()]

        if جال_بینی_رسائی:
            قسم.ذرائع.append(مرکسم۵_جال())
        else:
            انتباہ('جال بین میں مرکسم ۵ کا پتہ نھیں ملا۔')

    @staticmethod
    def _مکمل(سے, تک, اعداد):
        pdt.assert_index_equal(اعداد.روزانہ().dropna(how='all').index, pd.period_range(سے, تک, freq='D'))

    def _خالی(خود, اعداد):
        if اعداد is not None:
            خود.assertEqual(len(اعداد.روزانہ().dropna(how='all').index), 0)

    def test_کوائف_پانا(خود):
        سے, تک = '۲۰۵۰۱۲۰۱', '۲۰۵۱۰۱۱۵'
        for ذریعہ in خود.ذرائع:
            with خود.subTest(ذریعہ.__class__.__name__):
                اعداد = ذریعہ.کوائف_پانا(سے, تک, عرض=11.02, طول=76.96, بلندی=1)
                خود._مکمل(سے, تک, اعداد)

    def test_دوسرہ_نمونہ(خود):
        نمونہ = '۰۱۰۱۰۱۰۱۰۱۰۱۰۱۰۱۱'
        ذرائع = [مرکسم_۵_بنانا(نمونہ)]
        if جال_بینی_رسائی:
            ذرائع.append(مرکسم۵_جال(نمونہ=نمونہ))
        سے, تک = '۲۰۵۰۱۲۰۱', '۲۰۵۱۰۱۱۵'

        for ذریعہ in ذرائع:
            with خود.subTest(ذریعہ.__class__.__name__):
                اعداد = ذریعہ.کوائف_پانا(سے, تک, عرض=11.02, طول=76.96, بلندی=1)
                خود._مکمل(سے, تک, اعداد)

    def test_خاکے_۰(خود):
        سے, تک = '۲۰۵۲۰۱۰۱', '۲۰۵۲۰۱۱۵'
        for ذریعہ in خود.ذرائع:
            with خود.subTest(ذریعہ.__class__.__name__):
                اعداد = ذریعہ.کوائف_پانا(سے, تک, عرض=11.02, طول=76.96, بلندی=1, خاکے='۰')
                خود._مکمل(سے, تک, اعداد)

    def test_خاکے_صيحی_نہیں(خود):
        سے, تک = '۲۰۵۱۰۱۱۵', '۲۰۵۲۰۱۰۱'
        for ذریعہ in خود.ذرائع:
            with خود.subTest(ذریعہ.__class__.__name__):
                اعداد = ذریعہ.کوائف_پانا(سے, تک, عرض=11.02, طول=76.96, بلندی=1, خاکے='۱۲۳۴۵۶۷۸۹۰')
                خود._خالی(اعداد)

    def test_سال_کم(خود):
        سے, تک = '۱۹۹۹۰۱۰۱', '۱۹۹۹۰۲۰۱'
        for ذریعہ in خود.ذرائع:
            with خود.subTest(ذریعہ.__class__.__name__):
                اعداد = ذریعہ.کوائف_پانا(سے, تک, عرض=11.02, طول=76.96, بلندی=1)
                خود._مکمل(سے, تک, اعداد)

    def test_سال_زیادہ(خود):
        سے, تک = '۲۱۰۰۰۱۰۱', '۲۱۰۰۰۲۰۱'
        for ذریعہ in خود.ذرائع:
            with خود.subTest(ذریعہ.__class__.__name__):
                اعداد = ذریعہ.کوائف_پانا(سے, تک, عرض=11.02, طول=76.96, بلندی=1)
                خود._خالی(اعداد)

    def test_نمونہ_صيحی_نہیں(خود):
        for ذریعہ in خود.ذرائع:
            with خود.subTest(ذریعہ.__class__.__name__):
                with خود.assertRaises(ValueError):
                    ذریعہ.__class__(نمونہ='۰۱۰۱۰۱۰۱۰۱۰۱۰۱۰۱۲')

    def test_نمونہ_زیادہ_لمبا(خود):
        for ذریعہ in خود.ذرائع:
            with خود.subTest(ذریعہ.__class__.__name__):
                with خود.assertRaises(ValueError):
                    ذریعہ.__class__(نمونہ='۰۱۰۱۰۱۰۱۰۱۰۱۰۱۰۱۰۱')
