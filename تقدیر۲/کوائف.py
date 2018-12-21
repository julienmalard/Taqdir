import os

import pandas as pd


class کوائف(object):
    def __init__(خود, سے, تک, اعداد=None):
        ستون = ['بارش', 'شمسی_تابکاری', 'درجہ_حرارت_زیادہ', 'درجہ_حرارت_کم', 'درجہ_حرارت_اوسط']
        خود.اعداد = pd.DataFrame(اعداد, columns=ستون, index=pd.period_range(سے, تک))
        خود.سے = سے
        خود.تک = تک

    def روزانہ(خود):
        return خود.اعداد

    def ماہانہ(خود):
        return خود.اعداد.resample('M').mean()

    def سالانہ(خود):
        return خود.اعداد.resample('Y').mean()

    def لاپتہ(خود, سارہ=False):
        if سارہ:
            return خود.اعداد[خود.اعداد.isnull().all(axis=1)].index
        else:
            return خود.اعداد[خود.اعداد.isnull().any(axis=1)].index

    def لکھنا(خود, راستہ, نام='تقدیر', وضع='.csv'):
        if not os.path.isdir(راستہ):
            os.mkdir(راستہ)
        پئرا_نام = os.path.join(راستہ, نام+وضع)

        if وضع == '.csv':
            خود.اعداد.to_csv(پئرا_نام, encoding='utf8')
        elif وضع == '.json':
            خود.اعداد.to_json(پئرا_نام, force_ascii=False)
        else:
            raise ValueError(وضع)

    def __add__(خود, دوسرہ):
        return کوائف(خود.سے, خود.تک, اعداد=خود.اعداد.combine_first(دوسرہ.اعداد))
