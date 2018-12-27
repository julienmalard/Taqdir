import unittest
from warnings import warn as انتباہ

import pandas as pd
import pandas.testing as pdt
from تقدیر۲.ذرائع import مرکسم۵, مرکسم۵_جال
from تقدیر۲.ذرائع.مرکسم۵ import راستہ_مرکسم_پانا
import requests
راستہ_مرکسم۵ = راستہ_مرکسم_پانا()

try:
    جالبینی_رسائی = requests.head("http://gisweb.ciat.cgiar.org/MarkSimGCM/#tabs-3").status_code == 200
except requests.exceptions.ConnectionError:
    جالبینی_رسائی = False

ذرائع = []
if راستہ_مرکسم۵:
    ذرائع.append(مرکسم۵())
else:
    انتباہ('مرکسم ۵ کا راستہ نھیں ملی۔')

if جالبینی_رسائی:
    ذرائع.append(مرکسم۵_جال())
else:
    انتباہ('جال میں مرکسم ۵ نھیں ملی۔')

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
    def test_جگہ_سحی_نہیں(خود):
        سے, تک = '۲۰۵۰۱۲۰۱', '۲۰۵۱۰۱۱۵'
        for ذریعہ in ذرائع:
            with خود.subTest(ذریعہ.__class__.__name__):
                اعداد = ذریعہ.کوائف_پانا(سے, تک, چوڑائی=1, طول=1, بلندی=1)  # سمندر
                خود._خالی(اعداد)

    @unittest.skipIf(not ذرائع, پیغام)
    def test_خاکے_۰(خود):
        سے, تک = '۲۰۵۱۱۲۰۱', '۲۰۵۲۰۱۱۵'
        for ذریعہ in ذرائع:
            with خود.subTest(ذریعہ.__class__.__name__):
                اعداد = ذریعہ.کوائف_پانا(سے, تک, چوڑائی=11.02, طول=76.96, بلندی=1, خاکے='۰')
                خود._پورا(سے, تک, اعداد)

    @unittest.skipIf(not ذرائع, پیغام)
    def test_خاکے_سحی_نہیں(خود):
        سے, تک = '۲۰۵۰۱۲۰۱', '۲۰۵۱۰۱۱۵'
        for ذریعہ in ذرائع:
            with خود.subTest(ذریعہ.__class__.__name__):
                اعداد = ذریعہ.کوائف_پانا(سے, تک, چوڑائی=11.02, طول=76.96, بلندی=1, خاکے='۱۲۳۴۵۶۷۸۹۰')
                خود._خالی(اعداد)

    @unittest.skipIf(not ذرائع, پیغام)
    def test_سال_کم(خود):
        سے, تک = '۱۹۹۹۰۱۰۱', '۲۰۰۰۰۱۰۱',
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
