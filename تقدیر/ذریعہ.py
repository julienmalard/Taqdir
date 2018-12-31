import datetime

import pandas as pd


class ذریعہ(object):
    """

    """

    ستون = ['بارش', 'شمسی_تابکاری', 'درجہ_حرارت_زیادہ', 'درجہ_حرارت_کم', 'درجہ_حرارت_اوسط']

    def کوائف_پانا(خود, سے, تک, چوڑائی, طول, بلندی, خاکے='۸۔۵'):
        """

        Parameters
        ----------
        سے: datetime.date | str
            وہ تاریخ جب سے کوائف چاہئے۔
        تک: datetime.date | str
            وہ تاریخ جب تک کوائف چاہئے۔
        چوڑائی: float | int
        طول: float | int
        بلندی: float | int
        خاکے: str
             آبوہوا کی تبدیلی کا خاکے۔

        Returns
        -------
        کوائف:

        """
        raise NotImplementedError

    def _پاندس_بنانا(خود, سے, تک):
        """

        Parameters
        ----------
        سے: datetime.date | str
        تک: datetime.date | str

        Returns
        -------

        """
        اعداد_پاندس = pd.DataFrame(columns=list(خود.ستون), index=pd.period_range(سے, تک), dtype=float)
        return اعداد_پاندس
