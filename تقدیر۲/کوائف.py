import os
from datetime import date

import pandas as pd

from .ذریعہ import ذریعہ


class کوائف(object):
    def __init__(خود, سے, تک, اعداد=None):
        """
        خالی (یا نہ خالی) کوائف بانانا۔

        Parameters
        ----------
        سے: date
            پہلی تاریخ۔
        تک: date
            آخری تاریخ۔
        اعداد: pd.DataFrame
            پہلہ سے ھونے طالے اعدادو شمار۔
        """

        خود.اعداد = pd.DataFrame(اعداد, columns=ذریعہ.ستون, index=pd.period_range(سے, تک))
        if اعداد is not None:
            خود.اعداد.combine_first(اعداد)

        خود.سے = سے
        خود.تک = تک
        خود._بھرنا()

    def _بھرنا(خود):
        """
        لاپتہ کہائف کو بھرنے کی کوشیش کریگا۔
        """

        # لاپتہ اوست درجہ حرارت بھرنا، جہاں بھر جا سکتا ھیے۔
        خود.اعداد['درجہ_حرارت_اوسط'].fillna((خود.اعداد['درجہ_حرارت_کم'] + خود.اعداد['درجہ_حرارت_زیادہ']) / 2)

    def روزانہ(خود):
        """
        رہزانہ کوائف پانا۔

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
        """
        return خود.اعداد.resample('M').mean()

    def سالانہ(خود):
        """
        سالانہ کوائف پانا۔

        Returns
        -------
        pd.DataFrame
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
        else:
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
            مسل کا وضع۔

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
        return کوائف(خود.سے, خود.تک, اعداد=خود.اعداد.combine_first(دوسرہ.اعداد))
