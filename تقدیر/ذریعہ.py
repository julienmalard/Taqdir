import datetime
from typing import List

import numpy as np
import pandas as pd

from تقدیر.کام import تاریخ_بنانا, بلندی_پانا
from تقدیر.کوائف import کوائف


class ذریعہ(object):
    """
    آب و ہوا کے کوائف کا ذریعہ۔
    """

    def کوائف_پانا(خود, سے, تک, عرض, طول, بلندی, خاکے='۸.۵'):
        """
        وہ کوائف مہيا کرنا جو ``سے`` اور ``تک`` تاریخ کے درميان اس جگہ اور خاکے کے ليے دستیاب ہیں۔

        Parameters
        ----------
        سے: datetime.date | str
            وہ تاریخ جب سے کوائف چاہيں۔
        تک: datetime.date | str
            وہ تاریخ جب تک کوائف چاہيں ۔
        عرض: float | int
            جگہ کی عرض۔
        طول: float | int
            جگہ کی طول۔
        بلندی: None | float | int
            جگہ کی بلندی۔
        خاکے: None | str
             آب وہوا کی تبدیلی کا خاکا۔

        Returns
        -------
        کوائف:
            ہمہارے (روزانہ) کوائف۔
        """

        سے = تاریخ_بنانا(سے)
        تک = تاریخ_بنانا(تک)

        بلندی = بلندی if بلندی is not None else بلندی_پانا(عرض, طول)

        if تک < سے:
            raise ValueError("آخری تاریخ پہلی تاریخ سے بڑا ہونے چاہئے")

        اعداد = خود._کوائف_روزانہ(سے, تک, خود._کوائف_بنانا(سے, تک, عرض, طول, بلندی, خاکے))

        return کوائف(اعداد)

    @property
    def متغیرات(خود):
        raise NotImplementedError

    def _کوائف_روزانہ(خود, سے, تک, کوائف_پاندس):
        """
        پاندس کے کوائف سے روزانہ کوائف بناتا ہیے۔

        Parameters
        ----------
        سے: datetime.date | str
            وہ تاریخ جب سے کوائف چاہئے۔
        تک: datetime.date | str
            وہ تاریخ جب تک کوائف چاہئے۔
        کوائف_پاندس: pd.DataFrame
            ہمہارے کوائف، پاندس میں۔ اشاریہ روزانہ، ماہانہ یا سالانہ ہو سمکتا ہیے۔

        Returns
        -------
        pd.DataFrame:
            ``سے`` اور ``تک`` کے بیچ میں روزانہ کوائف۔
        """
        اعداد = pd.DataFrame(columns=خود.متغیرات, index=pd.period_range(سے, تک), dtype=float)

        if کوائف_پاندس is None or not len(کوائف_پاندس):
            return اعداد

        if کوائف_پاندس.index.freq == 'D':
            اعداد.fillna(کوائف_پاندس, inplace=True)
        elif کوائف_پاندس.index.freq == 'M':
            for م in کوائف_پاندس.index:
                جہاں = np.logical_and(اعداد.index.month == م.month, اعداد.index.year == م.year)
                اعداد.loc[جہاں, کوائف_پاندس.columns] = کوائف_پاندس.loc[م].values
        elif کوائف_پاندس.index.freq == 'Y':
            for س in کوائف_پاندس.index:
                جہاں = اعداد.index.year == س.year
                اعداد.loc[جہاں, کوائف_پاندس.columns] = کوائف_پاندس.loc[س].values
        else:
            raise ValueError(کوائف_پاندس.index)

        return اعداد

    @staticmethod
    def _اشاریہ_پانڈا_بنانا(تاریخیں):
        """
        پاندس کا تاریخ کے اشاریہ بناتا ہیے۔
        
        Parameters
        ----------
        تاریخیں: List or pd.Index
            ہمہارے تاریخ کا فرست۔

        Returns
        -------
        pd.PeriodIndex:
            روزانہ، ماہانہ یا سالانہ اشاریہ۔
        """
        if isinstance(تاریخیں, pd.DatetimeIndex):
            return تاریخیں.to_period()

        if isinstance(تاریخیں, pd.PeriodIndex):
            return تاریخیں

        تاریخ = تاریخیں[0]
        لمبای = len(str(تاریخ))
        if لمبای == 4:
            ھر = 'Y'
        elif لمبای <= 7:
            ھر = 'M'
        else:
            ھر = 'D'
        return pd.PeriodIndex(تاریخیں, freq=ھر)

    def _کوائف_بنانا(خود, سے, تک, عرض, طول, بلندی, خاکے):
        """
        ایک جگہ کے لئے خاکے  کے لحاص سے ``سے`` سے ``تک`` تک کوائف دینا۔

        Parameters
        ----------
        سے: datetime.date | str
            وہ تاریخ جب سے کوائف چاہيں۔
        تک: datetime.date | str
            وہ تاریخ جب تک کوائف چاہيں۔
        عرض: float | int
            جگہ کا عرض۔
        طول: float | int
            جگہ کا طول۔
        بلندی: None | float | int
            جگہ کی بلندی۔
        خاکے: None | str
             آب وہوا کی تبدیلی کا خاکا۔

        Returns
        -------
        pd.DataFrame
            کوائف، پاندس میں۔ اگر ان تاریخ، جگہ، یا خاکے کے لئے اس ذریعے میں کوائف
            دستیاب نہیں ہیں، تو پھر ``None`` واپس دینا۔ پاندس کا اشاریہ
            pd.PeriodIndex ہونا چاہئے۔ اشاریہ روزانہ، ماہانہ، سا لانہ کا ہو سکتا ہے۔
        """
        raise NotImplementedError
