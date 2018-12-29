import pandas as pd


class ذریعہ(object):
    """

    """

    ستون = ['بارش', 'شمسی_تابکاری', 'درجہ_حرارت_زیادہ', 'درجہ_حرارت_کم', 'درجہ_حرارت_اوسط']

    def کوائف_پانا(خود, سے, تک, چوڑائی, طول, بلندی, خاکے='۸۔۵ََ'):
        """

        Parameters
        ----------
        سے
        تک
        چوڑائی
        طول
        بلندی
        خاکے

        Returns
        -------

        """
        raise NotImplementedError

    def _پاندس_بنانا(خود, سے, تک):
        """

        Parameters
        ----------
        سے
        تک

        Returns
        -------

        """
        اعداد_پاندس = pd.DataFrame(columns=list(خود.ستون), index=pd.period_range(سے, تک), dtype=float)
        return اعداد_پاندس
