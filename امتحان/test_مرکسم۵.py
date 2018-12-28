import os
import unittest
from warnings import warn as انتباہ

import pandas as pd
import pandas.testing as pdt
import requests
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from تقدیر۲.ذرائع import مرکسم۵, مرکسم۵_جال
from تقدیر۲.ذرائع.مرکسم۵ import راستہ_مرکسم_پانا

راستہ_مرکسم۵ = راستہ_مرکسم_پانا()

try:
    جالبینی_رسائی = requests.head("http://gisweb.ciat.cgiar.org/MarkSimGCM/#tabs-3").status_code == 200
    webdriver.Firefox()
except (requests.exceptions.ConnectionError, WebDriverException):
    جالبینی_رسائی = False

ذرائع = []
if راستہ_مرکسم۵:
    ذرائع.append(مرکسم۵())
else:
    ذرائع.append(مرکسم۵(os.path.join(os.path.split(__file__)[0], 'وسائل/مرکسم۵_جیسے.py')))
    انتباہ('مرکسم ۵ کا راستہ نھیں ملی۔')

if جالبینی_رسائی:
    ذرائع.append(مرکسم۵_جال())
else:
    انتباہ('جالبین میں مرکسم ۵ کا پنہ نھیں ملا۔')

پیغام = 'مرکسم ملی نہیں۔'


class امتحان_مرکسم۵(unittest.TestCase):
    @staticmethod
    def _پورا(سے, تک, اعداد):
        pdt.assert_index_equal(اعداد.dropna(how='all').index, pd.period_range(سے, تک, freq='D'))

    def _خالی(خود, اعداد):
        if اعداد is not None:
            خود.assertEqual(len(اعداد.dropna(how='all').index), 0)

    @unittest.skipIf(not ذرائع, پیغام)
    def test_کوائف_پانا(خود):
        سے, تک = '۲۰۵۰۱۲۰۱', '۲۰۵۱۰۱۱۵'
        for ذریعہ in ذرائع:
            with خود.subTest(ذریعہ.__class__.__name__):
                اعداد = ذریعہ.کوائف_پانا(سے, تک, چوڑائی=11.02, طول=76.96, بلندی=1)
                خود._پورا(سے, تک, اعداد)

    @unittest.skipIf(not ذرائع, پیغام)
    def test_خاکے_۰(خود):
        سے, تک = '۲۰۵۲۰۱۰۱', '۲۰۵۲۰۱۱۵'
        for ذریعہ in ذرائع:
            with خود.subTest(ذریعہ.__class__.__name__):
                اعداد = ذریعہ.کوائف_پانا(سے, تک, چوڑائی=11.02, طول=76.96, بلندی=1, خاکے='۰')
                خود._پورا(سے, تک, اعداد)

    @unittest.skipIf(not ذرائع, پیغام)
    def test_خاکے_سحی_نہیں(خود):
        سے, تک = '۲۰۵۲۰۱۰۱', '۲۰۵۱۰۱۱۵'
        for ذریعہ in ذرائع:
            with خود.subTest(ذریعہ.__class__.__name__):
                اعداد = ذریعہ.کوائف_پانا(سے, تک, چوڑائی=11.02, طول=76.96, بلندی=1, خاکے='۱۲۳۴۵۶۷۸۹۰')
                خود._خالی(اعداد)

    @unittest.skipIf(not ذرائع, پیغام)
    def test_سال_کم(خود):
        سے, تک = '۱۹۹۹۰۱۰۱', '۱۹۹۹۰۲۰۱'
        for ذریعہ in ذرائع:
            with خود.subTest(ذریعہ.__class__.__name__):
                اعداد = ذریعہ.کوائف_پانا(سے, تک, چوڑائی=11.02, طول=76.96, بلندی=1)
                خود._پورا(سے, تک, اعداد)

    @unittest.skipIf(not ذرائع, پیغام)
    def test_سال_زیادہ(خود):
        سے, تک = '۲۱۰۰۰۱۰۱', '۲۱۰۰۰۲۰۱'
        for ذریعہ in ذرائع:
            with خود.subTest(ذریعہ.__class__.__name__):
                اعداد = ذریعہ.کوائف_پانا(سے, تک, چوڑائی=11.02, طول=76.96, بلندی=1)
                خود._خالی(اعداد)
