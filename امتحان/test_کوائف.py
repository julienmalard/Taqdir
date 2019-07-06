import os
import tempfile
import unittest
from datetime import date, timedelta

import numpy as np
import numpy.testing as npt
import pandas as pd

from تقدیر.متغیرات import متغیرات, بارش
from تقدیر.کوائف import کوائف


class امتحان_کوائف(unittest.TestCase):

    @classmethod
    def setUpClass(قسم):
        قسم.سے = date(2001, 1, 1)
        قسم.تک = date(2001, 3, 1)
        قسم.تاریخیں = pd.period_range(قسم.سے, قسم.تک)

        قسم.اعداد_سے = date(2000, 12, 1)
        قسم.اعداد_تک = date(2001, 2, 15)
        تاریخیں_اعداد = pd.period_range(قسم.اعداد_سے, قسم.اعداد_تک)
        اعداد = pd.DataFrame(
            data={س: np.random.random(len(تاریخیں_اعداد)) for س in متغیرات},
            columns=متغیرات,
            index=تاریخیں_اعداد
        )
        اعداد[str(بارش)].loc[قسم.اعداد_تک] = np.nan

        قسم.کوائف = کوائف(اعداد, قسم.سے, قسم.تک)

        قسم.راستہ = tempfile.TemporaryDirectory()

    def test_تاریخیں(خود):
        تاریخیں = خود.کوائف.روزانہ().index
        npt.assert_array_equal(تاریخیں, خود.تاریخیں)

    def test_جوڑنا(خود):
        تاریخیں = pd.period_range(خود.اعداد_تک, خود.تک)
        اعداد = pd.DataFrame(
            data={س: np.random.random(len(تاریخیں)) for س in متغیرات},
            columns=متغیرات,
            index=تاریخیں
        )
        کوائف_ = کوائف(اعداد, خود.سے, خود.تک)
        کوائف_ += خود.کوائف
        خود.assertEqual(len(کوائف_.لاپتہ()), 0)

    def test_لیکھنا(خود):
        ف_وضعِ = ['.csv', '.json']
        نام = "امتحان"
        for وضعِ in ف_وضعِ:
            with خود.subTest(وضعِ):
                خود.کوائف.لکھنا(راستہ=خود.راستہ.name, نام=نام, وضع=وضعِ)
                خود.assertTrue(os.path.isfile(os.path.join(خود.راستہ.name, نام + وضعِ)))

    def test_لاپتہ_سارے(خود):
        لاپتہ = خود.کوائف.لاپتہ(سارے=True)
        npt.assert_array_equal(لاپتہ, pd.period_range(خود.اعداد_تک + timedelta(1), خود.تک))

    def test_لاپتہ_ایک_ھی(خود):
        لاپتہ = خود.کوائف.لاپتہ(سارے=False)
        npt.assert_array_equal(لاپتہ, pd.period_range(خود.اعداد_تک, خود.تک))

    def test_سالانہ(خود):
        npt.assert_array_equal(خود.کوائف.سالانہ().index, خود.تاریخیں.asfreq('Y').unique())

    def test_ماہانہ(خود):
        npt.assert_array_equal(خود.کوائف.ماہانہ().index, خود.تاریخیں.asfreq('M').unique())

    def test_روزانہ(خود):
        npt.assert_array_equal(خود.کوائف.روزانہ(), خود.کوائف.اعداد)

    @classmethod
    def tearDownClass(قسم):
        قسم.راستہ.cleanup()
