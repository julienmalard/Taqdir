import os
from datetime import date

import pandas as pd

from تقدیر.کام import متاغیرات


class کوائف(object):
    """
    آبوہوا کے کوائف۔
    """

    def __init__(خود, اعداد, سے=None, تک=None):
        """
        خالی (یا نہ خالی) کوائف بانانا۔

        Parameters
        ----------
        اعداد: pd.DataFrame | None
            پہلہ سے ھونے طالے اعدادو شمار۔
        سے: date
            پہلی تاریخ۔
        تک: date
            آخری تاریخ۔
        """

        if اعداد is None and (سے is None or تک is None):
            raise ValueError

        سے = سے or اعداد.index.min()
        تک = تک or اعداد.index.max()

        خود.اعداد = pd.DataFrame(columns=متاغیرات, index=pd.period_range(سے, تک))
        if اعداد is not None:
            خود.اعداد = خود.اعداد.combine_first(اعداد)
        خود.اعداد = خود.اعداد[سے:تک]

        خود.سے = سے
        خود.تک = تک
        خود._بھرنا()

    def _بھرنا(خود):
        """
        لاپتہ کہائف کو بھرنے کی کوشیش کریگا۔
        """

        # لاپتہ اوست درجہ حرارت بھرنا، جہاں بھر جا سکتا ھیے۔
        خود.اعداد['درجہ_حرارت_اوسط'].fillna(
            (خود.اعداد['درجہ_حرارت_کم'] + خود.اعداد['درجہ_حرارت_زیادہ']) / 2, inplace=True
        )

    def روزانہ(خود):
        """
        روزانہ کوائف پانا۔

        Returns
        -------
        pd.DataFrame
        """
        return خود.اعداد

    def ماہانہ(خود):
        """
        ماہانہ کوائف پانا۔

        Returns
        -------
        pd.DataFrame
            کوائف کے ماہانہ اوسط۔
        """
        return خود.اعداد.resample('M').mean()

    def سالانہ(خود):
        """
        سالانہ کوائف پانا۔

        Returns
        -------
        pd.DataFrame
            کوائف کے سالانہ اوسط۔
        """
        return خود.اعداد.resample('Y').mean()

    def لاپتہ(خود, سارے=False):
        """
        لاپتہ کوائف رکھنے والے دن واپس دیگا۔

        Parameters
        ----------
        سارے: bool
            اگر صرف ان دنوں دینا جینکے سارے ستون کے کوائف لاپتہ ہیں۔

        Returns
        -------
        pd.PeriodIndex
        """
        if سارے:
            return خود.اعداد[خود.اعداد.isnull().all(axis=1)].index
        return خود.اعداد[خود.اعداد.isnull().any(axis=1)].index

    def لکھنا(خود, راستہ, نام='تقدیر', وضع='.csv'):
        """
        کوائف کو مسل میں رکھنا۔
        
        Parameters
        ----------
        راستہ: str
            مسل کا راستہ۔
        نام: str
            مسل کا نام۔
        وضع: str
            مسل کا وضع۔ `.csv` یا `.json` ہو سکتا ہیے۔

        """
        if not os.path.isdir(راستہ):
            os.mkdir(راستہ)
        پورا_نام = os.path.join(راستہ, نام + وضع)

        if وضع == '.csv':
            خود.اعداد.to_csv(پورا_نام, encoding='utf8')
        elif وضع == '.json':
            خود.اعداد.to_json(پورا_نام, force_ascii=False)
        else:
            raise ValueError(وضع)

    def __add__(خود, دوسرہ):
        return کوائف(خود.اعداد.combine_first(دوسرہ.اعداد), خود.سے, خود.تک)
