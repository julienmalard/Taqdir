import datetime
from typing import List

import numpy as np
import pandas as pd

from تقدیر.کام import متاغیرات, تاریخ_بنانا
from تقدیر.کوائف import کوائف


class ذریعہ(object):
    """
    آبو ہوا کے کوائف کا ذریعہ۔
    """

    def کوائف_پانا(خود, سے, تک, چوڑائی, طول, بلندی, خاکے='۸۔۵'):
        """
        ان کوائف دینا جو ``سے`` اور ``تک`` تاریخ کے بیچ میں اس جگہ اور خاکے پر دستیاب ہیں۔

        Parameters
        ----------
        سے: datetime.date | str
            وہ تاریخ جب سے کوائف چاہئے۔
        تک: datetime.date | str
            وہ تاریخ جب تک کوائف چاہئے۔
        چوڑائی: float | int
            جگہ کی چوڑائی۔
        طول: float | int
            جگہ کی طول۔
        بلندی: None | float | int
            جگہ کی بلندی۔
        خاکے: None | str
             آبوہوا کی تبدیلی کا خاکے۔

        Returns
        -------
        کوائف:
            ہمہارے (روزانہ) کوائف۔
        """

        سے = تاریخ_بنانا(سے)
        تک = تاریخ_بنانا(تک)

        if تک <= سے:
            raise ValueError("آخری تاریخ پہلی تاریخ سے بڑا ہونے چاہئے")

        اعداد = خود._کوائف_روزانہ(سے, تک, خود._کوائف_بنانا(سے, تک, چوڑائی, طول, بلندی, خاکے))

        return کوائف(اعداد)

    @staticmethod
    def _کوائف_روزانہ(سے, تک, کوائف_پاندس):
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
        اعداد = pd.DataFrame(columns=list(متاغیرات), index=pd.period_range(سے, تک), dtype=float)

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
    def _اشاریہ_پاندس_بنانا(تاریخیں):
        """
        پاندس کا تاریخ کے اشاریہ بناتا ہیے۔
        
        Parameters
        ----------
        تاریخیں: List
            ہمہارے تاریخ کا فرست۔

        Returns
        -------
        pd.PeriodIndex:
            روزانہ، ماہانہ یا سالانہ اشاریہ۔
        """
        تاریخ = تاریخیں[0]
        لمبای = len(str(تاریخ))
        if لمبای == 4:
            ھر = 'Y'
        elif لمبای <= 7:
            ھر = 'M'
        else:
            ھر = 'D'
        return pd.PeriodIndex(تاریخیں, freq=ھر)

    def _کوائف_بنانا(خود, سے, تک, چوڑائی, طول, بلندی, خاکے):
        """
        ایک جگہ کے لئے ``سے`` سے ``تک`` تک کوائف دینا، خاکے کے لحاس سے۔

        Parameters
        ----------
        سے: datetime.date | str
            وہ تاریخ جب سے کوائف چاہئے۔
        تک: datetime.date | str
            وہ تاریخ جب تک کوائف چاہئے۔
        چوڑائی: float | int
            جگہ کی چوڑائی۔
        طول: float | int
            جگہ کی طول۔
        بلندی: None | float | int
            جگہ کی بلندی۔
        خاکے: None | str
             آبوہوا کی تبدیلی کا خاکے۔

        Returns
        -------
        pd.DataFrame:
            کوائف، پاندس میں۔ اگر ان تاریخ، جگہ، یا خاکے کع لئے اس ذریعہ میں کوائف دستیاب نہیں ہیں، پھیر
             ``None`` واپس دینا۔ پاندس کا اشاریہ pd.PeriodIndex ہونے چاہئے۔ اشاریہ روزانہ، مہانہ، ےا سلانہ
             کا ہو سکتا ہیے۔
        """
        raise NotImplementedError
