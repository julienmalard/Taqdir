import pandas as pd


class ذریعہ(object):
    def کوائف_پانا(خود, سے, تک, چوڑائی, طول, بلندی, خاکے='۸۔۵ََ'):
        raise NotImplementedError

    @staticmethod
    def _پاندس_بنانا(سے, تک):
        ستون = ['بارش', 'شمسی_تابکاری', 'درجہ_حرارت_زیادہ', 'درجہ_حرارت_کم', 'درجہ_حرارت_اوسط']
        اعداد_پاندس = pd.DataFrame(columns=list(ستون), index=pd.period_range(سے, تک))
        return اعداد_پاندس
