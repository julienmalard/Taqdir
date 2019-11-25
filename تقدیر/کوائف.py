import os
from datetime import date

import numpy as np
import pandas as pd


class کوائف(object):
    """
    آب وہوا کے کوائف۔
    """

    def __init__(خود, اعداد, سے=None, تک=None, متغیرات=None):
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
        if متغیرات is None:
            متغیرات = اعداد.columns

        سے = سے or اعداد.index.min()
        تک = تک or اعداد.index.max()

        خود.اعداد = pd.DataFrame(columns=متغیرات, index=pd.period_range(سے, تک), dtype=float)
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
        if all(م in خود.اعداد for م in ['درجہ_حرارت_کم', 'درجہ_حرارت_زیادہ']):
            if 'درجہ_حرارت_اوسط' not in خود.اعداد:
                خود.اعداد['درجہ_حرارت_اوسط'] = np.nan
            خود.اعداد['درجہ_حرارت_اوسط'].fillna(
                (خود.اعداد['درجہ_حرارت_کم'] + خود.اعداد['درجہ_حرارت_زیادہ']) / 2, inplace=True
            )

    def روزانہ(خود):
        """
        روزانہ کی ظرز پر کوائف ۔

        Returns
        -------
        pd.DataFrame
        """
        return خود.اعداد

    def ماہانہ(خود):
        """
        ماہانہ کی ظرز پر کوائف ۔

        Returns
        -------
        pd.DataFrame
            کوائف کی ماہانہ اوسط۔
        """
        return خود.اعداد.resample('M').mean()

    def سالانہ(خود):
        """
        سالانہ کی ظرز پر کوائف ۔

        Returns
        -------
        pd.DataFrame
            کوائف کی سالانہ اوسط۔
        """
        return خود.اعداد.resample('Y').mean()

    def لاپتہ(خود, سارے=False):
        """
        نا معلوم دنوں کے کوائف واپس دیگا۔

        Parameters
        ----------
        سارے: bool
             صرف ان دنوں  کے کوائف دے گا جینکے سارےعمودی ستون کے کوائف نا معلوم ہیں۔

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
            مسل کا وضع۔ `.csv` یا `.json` ہو سکتا ہے۔

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

    def متاغیرات(خود):
        return list(خود.اعداد.columns)

    def __add__(خود, دوسرہ):
        return کوائف(خود.اعداد.combine_first(دوسرہ.اعداد), خود.سے, خود.تک)
