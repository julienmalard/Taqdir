import pandas as pd


class آدادوشمار(object):
    def __init__(خود, سے, تک, آداد=None):
        ستون = ['بارش', 'شمسی_تابکاری', 'درجہ_حرارت_زیادہ', 'درجہ_حرارت_کم', 'درجہ_حرارت_اوسط']
        خود.آداد = pd.DataFrame(آداد, columns=ستون, index=pd.period_range(سے, تک))
        خود.سے = سے
        خود.تک = تک

    def روزانہ(خود):
        return خود.آداد

    def ماہانہ(خود):
        return خود.آداد.resample('M').mean()

    def سالانہ(خود):
        return خود.آداد.resample('Y').mean()

    def لاپتہ(خود, سارہ=False):
        if سارہ:
            return خود.آداد[خود.آداد.isnull().all(axis=1)].index
        else:
            return خود.آداد[خود.آداد.isnull().any(axis=1)].index

    def لکھنا(خود):
        pass

    def __add__(خود, دوسرہ):
        return آدادوشمار(خود.سے, خود.تک, آداد=خود.آداد.combine_first(دوسرہ))
